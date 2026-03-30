"""
Phase 3 — LLM Integration

For each scored pair from Phase 2:
  1. Build prompt: paper title + abstract (≤1000 chars) + README excerpt (≤1500 chars)
  2. Single gpt-4o-mini call → level (STRONG/MEDIUM/WEAK) + reason
  3. Add LLM contribution to Cat C raw score, recompute total score and level
  4. Contradiction detection
  5. Formal confidence computation (HIGH/MEDIUM/LOW)

Validation mode (default): LLM called on all 88 scored pairs.
Production mode (--production): LLM called only for score in [0.35, 0.65].

LLM cache written to output/phase3/llm_cache.json — safe to interrupt and restart.

Input:  output/phase2/pairs_phase2.jsonl
Output: output/phase3/pairs_phase3.jsonl
        output/phase3/stats_pairs_phase3.json
        output/phase3/llm_cache.json

Run:
  OPENAI_API_KEY=sk-... python phase3/run.py
  OPENAI_API_KEY=sk-... python phase3/run.py --production
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

ROOT        = Path(__file__).parent.parent
CONFIG_PATH = ROOT / "configs" / "patterns.yaml"
INPUT_PATH  = ROOT / "output" / "phase2" / "pairs_phase2.jsonl"
OUTPUT_DIR  = ROOT / "output" / "phase3"
REPOS_DIR   = ROOT / "output" / "repos"
CACHE_PATH  = OUTPUT_DIR / "llm_cache.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load .env from project root if present
from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

sys.path.insert(0, str(ROOT / "phase0"))
from schema import AlignmentResult, LLMAlignment

# ── constants ─────────────────────────────────────────────────────────────────

MODEL           = "gpt-4o-mini"
ABSTRACT_LIMIT  = 1000   # chars sent to LLM
README_LIMIT    = 1500   # chars sent to LLM
CAT_A_CAP       = 0.45
CAT_B_CAP       = 0.25
CAT_C_CAP       = 0.30

# Mirrors Phase 2 signal weights exactly — used to reconstruct raw per-category scores
SIGNAL_WEIGHTS: dict[str, tuple[str, float]] = {
    "is_official":               ("A", 0.20),
    "mentioned_in_paper":        ("A", 0.15),
    "mentioned_in_github":       ("A", 0.05),
    "readme_has_arxiv_id":       ("A", 0.05),
    "readme_has_title":          ("A", 0.05),
    "repo_name_matches_method":  ("B", 0.10),
    "repo_name_overlaps_title":  ("B", 0.05),
    "readme_mentions_method":    ("B", 0.05),
    "readme_has_title_keywords": ("B", 0.05),
    "repo_has_structure":        ("C", 0.05),
    "dataset_keyword_overlap":   ("C", 0.05),
    "task_consistency":          ("C", 0.10),
}

CAT_A_SIGNAL_NAMES = {k for k, (cat, _) in SIGNAL_WEIGHTS.items() if cat == "A"}

LLM_CONTRIBUTION = {"STRONG": 0.10, "MEDIUM": 0.05, "WEAK": 0.00}

# ── helpers ───────────────────────────────────────────────────────────────────

def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def rebuild_cat_scores(signals_fired: list[str]) -> tuple[float, float, float]:
    """Reconstruct raw (uncapped) per-category scores from signals_fired."""
    cat_a = cat_b = cat_c = 0.0
    for sig in signals_fired:
        entry = SIGNAL_WEIGHTS.get(sig)
        if entry:
            cat, w = entry
            if cat == "A":   cat_a += w
            elif cat == "B": cat_b += w
            else:            cat_c += w
    return cat_a, cat_b, cat_c


def read_readme_excerpt(paper_id: str, readme_names: list[str]) -> str:
    safe_id  = re.sub(r"[^a-zA-Z0-9_\-]", "_", paper_id)
    repo_dir = REPOS_DIR / safe_id
    for name in readme_names:
        path = repo_dir / name
        if path.exists():
            try:
                return path.read_text(errors="ignore")[:README_LIMIT]
            except Exception:
                pass
    return ""


def build_prompt(record: dict, readme_excerpt: str) -> str:
    semantics = record.get("paper_semantics") or {}
    title     = record.get("paper_title") or ""
    abstract  = (semantics.get("abstract") or "")[:ABSTRACT_LIMIT]

    paper_block = f"Paper title: {title}"
    if abstract:
        paper_block += f"\nAbstract: {abstract}"

    readme_block = (
        f"Repository README (excerpt):\n{readme_excerpt}"
        if readme_excerpt else
        "Repository README: (not available)"
    )

    return (
        f"{paper_block}\n\n"
        f"{readme_block}\n\n"
        "Does this repository implement the method described in the paper?\n"
        'Respond with JSON only: {"level": "STRONG" | "MEDIUM" | "WEAK", "reason": "<one sentence>"}\n'
        "- STRONG: repo clearly implements this paper's method\n"
        "- MEDIUM: repo is plausibly related but uncertain\n"
        "- WEAK: little or no evidence the repo implements this paper"
    )


def call_llm(client: OpenAI, prompt: str) -> tuple[str, str, str | None]:
    """
    Call gpt-4o-mini with JSON mode. Returns (level, reason, error).
    Retries once on transient failure.
    """
    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an ML paper-code alignment evaluator. "
                            "Always respond with valid JSON."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0,
                max_tokens=150,
            )
            text   = response.choices[0].message.content or ""
            parsed = json.loads(text)
            level  = (parsed.get("level") or "").upper().strip()
            reason = (parsed.get("reason") or "").strip()
            if level not in ("STRONG", "MEDIUM", "WEAK"):
                return "", reason, f"unexpected_level:{level}"
            return level, reason, None

        except Exception as e:
            if attempt == 0:
                time.sleep(3)
                continue
            return "", "", str(e)[:120]

    return "", "", "max_retries_exceeded"

# ── scoring / contradiction / confidence ──────────────────────────────────────

def detect_contradiction(cat_b_raw: float, llm_level: str) -> tuple[bool, str]:
    """
    Surface signals fired (Cat B ≥ 0.10) but LLM returned weak → contradiction.
    No surface signals at all (Cat B == 0.0) but LLM returned strong → contradiction.

    Note: cat_b_raw == 0.0 means zero Cat B signals fired (not merely < 0.10).
    A single readme_has_title_keywords signal (0.05) is not a contradiction with LLM=STRONG —
    both agree the repo is related to the paper. Only the complete absence of any surface
    signal while LLM is highly confident is a genuine contradiction.
    """
    if cat_b_raw >= 0.10 and llm_level == "WEAK":
        return True, "surface signals fired but LLM returned weak"
    if cat_b_raw == 0.0 and llm_level == "STRONG":
        return True, "no surface signals but LLM returned strong"
    return False, ""


def compute_confidence(
    signals_fired: list[str],
    has_contradiction: bool,
    repo_too_sparse: bool,
) -> str:
    if repo_too_sparse or has_contradiction:
        return "LOW"
    explicit_fired = sum(1 for s in signals_fired if s in CAT_A_SIGNAL_NAMES)
    total          = len(signals_fired)
    if explicit_fired >= 1 and total >= 3:
        return "HIGH"
    if total >= 2:
        return "MEDIUM"
    return "LOW"


def recompute_alignment(record: dict, llm_level: str, llm_reason: str) -> dict:
    """
    Rebuild the full AlignmentResult with LLM contribution added to Cat C.
    """
    alignment     = record.get("alignment") or {}
    signals_fired = list(alignment.get("signals_fired") or [])

    cat_a_raw, cat_b_raw, cat_c_raw = rebuild_cat_scores(signals_fired)
    cat_c_with_llm = cat_c_raw + LLM_CONTRIBUTION.get(llm_level, 0.0)

    score = round(
        min(
            min(cat_a_raw, CAT_A_CAP) +
            min(cat_b_raw, CAT_B_CAP) +
            min(cat_c_with_llm, CAT_C_CAP),
            1.0,
        ),
        4,
    )

    if score >= 0.75:   level = "STRONG"
    elif score >= 0.45: level = "MEDIUM"
    else:               level = "WEAK"

    # Add LLM signal to fired list if it contributed
    if llm_level in ("STRONG", "MEDIUM"):
        signals_fired = signals_fired + [f"llm_{llm_level.lower()}"]

    has_contradiction, contradiction_note = detect_contradiction(cat_b_raw, llm_level)
    confidence = compute_confidence(signals_fired, has_contradiction,
                                    record.get("repo_too_sparse", False))

    # Contradiction: cap level at MEDIUM
    if has_contradiction and level == "STRONG":
        level = "MEDIUM"

    return {
        "score":             score,
        "level":             level,
        "confidence":        confidence,
        "has_contradiction": has_contradiction,
        "contradiction_note": contradiction_note if has_contradiction else None,
        "signals_fired":     signals_fired,
        "signal_count":      len(signals_fired),
        "llm_called":        True,
        "llm_alignment":     {"level": llm_level, "reason": llm_reason},
    }

# ── main ──────────────────────────────────────────────────────────────────────

def main(
    input_path: Path  = INPUT_PATH,
    output_path: Path = OUTPUT_DIR / "pairs_phase3.jsonl",
    production_mode: bool = False,
):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    cfg    = load_config()
    readme_names = cfg.get("repo_thresholds", {}).get("readme_filenames", ["README.md"])

    # Load or initialise cache (for restart safety)
    cache: dict = {}
    if CACHE_PATH.exists():
        with open(CACHE_PATH) as f:
            cache = json.load(f)
        if cache:
            print(f"Loaded {len(cache)} cached LLM results")

    records: list[dict] = []
    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    print(f"Loaded {len(records)} pairs from {input_path}")

    mode_label = "production" if production_mode else "validation (all scored pairs)"
    print(f"Mode: {mode_label}\n")

    stats: dict = {
        "total": len(records),
        "llm_called": 0,
        "cache_hits": 0,
        "llm_errors": 0,
        "skipped_not_scored": 0,
        "skipped_out_of_range": 0,
        "level_changes": 0,
        "contradictions": 0,
        "llm_judgments": {"STRONG": 0, "MEDIUM": 0, "WEAK": 0},
        "levels":      {"STRONG": 0, "MEDIUM": 0, "WEAK": 0},
        "confidence":  {"HIGH": 0, "MEDIUM": 0, "LOW": 0},
    }

    with open(output_path, "w") as out_f:
        for record in tqdm(records, desc="Phase 3"):
            alignment = record.get("alignment")

            # Unscored pairs pass through unchanged
            if not alignment:
                stats["skipped_not_scored"] += 1
                out_f.write(json.dumps(record) + "\n")
                continue

            score = alignment.get("score", 0.0)

            # Production mode: skip clearly-resolved pairs
            if production_mode and not (0.35 <= score <= 0.65):
                stats["skipped_out_of_range"] += 1
                out_f.write(json.dumps(record) + "\n")
                continue

            # Cache key: paper_id + repo_url
            cache_key = (record.get("paper_id") or "") + "|" + (record.get("repo_url") or "")

            if cache_key in cache:
                entry      = cache[cache_key]
                llm_level  = entry.get("level", "")
                llm_reason = entry.get("reason", "")
                llm_error  = entry.get("error")
                stats["cache_hits"] += 1
            else:
                readme_excerpt = read_readme_excerpt(
                    record.get("paper_id") or "", readme_names
                )
                prompt = build_prompt(record, readme_excerpt)
                llm_level, llm_reason, llm_error = call_llm(client, prompt)

                cache[cache_key] = {
                    "level": llm_level, "reason": llm_reason, "error": llm_error
                }
                with open(CACHE_PATH, "w") as cf:
                    json.dump(cache, cf, indent=2)

                stats["llm_called"] += 1
                time.sleep(0.3)

            if llm_error or not llm_level:
                alignment["llm_called"]    = True
                alignment["llm_alignment"] = {"level": None, "reason": None, "error": llm_error}
                stats["llm_errors"] += 1
                record["alignment"] = alignment
            else:
                prev_level          = alignment.get("level")
                record["alignment"] = recompute_alignment(record, llm_level, llm_reason)
                if record["alignment"]["level"] != prev_level:
                    stats["level_changes"] += 1
                if record["alignment"]["has_contradiction"]:
                    stats["contradictions"] += 1
                stats["llm_judgments"][llm_level] += 1

            al = record["alignment"]
            if al.get("level") in stats["levels"]:
                stats["levels"][al["level"]] += 1
            if al.get("confidence") in stats["confidence"]:
                stats["confidence"][al["confidence"]] += 1

            out_f.write(json.dumps(record) + "\n")

    # ── summary ───────────────────────────────────────────────────────────────

    scored = stats["llm_called"] + stats["cache_hits"] + stats["llm_errors"]
    print(f"\n{'='*55}")
    print("  PHASE 3 RESULTS")
    print(f"{'='*55}")
    print(f"  Total pairs:             {stats['total']}")
    print(f"  LLM called (new):        {stats['llm_called']}")
    print(f"  Cache hits:              {stats['cache_hits']}")
    print(f"  LLM errors:              {stats['llm_errors']}")
    print(f"  Skipped (not scored):    {stats['skipped_not_scored']}")
    if production_mode:
        print(f"  Skipped (out of range):  {stats['skipped_out_of_range']}")
    print(f"  Level changes after LLM: {stats['level_changes']}")
    print(f"  Contradictions:          {stats['contradictions']}")
    print(f"\n  LLM judgments:")
    for j in ("STRONG", "MEDIUM", "WEAK"):
        print(f"    {j:<8} {stats['llm_judgments'][j]:>3}")
    print(f"\n  Final level distribution:")
    for lv in ("STRONG", "MEDIUM", "WEAK"):
        n = stats["levels"][lv]
        pct = f"{n/scored*100:.0f}%" if scored else "—"
        print(f"    {lv:<8} {n:>3}  ({pct})")
    print(f"\n  Confidence distribution:")
    for c in ("HIGH", "MEDIUM", "LOW"):
        n = stats["confidence"][c]
        pct = f"{n/scored*100:.0f}%" if scored else "—"
        print(f"    {c:<8} {n:>3}  ({pct})")
    print(f"\n  Output: {output_path}")
    print(f"  Cache:  {CACHE_PATH}")

    stats_path = output_path.parent / f"stats_{output_path.stem}.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)


if __name__ == "__main__":
    os.chdir(ROOT)

    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default=str(INPUT_PATH),
                        help="Input JSONL from Phase 2")
    parser.add_argument("--output", default=str(OUTPUT_DIR / "pairs_phase3.jsonl"),
                        help="Output JSONL with LLM alignment and confidence")
    parser.add_argument("--production", action="store_true",
                        help="Production mode: only call LLM for score in [0.35, 0.65]")
    args = parser.parse_args()

    main(
        input_path=Path(args.input),
        output_path=Path(args.output),
        production_mode=args.production,
    )
