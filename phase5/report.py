"""
Phase 5A — Validation Report

Generates a human-readable Markdown report and CSV of all 100 pairs,
organised for manual review. Each pair shows:
  alignment score/level/confidence, LLM judgment + reason,
  contradiction flag, component signals, supported tasks, key flags.

Pairs are grouped by alignment level (STRONG → MEDIUM → WEAK) and
sorted by score descending within each group.

Input:  output/phase4/pairs_phase4.jsonl
Output: output/phase5/validation_report.md
        output/phase5/validation_report.csv

Run:
  python phase5/report.py
"""

import csv
import json
import os
import sys
from pathlib import Path

import argparse

ROOT       = Path(__file__).parent.parent
OUT_DIR    = ROOT / "output" / "phase5"
OUT_DIR.mkdir(parents=True, exist_ok=True)

_parser = argparse.ArgumentParser()
_parser.add_argument("--input", type=str,
                     default=str(ROOT / "output" / "phase4" / "pairs_phase4.jsonl"),
                     help="Input JSONL file (default: output/phase4/pairs_phase4.jsonl)")
_args, _ = _parser.parse_known_args()
INPUT_PATH = Path(_args.input)

# ── helpers ───────────────────────────────────────────────────────────────────

def trunc(s: str, n: int) -> str:
    s = s or ""
    return s[:n] + "…" if len(s) > n else s


def conf_icon(c: str | None) -> str:
    return {"HIGH": "●●●", "MEDIUM": "●●○", "LOW": "●○○", None: "—"}.get(c, c or "—")


def level_icon(l: str | None) -> str:
    return {"STRONG": "🟢", "MEDIUM": "🟡", "WEAK": "🔴", None: "—"}.get(l, l or "—")


def flags(r: dict) -> list[str]:
    f = []
    if r.get("has_contradiction"):       f.append("CONTRADICTION")
    if r.get("repo_too_sparse"):          f.append("SPARSE")
    if not r.get("paper_fetch_success"):  f.append("NO_ABSTRACT")
    al = r.get("alignment") or {}
    if al.get("confidence") == "LOW" and not r.get("has_contradiction"):
        f.append("LOW_CONF")
    if not r.get("is_official"):          f.append("NON-OFFICIAL")
    return f


def comp_summary(cs: dict | None) -> str:
    if not cs:
        return "—"
    parts = []
    for name in ("model", "loss", "eval"):
        sig = (cs.get(name) or {})
        if sig.get("detected"):
            parts.append(f"{name[0].upper()}:{sig.get('confidence','?')[0]}")
    return " ".join(parts) if parts else "none"

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    records: list[dict] = []
    with open(INPUT_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    # Attach convenience fields
    for r in records:
        al = r.get("alignment") or {}
        r["_score"]      = al.get("score")
        r["_level"]      = al.get("level")
        r["_confidence"] = al.get("confidence")
        r["_llm_level"]  = (al.get("llm_alignment") or {}).get("level")
        r["_llm_reason"] = (al.get("llm_alignment") or {}).get("reason") or ""
        r["_contra"]     = al.get("has_contradiction", False)
        r["_flags"]      = flags(r)

    scored   = [r for r in records if r["_score"] is not None]
    unscored = [r for r in records if r["_score"] is None]

    by_level = {
        "STRONG": sorted([r for r in scored if r["_level"] == "STRONG"],
                         key=lambda x: -x["_score"]),
        "MEDIUM": sorted([r for r in scored if r["_level"] == "MEDIUM"],
                         key=lambda x: -x["_score"]),
        "WEAK":   sorted([r for r in scored if r["_level"] == "WEAK"],
                         key=lambda x: -x["_score"]),
    }

    # ── Markdown report ───────────────────────────────────────────────────────
    md_path = OUT_DIR / "validation_report.md"
    with open(md_path, "w") as md:

        md.write("# PWC Pipeline — Phase 5 Validation Report\n\n")
        md.write(f"**Total pairs:** {len(records)}  \n")
        md.write(f"**Scored:** {len(scored)}  \n")
        md.write(f"**Unscored (no clone / no code / too large):** {len(unscored)}  \n\n")

        # Summary table
        md.write("## Summary\n\n")
        md.write("| Level | Count | Official | Non-official |\n")
        md.write("|---|---|---|---|\n")
        for lv in ("STRONG", "MEDIUM", "WEAK"):
            grp = by_level[lv]
            off = sum(1 for r in grp if r.get("is_official"))
            non = len(grp) - off
            md.write(f"| {lv} | {len(grp)} | {off} | {non} |\n")
        md.write(f"| Unscored | {len(unscored)} | — | — |\n\n")

        md.write("| Confidence | Count |\n|---|---|\n")
        for c in ("HIGH", "MEDIUM", "LOW"):
            n = sum(1 for r in scored if r["_confidence"] == c)
            md.write(f"| {c} | {n} |\n")
        md.write("\n")

        md.write(f"**Contradictions:** {sum(1 for r in scored if r['_contra'])}  \n")
        mc_n = sum(1 for r in records if "missing_component" in (r.get("supported_tasks") or []))
        er_n = sum(1 for r in records if "experiment_repair"  in (r.get("supported_tasks") or []))
        md.write(f"**Supports missing_component:** {mc_n}  \n")
        md.write(f"**Supports experiment_repair:** {er_n}  \n\n")

        md.write("---\n\n")

        # Per-level sections
        for lv in ("STRONG", "MEDIUM", "WEAK"):
            grp = by_level[lv]
            md.write(f"## {level_icon(lv)} {lv} ({len(grp)} pairs)\n\n")

            for i, r in enumerate(grp, 1):
                al     = r.get("alignment") or {}
                cs     = r.get("component_signals")
                es     = r.get("experiment_signals") or {}
                rd     = (r.get("readiness") or {})
                mc_rd  = rd.get("missing_component") or {}
                tasks  = r.get("supported_tasks") or []
                sigs   = al.get("signals_fired") or []
                f_list = r["_flags"]

                md.write(f"### {i}. {trunc(r.get('paper_title',''), 90)}\n\n")
                md.write(f"| Field | Value |\n|---|---|\n")
                md.write(f"| **Score** | `{r['_score']}` |\n")
                md.write(f"| **Level** | `{r['_level']}` |\n")
                md.write(f"| **Confidence** | {conf_icon(r['_confidence'])} `{r['_confidence']}` |\n")
                md.write(f"| **Is official** | {'Yes' if r.get('is_official') else 'No'} |\n")
                md.write(f"| **LLM judgment** | `{r['_llm_level']}` |\n")
                md.write(f"| **LLM reason** | {trunc(r['_llm_reason'], 120)} |\n")
                if r["_contra"]:
                    note = al.get("contradiction_note") or ""
                    md.write(f"| **⚠ Contradiction** | {note} |\n")
                md.write(f"| **Components** | {comp_summary(cs)} |\n")
                md.write(f"| **Eval script** | {'Yes' if es.get('has_eval_script') else 'No'} |\n")
                md.write(f"| **Metrics found** | {', '.join((es.get('metric_keywords') or [])[:4]) or '—'} |\n")
                md.write(f"| **Readiness (mc)** | {mc_rd.get('level','—')} ({mc_rd.get('score','—')}) |\n")
                md.write(f"| **Supported tasks** | {', '.join(tasks) if tasks else '—'} |\n")
                md.write(f"| **Signals fired** | {', '.join(sigs)} |\n")
                if f_list:
                    md.write(f"| **Flags** | {' · '.join(f_list)} |\n")
                md.write(f"| **Repo** | {r.get('repo_url','')} |\n")
                md.write("\n")

        # Unscored pairs
        md.write("## ⬜ Unscored Pairs\n\n")
        md.write("| Paper | Reason |\n|---|---|\n")
        for r in unscored:
            reason = (
                "no_executable_code" if r.get("repo_no_executable_code")
                else r.get("clone_error_type") or "too_large" if r.get("repo_too_large")
                else "unknown"
            )
            md.write(f"| {trunc(r.get('paper_title',''), 70)} | `{reason}` |\n")
        md.write("\n")

    print(f"Markdown report → {md_path}")

    # ── CSV export ────────────────────────────────────────────────────────────
    csv_path = OUT_DIR / "validation_report.csv"
    csv_fields = [
        "paper_title", "paper_arxiv_id", "repo_url", "is_official",
        "score", "level", "confidence",
        "llm_level", "llm_reason", "has_contradiction",
        "model_detected", "model_conf",
        "loss_detected",  "loss_conf",
        "eval_detected",  "eval_conf",
        "has_eval_script", "has_config", "metric_keywords",
        "readiness_mc_level", "readiness_mc_score",
        "readiness_er_level",
        "supported_tasks",
        "signals_fired",
        "flags",
        "paper_fetch_success", "repo_too_sparse",
    ]

    with open(csv_path, "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=csv_fields)
        writer.writeheader()
        for r in sorted(records, key=lambda x: (
            {"STRONG":0,"MEDIUM":1,"WEAK":2,None:3}.get(x["_level"], 3),
            -(x["_score"] or 0)
        )):
            al  = r.get("alignment") or {}
            cs  = r.get("component_signals") or {}
            es  = r.get("experiment_signals") or {}
            rd  = r.get("readiness") or {}
            mc  = rd.get("missing_component") or {}
            er  = rd.get("experiment_repair") or {}
            writer.writerow({
                "paper_title":       r.get("paper_title", ""),
                "paper_arxiv_id":    r.get("paper_arxiv_id", ""),
                "repo_url":          r.get("repo_url", ""),
                "is_official":       r.get("is_official", ""),
                "score":             al.get("score", ""),
                "level":             al.get("level", ""),
                "confidence":        al.get("confidence", ""),
                "llm_level":         (al.get("llm_alignment") or {}).get("level", ""),
                "llm_reason":        (al.get("llm_alignment") or {}).get("reason", ""),
                "has_contradiction": al.get("has_contradiction", ""),
                "model_detected":    (cs.get("model") or {}).get("detected", ""),
                "model_conf":        (cs.get("model") or {}).get("confidence", ""),
                "loss_detected":     (cs.get("loss") or {}).get("detected", ""),
                "loss_conf":         (cs.get("loss") or {}).get("confidence", ""),
                "eval_detected":     (cs.get("eval") or {}).get("detected", ""),
                "eval_conf":         (cs.get("eval") or {}).get("confidence", ""),
                "has_eval_script":   es.get("has_eval_script", ""),
                "has_config":        es.get("has_config", ""),
                "metric_keywords":   "|".join(es.get("metric_keywords") or []),
                "readiness_mc_level": mc.get("level", ""),
                "readiness_mc_score": mc.get("score", ""),
                "readiness_er_level": er.get("level", ""),
                "supported_tasks":   "|".join(r.get("supported_tasks") or []),
                "signals_fired":     "|".join(al.get("signals_fired") or []),
                "flags":             "|".join(r["_flags"]),
                "paper_fetch_success": r.get("paper_fetch_success", ""),
                "repo_too_sparse":   r.get("repo_too_sparse", ""),
            })

    print(f"CSV export       → {csv_path}")


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
