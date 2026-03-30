"""
Overnight Pipeline Runner
=========================

Runs batches of 50 pairs (25 official + 25 non-official) through the full
pipeline (Phases 1–4) sequentially, accumulating results with no overlap.
Designed to run unattended overnight.

State is checkpointed after every batch: safe to interrupt with Ctrl+C
and resume with --resume. Already-completed batches are skipped.

Constraints handled
-------------------
GitHub API:
  With GITHUB_TOKEN set in .env: 5,000 req/hour — no rate limit concern.
  Without token (unauthenticated): 60 req/hour. The code handles 403
  gracefully: size check is skipped and clone proceeds regardless.
  Use --pair-delay 60 for strict unauthenticated compliance (very slow).
  With auth, --pair-delay 0 is fine (default 0.0; built-in 0.3s remains).

Disk space:
  Each cloned repo averages ~8 MB. 50 repos per batch ≈ 400 MB.
  The script estimates projected disk usage before starting and warns if
  it exceeds --max-disk-gb (default 10 GB).

LLM cost:
  gpt-4o-mini at ~800 input tokens/pair ≈ $0.00015/pair.
  50 pairs × 15 batches ≈ $0.11. Existing pairs are served from cache.

Usage
-----
  python run_overnight.py --batches 15
  python run_overnight.py --batches 15 --resume
  python run_overnight.py --batches 5 --pair-delay 60  # strict API limit

Output
------
  output/overnight/state.json             checkpoint: completed seeds, stats
  output/overnight/all_ids.json           growing exclusion list (all sampled IDs)
  output/overnight/batch_{seed}_p1.jsonl  Phase 1 output per batch
  output/overnight/batch_{seed}_p2.jsonl  Phase 2 output per batch
  output/overnight/batch_{seed}_p3.jsonl  Phase 3 output per batch
  output/overnight/batch_{seed}_p4.jsonl  Phase 4 output (final) per batch
  output/overnight/combined_p4.jsonl      all completed batches combined
  output/overnight/run.log               timestamped progress log
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT        = Path(__file__).parent
OVERNIGHT   = ROOT / "output" / "overnight"
STATE_FILE  = OVERNIGHT / "state.json"
IDS_FILE    = OVERNIGHT / "all_ids.json"
COMBINED    = OVERNIGHT / "combined_p4.jsonl"
LOG_FILE    = OVERNIGHT / "run.log"

OVERNIGHT.mkdir(parents=True, exist_ok=True)

CONDA_ENV   = "paper2env"
BATCH_SIZE  = 50          # pairs per batch (25 official + 25 non-official)
DISK_WARN_GB = 10.0

# ── helpers ───────────────────────────────────────────────────────────────────

def log(msg: str, also_print: bool = True):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    if also_print:
        print(line)


def run_cmd(cmd: list[str], label: str) -> bool:
    """Run a subprocess command. Returns True on success."""
    log(f"  → {label}")
    start = time.time()
    result = subprocess.run(
        ["conda", "run", "-n", CONDA_ENV] + cmd,
        capture_output=True, text=True,
        cwd=str(ROOT),
    )
    elapsed = time.time() - start
    if result.returncode != 0:
        log(f"  ✗ FAILED ({elapsed:.0f}s): {result.stderr[-300:]}")
        return False
    # Print last few lines of stdout for progress visibility
    lines = [l for l in result.stdout.splitlines() if l.strip()]
    for l in lines[-6:]:
        log(f"      {l}", also_print=True)
    log(f"  ✓ done ({elapsed:.0f}s)")
    return True


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"completed_seeds": [], "batches_done": 0, "pairs_added": 0,
            "started_at": None, "last_seed": 44}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def load_ids() -> list:
    if IDS_FILE.exists():
        return json.loads(IDS_FILE.read_text())
    return []


def save_ids(ids: list):
    IDS_FILE.write_text(json.dumps(ids, indent=2))


def append_to_combined(batch_p4: Path):
    """Append all lines from a batch Phase 4 file to the combined output."""
    with open(COMBINED, "a") as out_f:
        with open(batch_p4) as in_f:
            for line in in_f:
                line = line.strip()
                if line:
                    out_f.write(line + "\n")


def estimate_disk_gb(n_batches: int) -> float:
    """Rough estimate: 400 MB per batch of 50 repos at ~8 MB median."""
    return n_batches * 0.4


def count_repos_on_disk() -> int:
    repos_dir = ROOT / "output" / "repos"
    if not repos_dir.exists():
        return 0
    return sum(1 for d in repos_dir.iterdir() if d.is_dir())


def collect_existing_ids() -> list[str]:
    """
    Gather all previously sampled paper IDs from existing batch ID files.
    Also includes any IDs already in the overnight IDs file.
    """
    all_ids: set[str] = set()

    # Original 3 batches
    for fname in [
        "output/phase1/sample_ids.json",
        "output/phase1/sample_ids_pairs_batch2.json",
        "output/phase1/sample_ids_pairs_batch3.json",
        "output/phase1/sample_ids_batches12.json",
    ]:
        p = ROOT / fname
        if p.exists():
            ids = json.loads(p.read_text())
            all_ids.update(x for x in ids if x)

    # Overnight IDs file (from previous runs)
    for x in load_ids():
        if x:
            all_ids.add(x)

    return list(all_ids)


def next_seed(state: dict) -> int:
    """Return next seed: one above the last used seed."""
    if state["completed_seeds"]:
        return max(state["completed_seeds"]) + 1
    return state.get("last_seed", 44) + 1

# ── single batch ──────────────────────────────────────────────────────────────

def run_batch(seed: int, pair_delay: float) -> tuple[bool, int]:
    """
    Run one batch (seed) through Phases 1–4.
    Returns (success, n_pairs_added).
    """
    p1 = OVERNIGHT / f"batch_{seed}_p1.jsonl"
    p2 = OVERNIGHT / f"batch_{seed}_p2.jsonl"
    p3 = OVERNIGHT / f"batch_{seed}_p3.jsonl"
    p4 = OVERNIGHT / f"batch_{seed}_p4.jsonl"

    log(f"\n{'='*60}")
    log(f"BATCH seed={seed}")
    log(f"{'='*60}")

    # ── Phase 1 ──
    phase1_cmd = [
        "python", "phase1/run.py",
        "--seed", str(seed),
        "--output", str(p1),
        "--exclude", str(IDS_FILE),
        "--pair-delay", str(pair_delay),
    ]
    if not run_cmd(phase1_cmd, "Phase 1 — ingest + clone"):
        return False, 0

    if not p1.exists() or p1.stat().st_size == 0:
        log("  ✗ Phase 1 produced no output")
        return False, 0

    # Add new IDs to exclusion list immediately after Phase 1
    # so that even if Phase 2-4 fail, these IDs are excluded next time
    # phase1/run.py saves IDs as sample_ids_{stem}.json where stem = p1 file stem
    ids_path = OVERNIGHT / f"sample_ids_{p1.stem}.json"
    if ids_path.exists():
        new_ids = [x for x in json.loads(ids_path.read_text()) if x]
        current_ids = load_ids()
        updated = list(set(current_ids) | set(new_ids))
        save_ids(updated)
        log(f"  IDs file updated: {len(updated)} total excluded")

    # ── Phase 2 ──
    if not run_cmd([
        "python", "phase2/run.py",
        "--input", str(p1), "--output", str(p2),
    ], "Phase 2 — alignment scoring"):
        return False, 0

    # ── Phase 3 ──
    if not run_cmd([
        "python", "phase3/run.py",
        "--input", str(p2), "--output", str(p3),
        "--production",
    ], "Phase 3 — LLM integration"):
        return False, 0

    # ── Phase 4 ──
    if not run_cmd([
        "python", "phase4/run.py",
        "--input", str(p3), "--output", str(p4),
    ], "Phase 4 — component + suitability"):
        return False, 0

    if not p4.exists():
        log("  ✗ Phase 4 produced no output")
        return False, 0

    # Count pairs added (exclude skipped/unscored)
    n_added = sum(1 for line in p4.read_text().splitlines() if line.strip())
    append_to_combined(p4)
    log(f"  ✓ Batch complete — {n_added} records appended to combined output")

    return True, n_added

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Run the PWC pipeline overnight across multiple batches."
    )
    parser.add_argument("--batches",    type=int,   default=10,
                        help="Number of batches to run (default: 10)")
    parser.add_argument("--pair-delay", type=float, default=0.3,
                        help="Delay in seconds between pairs in Phase 1 (default: 0.3). "
                             "With GITHUB_TOKEN in .env, 0.3 is fine. "
                             "Use 60 only if running without a token.")
    parser.add_argument("--max-disk-gb", type=float, default=DISK_WARN_GB,
                        help="Warn and abort if projected disk usage exceeds "
                             "this many GB (default: 10)")
    parser.add_argument("--resume",     action="store_true",
                        help="Resume from checkpoint — skip already-completed batches")
    args = parser.parse_args()

    log(f"\n{'#'*60}")
    log(f"# OVERNIGHT RUN — {args.batches} batches requested")
    log(f"{'#'*60}")

    # ── disk space warning ────────────────────────────────────────────────────
    projected_gb = estimate_disk_gb(args.batches)
    existing_repos = count_repos_on_disk()
    log(f"Existing repos on disk: {existing_repos}")
    log(f"Projected additional disk usage: ~{projected_gb:.1f} GB")
    if projected_gb > args.max_disk_gb:
        log(f"WARNING: projected usage ({projected_gb:.1f} GB) exceeds "
            f"--max-disk-gb ({args.max_disk_gb} GB)")
        ans = input("Continue? [y/N] ").strip().lower()
        if ans != "y":
            log("Aborted by user.")
            sys.exit(0)

    # ── rate limit info ───────────────────────────────────────────────────────
    import os as _os
    has_token = bool(_os.getenv("GITHUB_TOKEN") or
                     (ROOT / ".env").exists() and "GITHUB_TOKEN" in (ROOT / ".env").read_text())
    limit_str = "5000/hour (authenticated)" if has_token else "60/hour (unauthenticated)"
    log(f"Per-pair delay: {args.pair_delay:.1f}s | GitHub API limit: {limit_str}")
    if not has_token and args.pair_delay < 60:
        log("NOTE: no GITHUB_TOKEN found — rate may exceed 60 req/hour. "
            "Size checks skipped on 403; clones still proceed. "
            "Add GITHUB_TOKEN to .env or use --pair-delay 60 for compliance.")

    # ── load / init state ─────────────────────────────────────────────────────
    state = load_state()
    if not args.resume:
        if state["batches_done"] > 0:
            log(f"Found existing state ({state['batches_done']} batches done). "
                f"Use --resume to continue, or delete {STATE_FILE} to start fresh.")
            sys.exit(1)
    else:
        log(f"Resuming: {state['batches_done']} batches already completed, "
            f"seeds used: {state['completed_seeds']}")

    if state["started_at"] is None:
        state["started_at"] = datetime.now().isoformat()

    # ── seed the exclusion list ───────────────────────────────────────────────
    if not IDS_FILE.exists() or not args.resume:
        existing_ids = collect_existing_ids()
        save_ids(existing_ids)
        log(f"Exclusion list initialised: {len(existing_ids)} IDs from existing batches")
    else:
        log(f"Exclusion list loaded: {len(load_ids())} IDs")

    # ── update phase1/run.py to accept --pair-delay if not present ───────────
    # (handled inside the run_batch subprocess call via existing arg support)

    # ── run batches ───────────────────────────────────────────────────────────
    run_start  = time.time()
    seeds_todo = []
    current_seed = next_seed(state)
    for _ in range(args.batches):
        if current_seed not in state["completed_seeds"]:
            seeds_todo.append(current_seed)
        current_seed += 1

    log(f"Seeds to process: {seeds_todo}")
    log("")

    batch_times = []
    for seed in seeds_todo:
        batch_start = time.time()
        ok, n_added = run_batch(seed, args.pair_delay)
        elapsed     = time.time() - batch_start
        batch_times.append(elapsed)

        if ok:
            state["completed_seeds"].append(seed)
            state["batches_done"] += 1
            state["pairs_added"]  += n_added
            state["last_seed"]     = seed
            save_state(state)
            avg = sum(batch_times) / len(batch_times)
            remaining = len(seeds_todo) - len(batch_times)
            eta_min = int(avg * remaining / 60)
            log(f"  Batch {seed} done in {elapsed/60:.1f} min | "
                f"ETA: ~{eta_min} min for {remaining} remaining batches")
        else:
            log(f"  Batch {seed} FAILED — skipping. Check log for details.")
            # Don't add to completed; will be retried on next resume

    # ── final summary ─────────────────────────────────────────────────────────
    total_elapsed = time.time() - run_start
    log(f"\n{'='*60}")
    log(f"OVERNIGHT RUN COMPLETE")
    log(f"{'='*60}")
    log(f"  Batches completed:  {state['batches_done']}")
    log(f"  Total pairs added:  {state['pairs_added']}")
    log(f"  Total time:         {total_elapsed/60:.1f} min")
    log(f"  Combined output:    {COMBINED}")
    log(f"  Log:                {LOG_FILE}")

    # Count combined output lines
    if COMBINED.exists():
        n_combined = sum(1 for l in COMBINED.read_text().splitlines() if l.strip())
        log(f"  Combined records:   {n_combined}")

    log(f"\nNext step: run Phase 5 reports on the combined output:")
    log(f"  python phase5/report.py --input {COMBINED}")
    log(f"  python phase5/calibrate.py --input {COMBINED}")


if __name__ == "__main__":
    import os
    os.chdir(ROOT)
    main()
