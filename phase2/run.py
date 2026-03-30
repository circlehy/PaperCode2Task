"""
Phase 2 — Rule-based Alignment Scoring

Reads output/phase1/pairs_all.jsonl.
For each usable pair (clone_success=True, not repo_no_executable_code, not repo_too_large):
  Category A: explicit-link signals (cap 0.45)
  Category B: surface/name matching signals (cap 0.25)
  Category C: semantic consistency, rule-based only (cap 0.30, partial — LLM deferred to Phase 3)
  score = clamp(min(A_raw, 0.45) + min(B_raw, 0.25) + min(C_raw, 0.30), 0, 1)
  level: ≥0.75 STRONG, 0.45–0.74 MEDIUM, <0.45 WEAK
  confidence: deferred to Phase 3

Skipped pairs (too_large, clone failed, no_executable_code) pass through unchanged.
repo_too_sparse pairs are scored but will be forced LOW confidence in Phase 3.

Input:  output/phase1/pairs_all.jsonl
Output: output/phase2/pairs_phase2.jsonl
        output/phase2/stats_phase2.json

Run:
  python phase2/run.py [--input PATH] [--output PATH]
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml
from tqdm import tqdm

ROOT = Path(__file__).parent.parent
CONFIG_PATH = ROOT / "configs" / "patterns.yaml"
INPUT_PATH  = ROOT / "output" / "phase1" / "pairs_all.jsonl"
OUTPUT_DIR  = ROOT / "output" / "phase2"
REPOS_DIR   = ROOT / "output" / "repos"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT / "phase0"))
from schema import AlignmentResult

# ── constants ─────────────────────────────────────────────────────────────────

CAT_A_CAP = 0.45
CAT_B_CAP = 0.25
CAT_C_CAP = 0.30

README_READ_LIMIT = 20_000   # chars
TITLE_MATCH_RATIO = 0.60     # fraction of title tokens that must appear in README
TITLE_KW_IN_README = 3       # min title tokens for "readme_has_title_keywords" signal
STRUCTURE_DIR_MIN  = 2       # min matching dirs for "repo_has_structure" signal

# ── helpers ───────────────────────────────────────────────────────────────────

def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def repo_dir_from_id(paper_id: str) -> Path:
    """Reconstruct local clone path from paper_id (mirrors Phase 1 naming logic)."""
    safe_id = re.sub(r"[^a-zA-Z0-9_\-]", "_", paper_id)
    return REPOS_DIR / safe_id


def read_readme(repo_dir: Path, readme_names: list[str]) -> str:
    """Return README text (up to README_READ_LIMIT chars), or '' if not found."""
    for name in readme_names:
        path = repo_dir / name
        if path.exists():
            try:
                return path.read_text(errors="ignore")[:README_READ_LIMIT]
            except Exception:
                pass
    return ""


def title_tokens(title: str, stopwords: set[str]) -> list[str]:
    """Lowercase title, strip stopwords, return non-trivial word tokens."""
    words = re.findall(r"[a-zA-Z0-9]+", title.lower())
    return [w for w in words if w not in stopwords and len(w) > 2]


def repo_name_tokens(repo_url: str) -> list[str]:
    """Parse repo name from URL, split on - and _, return lowercase tokens."""
    parts = repo_url.rstrip("/").split("/")
    name = parts[-1].replace(".git", "").lower() if parts else ""
    return [t for t in re.split(r"[-_]", name) if t]


def top_level_dirs(repo_dir: Path) -> set[str]:
    """Return lowercase set of top-level directory names (excluding .git)."""
    try:
        return {d.name.lower() for d in repo_dir.iterdir()
                if d.is_dir() and d.name != ".git"}
    except Exception:
        return set()


def is_usable(record: dict) -> bool:
    """Return True if Phase 2 should score this pair."""
    return (
        record.get("clone_success") is True
        and not record.get("repo_no_executable_code")
        and not record.get("repo_too_large")
    )

# ── alignment computation ─────────────────────────────────────────────────────

def compute_alignment(record: dict, cfg: dict) -> AlignmentResult:
    """
    Compute rule-based alignment for one pair. Returns populated AlignmentResult.
    LLM signals (Phase 3) are left at 0.
    """
    stopwords     = set(cfg.get("stopwords", []))
    readme_names  = cfg.get("repo_thresholds", {}).get("readme_filenames", ["README.md"])
    struct_dirs   = set(cfg.get("structure_pattern_directories", []))
    dataset_kws   = [k.lower() for k in cfg.get("dataset_keywords", [])]

    repo_dir     = repo_dir_from_id(record.get("paper_id") or "")
    readme       = read_readme(repo_dir, readme_names)
    readme_lower = readme.lower()

    semantics   = record.get("paper_semantics") or {}
    method_hint = (semantics.get("method_hint") or "").lower()
    task_hint   = (semantics.get("task_hint")   or "").lower()
    arxiv_id    = record.get("paper_arxiv_id")  or ""
    abstract_kws  = {k.lower() for k in semantics.get("keywords", [])}
    abstract_text = (semantics.get("abstract") or "").lower()

    t_tokens    = title_tokens(record.get("paper_title") or "", stopwords)
    repo_tokens = repo_name_tokens(record.get("repo_url") or "")

    signals = []
    cat_a_raw = cat_b_raw = cat_c_raw = 0.0

    # ── Category A: Explicit-link signals ────────────────────────────────────

    if record.get("is_official"):
        signals.append("is_official")
        cat_a_raw += 0.20

    if record.get("mentioned_in_paper"):
        signals.append("mentioned_in_paper")
        cat_a_raw += 0.15

    if record.get("mentioned_in_github"):
        signals.append("mentioned_in_github")
        cat_a_raw += 0.05

    if arxiv_id and arxiv_id in readme:
        signals.append("readme_has_arxiv_id")
        cat_a_raw += 0.05

    if t_tokens:
        in_readme = sum(1 for t in t_tokens if t in readme_lower)
        if in_readme / len(t_tokens) >= TITLE_MATCH_RATIO:
            signals.append("readme_has_title")
            cat_a_raw += 0.05

    # ── Category B: Surface / name matching ──────────────────────────────────

    if method_hint:
        method_tokens    = set(re.split(r"[\s\-_]+", method_hint))
        method_collapsed = re.sub(r"[\s\-_]", "", method_hint)
        repo_collapsed   = "".join(repo_tokens)
        if (method_tokens & set(repo_tokens)) or (method_collapsed in repo_collapsed):
            signals.append("repo_name_matches_method")
            cat_b_raw += 0.10

    if t_tokens and repo_tokens and (set(t_tokens) & set(repo_tokens)):
        signals.append("repo_name_overlaps_title")
        cat_b_raw += 0.05

    if method_hint and method_hint in readme_lower:
        signals.append("readme_mentions_method")
        cat_b_raw += 0.05

    if t_tokens and sum(1 for t in t_tokens if t in readme_lower) >= TITLE_KW_IN_README:
        signals.append("readme_has_title_keywords")
        cat_b_raw += 0.05

    # ── Category C: Semantic consistency (rule-based only) ───────────────────

    tl_dirs = top_level_dirs(repo_dir)
    if len(tl_dirs & struct_dirs) >= STRUCTURE_DIR_MIN:
        signals.append("repo_has_structure")
        cat_c_raw += 0.05

    for dk in dataset_kws:
        if dk in readme_lower and (dk in abstract_kws or dk in abstract_text):
            signals.append("dataset_keyword_overlap")
            cat_c_raw += 0.05
            break  # signal fires at most once

    if task_hint and task_hint in readme_lower:
        signals.append("task_consistency")
        cat_c_raw += 0.10

    # ── Final score and level ─────────────────────────────────────────────────

    score = round(
        min(min(cat_a_raw, CAT_A_CAP) + min(cat_b_raw, CAT_B_CAP) + min(cat_c_raw, CAT_C_CAP), 1.0),
        4
    )

    if score >= 0.75:
        level = "STRONG"
    elif score >= 0.45:
        level = "MEDIUM"
    else:
        level = "WEAK"

    return AlignmentResult(
        score=score,
        level=level,
        # confidence deferred to Phase 3
        signals_fired=signals,
        signal_count=len(signals),
        llm_called=False,
    )

# ── main ──────────────────────────────────────────────────────────────────────

def main(input_path: Path = INPUT_PATH, output_path: Path = OUTPUT_DIR / "pairs_phase2.jsonl"):
    cfg = load_config()
    readme_names = cfg.get("repo_thresholds", {}).get("readme_filenames", ["README.md"])

    records = []
    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    print(f"Loaded {len(records)} pairs from {input_path}")

    stats = {
        "total": len(records),
        "scored": 0,
        "skipped_no_clone": 0,
        "skipped_no_code": 0,
        "skipped_too_large": 0,
        "sparse_scored": 0,
        "levels": {"STRONG": 0, "MEDIUM": 0, "WEAK": 0},
        "signals_distribution": {},
    }

    with open(output_path, "w") as out_f:
        for record in tqdm(records, desc="Phase 2"):
            if not record.get("clone_success"):
                stats["skipped_no_clone"] += 1
            elif record.get("repo_no_executable_code"):
                stats["skipped_no_code"] += 1
            elif record.get("repo_too_large"):
                stats["skipped_too_large"] += 1
            else:
                alignment = compute_alignment(record, cfg)
                record["alignment"] = json.loads(alignment.model_dump_json())

                stats["scored"] += 1
                stats["levels"][alignment.level] += 1
                if record.get("repo_too_sparse"):
                    stats["sparse_scored"] += 1
                for sig in alignment.signals_fired:
                    stats["signals_distribution"][sig] = stats["signals_distribution"].get(sig, 0) + 1

            out_f.write(json.dumps(record) + "\n")

    # ── Summary ──────────────────────────────────────────────────────────────

    scored = stats["scored"]
    print(f"\n{'='*55}")
    print("  PHASE 2 RESULTS")
    print(f"{'='*55}")
    print(f"  Total pairs:             {stats['total']}")
    print(f"  Scored:                  {scored}")
    print(f"  Skipped (no clone):      {stats['skipped_no_clone']}")
    print(f"  Skipped (no code):       {stats['skipped_no_code']}")
    print(f"  Skipped (too large):     {stats['skipped_too_large']}")
    print(f"  Of scored — sparse:      {stats['sparse_scored']}")
    print(f"\n  Level distribution:")
    for level in ("STRONG", "MEDIUM", "WEAK"):
        n = stats["levels"][level]
        pct = f"{n/scored*100:.0f}%" if scored else "—"
        print(f"    {level:<8} {n:>3}  ({pct})")
    print(f"\n  Signal firing counts:")
    for sig, count in sorted(stats["signals_distribution"].items(), key=lambda x: -x[1]):
        print(f"    {sig:<35} {count:>3}")
    print(f"\n  Output: {output_path}")

    stats_path = output_path.parent / f"stats_{output_path.stem}.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)


if __name__ == "__main__":
    import os
    os.chdir(ROOT)

    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default=str(INPUT_PATH),
                        help="Input JSONL from Phase 1")
    parser.add_argument("--output", default=str(OUTPUT_DIR / "pairs_phase2.jsonl"),
                        help="Output JSONL with alignment fields populated")
    args = parser.parse_args()

    main(input_path=Path(args.input), output_path=Path(args.output))
