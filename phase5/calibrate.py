"""
Phase 5B — Threshold Sensitivity Analysis

Answers the calibration questions:
  1. Where do scores naturally cluster? Are the thresholds (0.75/0.45) well-placed?
  2. Is the official/non-official scoring gap a threshold problem or a weight problem?
  3. Which pairs are borderline (within ±0.05 of a threshold)?
  4. How do STRONG/MEDIUM/WEAK counts shift as thresholds vary?
  5. Where do contradictions and LLM disagreements sit in the score distribution?

Input:  output/phase4/pairs_phase4.jsonl
Output: output/phase5/calibration_analysis.md
        output/phase5/calibration_stats.json

Run:
  python phase5/calibrate.py
"""

import argparse
import json
import os
from pathlib import Path

ROOT       = Path(__file__).parent.parent
OUT_DIR    = ROOT / "output" / "phase5"
OUT_DIR.mkdir(parents=True, exist_ok=True)

_parser = argparse.ArgumentParser()
_parser.add_argument("--input", type=str,
                     default=str(ROOT / "output" / "phase4" / "pairs_phase4.jsonl"),
                     help="Input JSONL file (default: output/phase4/pairs_phase4.jsonl)")
_args, _ = _parser.parse_known_args()
INPUT_PATH = Path(_args.input)

CURRENT_STRONG = 0.75
CURRENT_MEDIUM = 0.45
BORDERLINE_TOL = 0.05

# ── helpers ───────────────────────────────────────────────────────────────────

def levels_at(scores: list[float], strong_t: float, medium_t: float) -> dict:
    s = sum(1 for x in scores if x >= strong_t)
    m = sum(1 for x in scores if medium_t <= x < strong_t)
    w = sum(1 for x in scores if x < medium_t)
    return {"STRONG": s, "MEDIUM": m, "WEAK": w}


def bar(value: int, total: int, width: int = 30) -> str:
    n = round(value / total * width) if total else 0
    return "█" * n + "░" * (width - n)


def bucket_scores(scores: list[float], lo: float, hi: float,
                  n_buckets: int = 20) -> list[int]:
    step   = (hi - lo) / n_buckets
    counts = [0] * n_buckets
    for s in scores:
        idx = int((s - lo) / step)
        idx = max(0, min(n_buckets - 1, idx))
        counts[idx] += 1
    return counts

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    records: list[dict] = []
    with open(INPUT_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    scored = [r for r in records if (r.get("alignment") or {}).get("score") is not None]
    all_scores   = [(r.get("alignment") or {})["score"] for r in scored]
    off_scores   = [(r.get("alignment") or {})["score"] for r in scored if r.get("is_official")]
    nonoff_scores= [(r.get("alignment") or {})["score"] for r in scored if not r.get("is_official")]

    stats = {}
    md_lines: list[str] = []
    w = md_lines.append

    w("# PWC Pipeline — Phase 5 Calibration Analysis\n")
    w(f"Scored pairs: {len(scored)} | "
      f"Official: {len(off_scores)} | Non-official: {len(nonoff_scores)}\n")
    w(f"Current thresholds: STRONG ≥ {CURRENT_STRONG} | MEDIUM ≥ {CURRENT_MEDIUM}\n")

    # ── 1. Score distribution histogram ──────────────────────────────────────
    w("\n---\n")
    w("## 1. Score Distribution\n")
    w("```")
    w(f"{'Score range':<14}  {'All':>4}  {'Official':>8}  {'Non-off':>7}  Histogram (all)")
    w("-" * 65)

    buckets_all = bucket_scores(all_scores,    0.0, 1.0, 20)
    buckets_off = bucket_scores(off_scores,    0.0, 1.0, 20)
    buckets_non = bucket_scores(nonoff_scores, 0.0, 1.0, 20)

    for i, (a, o, n) in enumerate(zip(buckets_all, buckets_off, buckets_non)):
        lo = i * 0.05
        hi = lo + 0.05
        marker = ""
        if abs(lo - CURRENT_STRONG) < 0.001: marker = " ◄ STRONG threshold"
        if abs(lo - CURRENT_MEDIUM) < 0.001: marker = " ◄ MEDIUM threshold"
        w(f"[{lo:.2f}–{hi:.2f})     {a:>4}  {o:>8}  {n:>7}  {bar(a, len(scored), 25)}{marker}")
    w("```\n")

    stats["score_distribution"] = {
        "all": {f"{i*0.05:.2f}-{i*0.05+0.05:.2f}": c
                for i, c in enumerate(buckets_all)},
        "official": {f"{i*0.05:.2f}-{i*0.05+0.05:.2f}": c
                     for i, c in enumerate(buckets_off)},
        "non_official": {f"{i*0.05:.2f}-{i*0.05+0.05:.2f}": c
                         for i, c in enumerate(buckets_non)},
    }

    # Key stats
    w("**Summary statistics:**\n")
    w(f"| Metric | All | Official | Non-official |")
    w(f"|---|---|---|---|")
    for label, s_list in [("All", all_scores), ("Official", off_scores), ("Non-off", nonoff_scores)]:
        pass
    for metric, fn in [
        ("Min",    min), ("Max", max),
        ("Mean",   lambda x: round(sum(x)/len(x), 3) if x else 0),
        ("Median", lambda x: sorted(x)[len(x)//2] if x else 0),
    ]:
        a = fn(all_scores)    if all_scores    else "—"
        o = fn(off_scores)    if off_scores    else "—"
        n = fn(nonoff_scores) if nonoff_scores else "—"
        w(f"| {metric} | {a} | {o} | {n} |")
    w("")

    # ── 2. Official vs Non-official level breakdown ───────────────────────────
    w("\n---\n")
    w("## 2. Official vs Non-official Breakdown\n")

    lv_off    = levels_at(off_scores,    CURRENT_STRONG, CURRENT_MEDIUM)
    lv_nonoff = levels_at(nonoff_scores, CURRENT_STRONG, CURRENT_MEDIUM)

    w("| Level | Official | Non-official |")
    w("|---|---|---|")
    for lv in ("STRONG", "MEDIUM", "WEAK"):
        w(f"| {lv} | {lv_off[lv]} / {len(off_scores)} | {lv_nonoff[lv]} / {len(nonoff_scores)} |")
    w("")
    w(f"> **Key finding:** All {len(nonoff_scores)} non-official repos are WEAK at current thresholds.  \n"
      f"> Max non-official score: `{max(nonoff_scores):.3f}` — threshold for MEDIUM is `{CURRENT_MEDIUM}`.  \n"
      f"> Gap: `{CURRENT_MEDIUM - max(nonoff_scores):.3f}` — non-official repos would need this score increase to reach MEDIUM.")

    if nonoff_scores:
        max_nonoff = max(nonoff_scores)
        stats["nonofficial_max_score"] = max_nonoff
        stats["nonofficial_gap_to_medium"] = round(CURRENT_MEDIUM - max_nonoff, 4)
    w("")

    # ── 3. Threshold sensitivity table ───────────────────────────────────────
    w("\n---\n")
    w("## 3. Threshold Sensitivity\n")
    w("How STRONG/MEDIUM/WEAK counts change as thresholds vary (all scored pairs).\n")
    w("```")
    w(f"{'STRONG≥':<9} {'MEDIUM≥':<9} {'STRONG':>7} {'MEDIUM':>7} {'WEAK':>7}")
    w("-" * 45)

    sensitivity_rows = []
    for strong_t in [0.60, 0.65, 0.70, 0.75, 0.80]:
        for medium_t in [0.35, 0.40, 0.45, 0.50]:
            if medium_t >= strong_t:
                continue
            lv = levels_at(all_scores, strong_t, medium_t)
            marker = " ◄ current" if strong_t == CURRENT_STRONG and medium_t == CURRENT_MEDIUM else ""
            w(f"{strong_t:<9.2f} {medium_t:<9.2f} {lv['STRONG']:>7} {lv['MEDIUM']:>7} {lv['WEAK']:>7}{marker}")
            sensitivity_rows.append({"strong_t": strong_t, "medium_t": medium_t, **lv})
    w("```\n")
    stats["sensitivity"] = sensitivity_rows

    # ── 4. Borderline pairs ───────────────────────────────────────────────────
    w("\n---\n")
    w("## 4. Borderline Pairs\n")
    w(f"Pairs within ±{BORDERLINE_TOL} of a threshold (most sensitive to recalibration).\n")

    borderline_strong = [r for r in scored
        if abs((r["alignment"]["score"]) - CURRENT_STRONG) <= BORDERLINE_TOL]
    borderline_medium = [r for r in scored
        if abs((r["alignment"]["score"]) - CURRENT_MEDIUM) <= BORDERLINE_TOL]

    w(f"### Near STRONG threshold ({CURRENT_STRONG} ± {BORDERLINE_TOL}): {len(borderline_strong)} pairs\n")
    w("| Score | Level | Official | LLM | Title |")
    w("|---|---|---|---|---|")
    for r in sorted(borderline_strong, key=lambda x: -x["alignment"]["score"]):
        al = r["alignment"]
        llm_l = (al.get("llm_alignment") or {}).get("level", "—")
        w(f"| `{al['score']}` | {al['level']} | {'Y' if r.get('is_official') else 'N'} | {llm_l} | {r.get('paper_title','')[:60]} |")
    w("")

    w(f"### Near MEDIUM threshold ({CURRENT_MEDIUM} ± {BORDERLINE_TOL}): {len(borderline_medium)} pairs\n")
    w("| Score | Level | Official | LLM | Title |")
    w("|---|---|---|---|---|")
    for r in sorted(borderline_medium, key=lambda x: -x["alignment"]["score"]):
        al = r["alignment"]
        llm_l = (al.get("llm_alignment") or {}).get("level", "—")
        w(f"| `{al['score']}` | {al['level']} | {'Y' if r.get('is_official') else 'N'} | {llm_l} | {r.get('paper_title','')[:60]} |")
    w("")

    stats["borderline_strong_count"] = len(borderline_strong)
    stats["borderline_medium_count"] = len(borderline_medium)

    # ── 5. LLM vs rule-based disagreements ───────────────────────────────────
    w("\n---\n")
    w("## 5. LLM vs Rule-based Disagreements\n")
    w("Cases where LLM judgment diverges from rule-based level (before LLM was added).\n")

    disagreements = []
    for r in scored:
        al = r.get("alignment") or {}
        sigs  = al.get("signals_fired") or []
        llm_l = (al.get("llm_alignment") or {}).get("level")
        if not llm_l:
            continue
        # Reconstruct rule-based level from score minus LLM contribution
        llm_contrib = {"llm_strong": 0.10, "llm_medium": 0.05}
        contrib = sum(llm_contrib.get(s, 0.0) for s in sigs)
        pre_llm_score = round(al["score"] - contrib, 4)
        if pre_llm_score >= CURRENT_STRONG:  pre_level = "STRONG"
        elif pre_llm_score >= CURRENT_MEDIUM: pre_level = "MEDIUM"
        else:                                 pre_level = "WEAK"
        post_level = al.get("level")
        if pre_level != post_level:
            disagreements.append({
                "title": r.get("paper_title","")[:60],
                "official": r.get("is_official"),
                "pre_llm_score": pre_llm_score,
                "pre_level": pre_level,
                "post_level": post_level,
                "llm_level": llm_l,
                "llm_reason": (al.get("llm_alignment") or {}).get("reason","")[:80],
            })

    w(f"**{len(disagreements)} pairs changed level after LLM signal was added.**\n")
    w("| Pre-LLM | Post-LLM | LLM | Official | Pre-score | Title |")
    w("|---|---|---|---|---|---|")
    for d in sorted(disagreements, key=lambda x: -x["pre_llm_score"]):
        w(f"| {d['pre_level']} | {d['post_level']} | {d['llm_level']} | "
          f"{'Y' if d['official'] else 'N'} | `{d['pre_llm_score']}` | {d['title']} |")
    w("")

    stats["llm_level_changes"] = len(disagreements)
    stats["llm_disagreements"]  = disagreements

    # ── 6. Contradiction review ───────────────────────────────────────────────
    w("\n---\n")
    w("## 6. Contradiction Cases\n")

    contras = [r for r in scored if (r.get("alignment") or {}).get("has_contradiction")]
    w(f"**{len(contras)} contradictions detected.**\n")
    if contras:
        w("| Score | Level | Conf | Official | Note | Title |")
        w("|---|---|---|---|---|---|")
        for r in sorted(contras, key=lambda x: -x["alignment"]["score"]):
            al = r["alignment"]
            note = (al.get("contradiction_note") or "")[:50]
            w(f"| `{al['score']}` | {al['level']} | {al.get('confidence','—')} | "
              f"{'Y' if r.get('is_official') else 'N'} | {note} | {r.get('paper_title','')[:50]} |")
    w("")

    stats["contradiction_count"] = len(contras)

    # ── Write outputs ─────────────────────────────────────────────────────────
    md_path = OUT_DIR / "calibration_analysis.md"
    with open(md_path, "w") as f:
        f.write("\n".join(md_lines))
    print(f"Calibration report → {md_path}")

    stats_path = OUT_DIR / "calibration_stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Calibration stats  → {stats_path}")


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
