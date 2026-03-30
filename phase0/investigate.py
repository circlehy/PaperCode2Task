"""
Phase 0 — Investigation Script

Validates assumptions about:
1. PWC dataset fields and data quality
2. arXiv abstract fetching
3. Repo cloning and structure
4. Pre-check threshold calibration (sparse / large)

Run:
    python phase0/investigate.py
"""

import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from collections import defaultdict, Counter

import requests
import yaml
from bs4 import BeautifulSoup
from datasets import load_dataset

OUTPUT_DIR = Path("output/phase0")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_PATH = Path("configs/patterns.yaml")

SAMPLE_SIZE = 10      # entries to inspect from dataset
PROBE_SIZE = 5        # entries to do live paper + repo probing on
CLONE_TIMEOUT = 60    # seconds

# ── helpers ──────────────────────────────────────────────────────────────────

def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def subsection(title: str):
    print(f"\n  ── {title} ──")

# ── 1. Dataset inspection ─────────────────────────────────────────────────────

def inspect_dataset(cfg: dict) -> list[dict]:
    section("1. DATASET INSPECTION")

    print("\n  Loading pwc-archive/links-between-paper-and-code ...")
    ds = load_dataset("pwc-archive/links-between-paper-and-code", split="train")
    total = len(ds)
    print(f"  Total entries: {total:,}")

    # Field names
    subsection("Fields")
    for col in ds.column_names:
        print(f"    {col}")

    # Sample entries
    sample = ds.select(range(SAMPLE_SIZE))

    subsection(f"Sample ({SAMPLE_SIZE} entries)")
    for i, entry in enumerate(sample):
        print(f"\n  [{i}] {entry.get('paper_title', 'N/A')[:80]}")
        for k, v in entry.items():
            display = str(v)[:120] if v is not None else "None"
            print(f"      {k}: {display}")

    # Null / missing rate for key fields
    subsection("Null rates for key fields (first 1000 entries)")
    key_fields = ["paper_title", "paper_url_abs", "repo_url", "is_official",
                  "mentioned_in_paper", "tasks", "methods", "area"]
    check_size = min(1000, total)
    check_sample = ds.select(range(check_size))

    null_counts = defaultdict(int)
    for entry in check_sample:
        for field in key_fields:
            val = entry.get(field)
            if val is None or val == "" or val == [] or val == {}:
                null_counts[field] += 1

    for field in key_fields:
        rate = null_counts[field] / check_size * 100
        status = "⚠️ " if rate > 20 else "✅"
        print(f"    {status} {field}: {null_counts[field]}/{check_size} null ({rate:.1f}%)")

    # is_official distribution
    subsection("is_official distribution (first 1000 entries)")
    official_counts = Counter(str(entry.get("is_official")) for entry in check_sample)
    for k, v in official_counts.most_common():
        print(f"    {k}: {v} ({v/check_size*100:.1f}%)")

    # Save sample to output
    sample_path = OUTPUT_DIR / "dataset_sample.json"
    with open(sample_path, "w") as f:
        json.dump([dict(e) for e in sample], f, indent=2, default=str)
    print(f"\n  Saved sample to {sample_path}")

    return [dict(e) for e in ds.select(range(PROBE_SIZE))]


# ── 2. Paper fetch probing ────────────────────────────────────────────────────

def probe_paper_fetch(entries: list[dict]):
    section("2. PAPER FETCH PROBING (arXiv HTML)")

    results = []
    for i, entry in enumerate(entries):
        url = entry.get("paper_url_abs")
        title = entry.get("paper_title", "N/A")[:60]
        print(f"\n  [{i}] {title}")
        print(f"      paper_url_abs: {url}")

        if not url:
            print("      ⚠️  No paper_url_abs — Level 1 fallback only")
            results.append({"index": i, "success": False, "reason": "no_url"})
            continue

        try:
            resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            # Try arXiv abstract extraction
            abstract = None
            # arXiv HTML format: <blockquote class="abstract">
            block = soup.find("blockquote", class_="abstract")
            if block:
                abstract = block.get_text(strip=True).removeprefix("Abstract:").strip()

            # Fallback: meta description
            if not abstract:
                meta = soup.find("meta", attrs={"name": "description"})
                if meta:
                    abstract = meta.get("content", "").strip()

            if abstract:
                print(f"      ✅ Abstract fetched ({len(abstract)} chars)")
                print(f"      Preview: {abstract[:150]}...")
                results.append({"index": i, "success": True, "abstract_len": len(abstract)})
            else:
                print(f"      ⚠️  Page fetched but abstract not found (HTTP {resp.status_code})")
                results.append({"index": i, "success": False, "reason": "parse_failed", "status": resp.status_code})

        except requests.Timeout:
            print(f"      ❌ Timeout")
            results.append({"index": i, "success": False, "reason": "timeout"})
        except requests.HTTPError as e:
            print(f"      ❌ HTTP error: {e}")
            results.append({"index": i, "success": False, "reason": f"http_{e.response.status_code}"})
        except Exception as e:
            print(f"      ❌ Error: {e}")
            results.append({"index": i, "success": False, "reason": str(e)})

        time.sleep(0.5)  # polite delay

    success_rate = sum(1 for r in results if r["success"]) / len(results) * 100
    print(f"\n  Paper fetch success rate: {success_rate:.0f}% ({sum(1 for r in results if r['success'])}/{len(results)})")

    fetch_path = OUTPUT_DIR / "paper_fetch_probe.json"
    with open(fetch_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Saved results to {fetch_path}")


# ── 3. Repo probing ───────────────────────────────────────────────────────────

def probe_repos(entries: list[dict], cfg: dict):
    section("3. REPO PROBING (clone + structure)")

    code_exts = set(cfg["code_file_extensions"])
    sparse_threshold = cfg["repo_thresholds"]["sparse_file_count"]
    readme_names = set(cfg["repo_thresholds"]["readme_filenames"])

    results = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, entry in enumerate(entries):
            repo_url = entry.get("repo_url")
            title = entry.get("paper_title", "N/A")[:60]
            print(f"\n  [{i}] {title}")
            print(f"      repo_url: {repo_url}")

            if not repo_url:
                print("      ⚠️  No repo_url")
                results.append({"index": i, "success": False, "reason": "no_url"})
                continue

            clone_dir = Path(tmpdir) / f"repo_{i}"
            clone_cmd = ["git", "clone", "--depth=1", "--quiet", repo_url, str(clone_dir)]

            try:
                subprocess.run(clone_cmd, timeout=CLONE_TIMEOUT, check=True,
                               capture_output=True)

                # Collect file stats
                all_files = list(clone_dir.rglob("*"))
                files_only = [f for f in all_files if f.is_file()]
                code_files = [f for f in files_only if f.suffix in code_exts]
                has_readme = any(f.name in readme_names for f in files_only)

                # Top-level directory structure
                top_dirs = sorted(set(
                    f.relative_to(clone_dir).parts[0]
                    for f in all_files
                    if len(f.relative_to(clone_dir).parts) > 1
                ))[:10]

                # File extension breakdown
                ext_counts = Counter(f.suffix for f in files_only if f.suffix)
                top_exts = ext_counts.most_common(8)

                is_sparse = len(code_files) < sparse_threshold

                print(f"      ✅ Cloned successfully")
                print(f"      Total files: {len(files_only)}")
                print(f"      Code files:  {len(code_files)} {'⚠️  SPARSE' if is_sparse else ''}")
                print(f"      Has README:  {has_readme}")
                print(f"      Top dirs:    {top_dirs}")
                print(f"      Extensions:  {top_exts}")

                results.append({
                    "index": i,
                    "success": True,
                    "total_files": len(files_only),
                    "code_file_count": len(code_files),
                    "has_readme": has_readme,
                    "is_sparse": is_sparse,
                    "top_dirs": top_dirs,
                    "extension_counts": dict(top_exts),
                })

            except subprocess.TimeoutExpired:
                print(f"      ❌ Clone timeout (>{CLONE_TIMEOUT}s)")
                results.append({"index": i, "success": False, "reason": "timeout"})
            except subprocess.CalledProcessError as e:
                stderr = e.stderr.decode("utf-8", errors="ignore").strip()
                reason = "not_found" if "Repository not found" in stderr or "does not exist" in stderr else \
                         "private" if "Authentication" in stderr or "access" in stderr.lower() else \
                         "unknown"
                print(f"      ❌ Clone failed: {reason} — {stderr[:100]}")
                results.append({"index": i, "success": False, "reason": reason})
            except Exception as e:
                print(f"      ❌ Error: {e}")
                results.append({"index": i, "success": False, "reason": str(e)})

    success_rate = sum(1 for r in results if r["success"]) / len(results) * 100
    print(f"\n  Clone success rate: {success_rate:.0f}% ({sum(1 for r in results if r['success'])}/{len(results)})")
    sparse_count = sum(1 for r in results if r.get("is_sparse"))
    print(f"  Sparse repos (< {sparse_threshold} code files): {sparse_count}/{sum(1 for r in results if r['success'])}")

    repo_path = OUTPUT_DIR / "repo_probe.json"
    with open(repo_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Saved results to {repo_path}")


# ── 4. Schema validation ──────────────────────────────────────────────────────

def validate_schema():
    section("4. SCHEMA VALIDATION")
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from schema import PairRecord, PaperSemantics, AlignmentResult
        # Instantiate an empty record to confirm schema works
        record = PairRecord(
            paper_id="test_001",
            paper_title="Test Paper",
            repo_url="https://github.com/example/repo",
            is_official=True,
            paper_semantics=PaperSemantics(
                task_hint="image classification",
                method_hint="CNN",
                domain_hint="computer vision",
                source="pwc_metadata"
            )
        )
        print(f"\n  ✅ Schema instantiates correctly")
        print(f"  Fields: {list(record.model_fields.keys())}")
        schema_path = OUTPUT_DIR / "schema_example.json"
        with open(schema_path, "w") as f:
            f.write(record.model_dump_json(indent=2))
        print(f"  Saved example record to {schema_path}")
    except Exception as e:
        print(f"\n  ❌ Schema error: {e}")


# ── 5. Summary ────────────────────────────────────────────────────────────────

def print_summary():
    section("5. PHASE 0 SUMMARY")
    print("""
  What to check before proceeding to Phase 1:

  Dataset fields
  ─────────────
  □ Verify which fields are consistently populated (check null rates above)
  □ Confirm 'tasks', 'methods', 'area' have usable string values for Level 1 hints
  □ Confirm 'paper_url_abs' is consistently an arXiv URL

  Paper fetching
  ──────────────
  □ Check paper fetch success rate (should be > 80% on clean sample)
  □ If abstract extraction fails often → may need to adjust HTML parser

  Repo cloning
  ────────────
  □ Check clone success rate (deleted/private repos are expected)
  □ Check how many repos are sparse — calibrate threshold if needed
  □ Review top-level directory structures to validate component detection assumptions

  Schema
  ──────
  □ Review output/phase0/schema_example.json — add or remove fields as needed
  □ This schema is the contract all pipeline phases write to

  Config
  ──────
  □ Review configs/patterns.yaml — adjust filename patterns and keyword lists
    based on what you see in real repos
""")


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.chdir(Path(__file__).parent.parent)  # run from project root

    cfg = load_config()
    probe_entries = inspect_dataset(cfg)
    probe_paper_fetch(probe_entries)
    probe_repos(probe_entries, cfg)
    validate_schema()
    print_summary()
