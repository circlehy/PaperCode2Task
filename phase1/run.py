"""
Phase 1 — Data Ingestion + Paper Parsing + Repo Acquisition

For each of 50 stratified sampled pairs (25 official + 25 non-official):
  1. Level 1: title-based token extraction → task_hint, method_hint, domain_hint
  2. Level 2: arXiv abstract fetch (only if paper_url_abs is arxiv.org)
  3. Pre-clone URL validation (sub-tree URL check)
  4. GitHub API size check (unauthenticated)
  5. git clone --depth=1
  6. Repo content pre-check (executable code count, README, two-tiered sparse check)

Output:
  output/phase1/pairs.jsonl     — one PairRecord JSON per line
  output/phase1/sample_ids.json — sampled paper IDs for reproducibility
  output/repos/{arxiv_id}/      — cloned repos (kept for Phase 4)

Run:
  python phase1/run.py
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml
from bs4 import BeautifulSoup
from datasets import load_dataset
from dotenv import load_dotenv
from tqdm import tqdm

# ── paths ─────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")
CONFIG_PATH = ROOT / "configs" / "patterns.yaml"
OUTPUT_DIR = ROOT / "output" / "phase1"
REPOS_DIR = ROOT / "output" / "repos"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPOS_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT / "phase0"))
from schema import PairRecord, PaperSemantics

# ── constants ─────────────────────────────────────────────────────────────────

SAMPLE_OFFICIAL = 25
SAMPLE_NONOFFICIAL = 25
RANDOM_SEED = 42
CLONE_TIMEOUT = 90       # seconds
LARGE_REPO_MB = 500
ARXIV_FETCH_TIMEOUT = 15
SPARSE_THRESHOLD = 3     # min executable code files

# ── config ────────────────────────────────────────────────────────────────────

def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

# ── 1. sampling ───────────────────────────────────────────────────────────────

def sample_pairs(ds, n_official: int, n_nonofficial: int, seed: int,
                 exclude_ids: set[str] | None = None) -> list[dict]:
    """
    Stratified sample: n_official official + n_nonofficial non-official.
    exclude_ids: set of paper_arxiv_id values to skip (for batch 2+).
    """
    import random
    rng = random.Random(seed)
    exclude_ids = exclude_ids or set()

    official = [
        dict(e) for e in ds
        if e["is_official"] is True and e.get("paper_arxiv_id") not in exclude_ids
    ]
    nonofficial = [
        dict(e) for e in ds
        if e["is_official"] is False and e.get("paper_arxiv_id") not in exclude_ids
    ]

    sampled_official = rng.sample(official, min(n_official, len(official)))
    sampled_nonofficial = rng.sample(nonofficial, min(n_nonofficial, len(nonofficial)))

    pairs = sampled_official + sampled_nonofficial
    rng.shuffle(pairs)
    return pairs

# ── 2. paper parsing — level 1 (title extraction) ────────────────────────────

def _match_keywords(text: str, keyword_list: list[str]) -> str | None:
    """Return first keyword (longest first) found in text, or None."""
    text_lower = text.lower()
    for kw in sorted(keyword_list, key=lambda x: -len(x)):
        if kw.lower() in text_lower:
            return kw.lower()
    return None


def extract_title_hints(title: str, cfg: dict) -> dict:
    """
    Extract task_hint, method_hint, domain_hint from paper title.
    domain_hint uses a fixed modality/domain term list instead of leftover tokens.
    """
    task_hint = _match_keywords(title, cfg.get("title_task_keywords", []))
    method_hint = _match_keywords(title, cfg.get("title_method_keywords", []))
    domain_hint = _match_keywords(title, cfg.get("domain_terms", []))
    return {"task_hint": task_hint, "method_hint": method_hint, "domain_hint": domain_hint}


def enrich_hints_from_abstract(hints: dict, abstract: str, cfg: dict) -> tuple[dict, bool]:
    """
    Fill any None hints using abstract text as fallback.
    Only fills fields that title extraction left empty.
    Returns (updated_hints, was_enriched).
    """
    enriched = False
    if not abstract:
        return hints, False
    if hints["task_hint"] is None:
        hit = _match_keywords(abstract, cfg.get("title_task_keywords", []))
        if hit:
            hints["task_hint"] = hit
            enriched = True
    if hints["method_hint"] is None:
        hit = _match_keywords(abstract, cfg.get("title_method_keywords", []))
        if hit:
            hints["method_hint"] = hit
            enriched = True
    if hints["domain_hint"] is None:
        hit = _match_keywords(abstract, cfg.get("domain_terms", []))
        if hit:
            hints["domain_hint"] = hit
            enriched = True
    return hints, enriched

# ── 2. paper parsing — level 2 (arXiv abstract) ──────────────────────────────

def fetch_arxiv_abstract(paper_url_abs: str, paper_arxiv_id: str | None) -> tuple[str | None, str | None]:
    """
    Fetch abstract from arXiv HTML. Only attempted for arxiv.org URLs.
    Falls back to constructing URL from paper_arxiv_id if needed.
    Returns (abstract_text, error_string).
    """
    url = paper_url_abs or ""

    # Gate: only attempt for arXiv URLs
    if "arxiv.org" not in url:
        # Try fallback via paper_arxiv_id
        if paper_arxiv_id:
            url = f"https://arxiv.org/abs/{paper_arxiv_id}"
        else:
            return None, "non_arxiv_url"

    try:
        resp = requests.get(
            url, timeout=ARXIV_FETCH_TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0 (research pipeline)"}
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # arXiv HTML abstract block
        block = soup.find("blockquote", class_="abstract")
        if block:
            abstract = block.get_text(strip=True).removeprefix("Abstract:").strip()
            return abstract, None

        # Fallback: meta description
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            return meta["content"].strip(), None

        return None, "parse_failed"

    except requests.Timeout:
        return None, "timeout"
    except requests.HTTPError as e:
        return None, f"http_{e.response.status_code}"
    except Exception as e:
        return None, str(e)[:80]

# ── 3. repo acquisition — github api size check ───────────────────────────────

def get_repo_size_mb(repo_url: str) -> float | None:
    """Query GitHub API for repo size. Returns MB or None on failure."""
    parsed = urlparse(repo_url)
    if "github.com" not in parsed.netloc:
        return None

    parts = [p for p in parsed.path.strip("/").split("/") if p]
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1].replace(".git", "")

    token = os.getenv("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        resp = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}",
            timeout=10,
            headers=headers,
        )
        if resp.status_code == 200:
            size_kb = resp.json().get("size", 0)
            return round(size_kb / 1024, 2)
        return None
    except Exception:
        return None

# ── 3. repo acquisition — clone ───────────────────────────────────────────────

def clone_repo(repo_url: str, dest: Path) -> dict:
    """
    Clone repo with --depth=1. Returns status dict.
    Handles: subtree URLs, timeouts, not_found, private.
    """
    # Sub-tree URL check
    if "/tree/" in repo_url:
        return {"clone_success": False, "clone_error_type": "subtree_url"}

    if dest.exists() and any(dest.iterdir()):
        return {"clone_success": True, "clone_error_type": None, "already_cloned": True}

    dest.mkdir(parents=True, exist_ok=True)
    cmd = ["git", "clone", "--depth=1", "--quiet", repo_url, str(dest)]

    try:
        subprocess.run(cmd, timeout=CLONE_TIMEOUT, check=True, capture_output=True)
        return {"clone_success": True, "clone_error_type": None}

    except subprocess.TimeoutExpired:
        _cleanup(dest)
        return {"clone_success": False, "clone_error_type": "timeout"}

    except subprocess.CalledProcessError as e:
        _cleanup(dest)
        stderr = e.stderr.decode("utf-8", errors="ignore")
        if "Repository not found" in stderr or "does not exist" in stderr or "not found" in stderr.lower():
            error_type = "not_found"
        elif any(w in stderr.lower() for w in ["authentication", "access denied", "could not read"]):
            error_type = "private"
        else:
            error_type = "unknown"
        return {"clone_success": False, "clone_error_type": error_type}

    except Exception as e:
        _cleanup(dest)
        return {"clone_success": False, "clone_error_type": str(e)[:60]}

def _cleanup(path: Path):
    if path.exists():
        import shutil
        shutil.rmtree(path, ignore_errors=True)

# ── 4. repo pre-check ─────────────────────────────────────────────────────────

def precheck_repo(clone_dir: Path, cfg: dict) -> dict:
    """Count executable code files and check for README. Two-tiered sparse check."""
    exe_exts = set(cfg.get("executable_code_extensions", []))
    readme_names = set(cfg.get("repo_thresholds", {}).get("readme_filenames", ["README.md"]))

    executable_count = 0
    has_readme = False

    for f in clone_dir.rglob("*"):
        if not f.is_file():
            continue
        # Skip .git internals
        if ".git" in f.parts:
            continue
        if f.suffix in exe_exts:
            executable_count += 1
        if f.name in readme_names:
            has_readme = True

    return {
        "executable_code_file_count": executable_count,
        "repo_has_readme": has_readme,
        "repo_no_executable_code": executable_count == 0,
        "repo_too_sparse": 0 < executable_count < SPARSE_THRESHOLD,
    }

# ── 5. process single pair ────────────────────────────────────────────────────

def process_pair(entry: dict, cfg: dict, idx: int) -> PairRecord:
    paper_url_abs = entry.get("paper_url_abs") or ""
    paper_arxiv_id = entry.get("paper_arxiv_id") or None
    paper_title = entry.get("paper_title") or ""
    repo_url = entry.get("repo_url") or ""

    # Stable identifier for directory naming
    safe_id = re.sub(r"[^a-zA-Z0-9_\-]", "_", paper_arxiv_id or f"pair_{idx:04d}")
    repo_dir = REPOS_DIR / safe_id

    record = PairRecord(
        paper_id=paper_arxiv_id or f"pair_{idx:04d}",
        paper_title=paper_title,
        paper_arxiv_id=paper_arxiv_id,
        repo_url=repo_url,
        is_official=entry.get("is_official"),
        mentioned_in_paper=entry.get("mentioned_in_paper"),
        mentioned_in_github=entry.get("mentioned_in_github"),
    )

    # ── Level 1: title extraction ──
    hints = extract_title_hints(paper_title, cfg)
    semantics = PaperSemantics(**hints, source="title_extraction")

    # ── Level 2: arXiv abstract ──
    abstract, fetch_error = fetch_arxiv_abstract(paper_url_abs, paper_arxiv_id)
    if abstract:
        semantics.abstract = abstract
        # Frequency-based keyword extraction from abstract
        from collections import Counter
        stopwords = set(cfg.get("stopwords", []))
        kw_tokens = [
            w.lower() for w in re.findall(r"[a-zA-Z]{4,}", abstract)
            if w.lower() not in stopwords
        ]
        semantics.keywords = [w for w, _ in Counter(kw_tokens).most_common(10)]

        # Abstract fallback: fill any hints still None from title
        hints_dict = {"task_hint": semantics.task_hint,
                      "method_hint": semantics.method_hint,
                      "domain_hint": semantics.domain_hint}
        updated_hints, enriched = enrich_hints_from_abstract(hints_dict, abstract, cfg)
        semantics.task_hint = updated_hints["task_hint"]
        semantics.method_hint = updated_hints["method_hint"]
        semantics.domain_hint = updated_hints["domain_hint"]

        semantics.source = "title_extraction+arxiv_html+abstract_enriched" if enriched else "title_extraction+arxiv_html"
        record.paper_fetch_success = True
    else:
        record.paper_fetch_success = False
        record.paper_fetch_error = fetch_error

    record.paper_semantics = semantics

    # ── Repo size check ──
    size_mb = get_repo_size_mb(repo_url)
    record.repo_size_mb = size_mb
    if size_mb and size_mb > LARGE_REPO_MB:
        record.repo_too_large = True
        return record  # skip clone

    # ── Clone ──
    clone_result = clone_repo(repo_url, repo_dir)
    record.clone_success = clone_result["clone_success"]
    record.clone_error_type = clone_result.get("clone_error_type")

    if not record.clone_success:
        return record

    # ── Pre-check ──
    check = precheck_repo(repo_dir, cfg)
    record.repo_no_executable_code = check["repo_no_executable_code"]
    record.repo_too_sparse = check["repo_too_sparse"]
    record.executable_code_file_count = check["executable_code_file_count"]
    record.repo_has_readme = check["repo_has_readme"]

    return record

# ── main ──────────────────────────────────────────────────────────────────────

def main(seed: int = RANDOM_SEED, output_path: Path = OUTPUT_DIR / "pairs.jsonl",
         exclude_path: str | None = None, pair_delay: float = 0.3):
    cfg = load_config()

    # Load exclusion list if provided
    exclude_ids: set[str] = set()
    if exclude_path and Path(exclude_path).exists():
        with open(exclude_path) as f:
            exclude_ids = set(x for x in json.load(f) if x)
        print(f"Excluding {len(exclude_ids)} already-sampled pairs")

    print("Loading dataset...")
    ds = load_dataset("pwc-archive/links-between-paper-and-code", split="train")
    print(f"Total entries: {len(ds):,}")

    print(f"\nSampling {SAMPLE_OFFICIAL} official + {SAMPLE_NONOFFICIAL} non-official (seed={seed})...")
    pairs = sample_pairs(ds, SAMPLE_OFFICIAL, SAMPLE_NONOFFICIAL, seed, exclude_ids)

    # Save sample IDs for reproducibility
    ids_path = output_path.parent / f"sample_ids_{output_path.stem}.json"
    sample_ids = [e.get("paper_arxiv_id") or e.get("paper_title", "")[:60] for e in pairs]
    with open(ids_path, "w") as f:
        json.dump(sample_ids, f, indent=2)

    print(f"Processing {len(pairs)} pairs...\n")

    stats = {
        "total": len(pairs), "paper_fetch_ok": 0, "clone_ok": 0,
        "clone_failed": 0, "subtree_url": 0, "too_large": 0,
        "no_executable_code": 0, "too_sparse": 0, "clone_errors": {}
    }

    with open(output_path, "w") as out_f:
        for idx, entry in enumerate(tqdm(pairs, desc="Phase 1")):
            time.sleep(pair_delay)  # polite delay for API calls
            try:
                record = process_pair(entry, cfg, idx)
            except Exception as e:
                tqdm.write(f"  [ERROR] pair {idx}: {e}")
                continue

            # Write to JSONL immediately
            out_f.write(record.model_dump_json() + "\n")
            out_f.flush()

            # Accumulate stats
            if record.paper_fetch_success:
                stats["paper_fetch_ok"] += 1
            if record.clone_success:
                stats["clone_ok"] += 1
            elif record.repo_too_large:
                stats["too_large"] += 1
            else:
                stats["clone_failed"] += 1
                err = record.clone_error_type or "unknown"
                stats["clone_errors"][err] = stats["clone_errors"].get(err, 0) + 1
                if err == "subtree_url":
                    stats["subtree_url"] += 1
            if record.repo_no_executable_code:
                stats["no_executable_code"] += 1
            if record.repo_too_sparse:
                stats["too_sparse"] += 1

    # ── Summary ──
    print(f"\n{'='*55}")
    print("  PHASE 1 RESULTS")
    print(f"{'='*55}")
    print(f"  Pairs processed:         {stats['total']}")
    print(f"  Paper fetch success:     {stats['paper_fetch_ok']} / {stats['total']}")
    print(f"  Clone success:           {stats['clone_ok']} / {stats['total']}")
    print(f"  Clone failed:            {stats['clone_failed']} / {stats['total']}")
    if stats["clone_errors"]:
        for err_type, count in stats["clone_errors"].items():
            print(f"    └─ {err_type}: {count}")
    print(f"  Too large (skipped):     {stats['too_large']}")
    print(f"  No executable code:      {stats['no_executable_code']}")
    print(f"  Too sparse (< {SPARSE_THRESHOLD} files):  {stats['too_sparse']}")
    print(f"\n  Output: {output_path}")
    print(f"  Repos:  {REPOS_DIR}")

    # Save stats
    stats_path = output_path.parent / f"stats_{output_path.stem}.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)

if __name__ == "__main__":
    os.chdir(ROOT)

    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=RANDOM_SEED,
                        help="Random seed for sampling")
    parser.add_argument("--output", type=str, default=str(OUTPUT_DIR / "pairs.jsonl"),
                        help="Output JSONL file path")
    parser.add_argument("--exclude", type=str, default=None,
                        help="Path to a previous sample_ids.json to exclude from sampling")
    parser.add_argument("--pair-delay", type=float, default=0.3,
                        help="Delay in seconds between pairs (default: 0.3)")
    args = parser.parse_args()

    main(seed=args.seed, output_path=Path(args.output), exclude_path=args.exclude,
         pair_delay=args.pair_delay)
