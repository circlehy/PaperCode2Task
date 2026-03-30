"""
Phase 4 — Component + Experiment Signals + Readiness + Task Suitability

For each scored pair from Phase 3:
  Component signals (model, loss, eval) — 3-layer heuristic:
    Layer 1 path-based  (filenames + component dirs) → HIGH
    Layer 2 content-based (first 50 lines, up to 30 files) → MEDIUM
    Layer 3 broad ML structure (≥2 structure dirs, no component found) → LOW
  Experiment signals:
    has_eval_script, metric_keywords, has_config, eval/metric confidence
  Readiness:
    missing_component score + level (from model/loss confidences)
    experiment_repair readiness (binary)
  Task suitability:
    supported_tasks list (missing_component, experiment_repair)

repo_too_sparse pairs: passed through with empty signals.

Input:  output/phase3/pairs_phase3.jsonl
Output: output/phase4/pairs_phase4.jsonl
        output/phase4/stats_pairs_phase4.json

Run:
  python phase4/run.py [--input PATH] [--output PATH]
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml
from tqdm import tqdm

ROOT        = Path(__file__).parent.parent
CONFIG_PATH = ROOT / "configs" / "patterns.yaml"
INPUT_PATH  = ROOT / "output" / "phase3" / "pairs_phase3.jsonl"
OUTPUT_DIR  = ROOT / "output" / "phase4"
REPOS_DIR   = ROOT / "output" / "repos"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT / "phase0"))
from schema import (
    ComponentSignal, ComponentSignals,
    ExperimentSignals, Readiness, ReadinessScore,
)

# ── constants ─────────────────────────────────────────────────────────────────

CONTENT_SCAN_LINES = 50    # lines per file for Layer 2
CONTENT_SCAN_FILES = 30    # max files per repo for Layer 2
STRUCTURE_DIR_MIN  = 2     # min matching dirs for Layer 3

# Readiness table: (model_conf, loss_conf) → (score, level)
# Keyed by (model_tier, loss_tier) where tier: 2=HIGH, 1=MEDIUM, 0=LOW/absent
def _readiness(model_tier: int, loss_tier: int) -> tuple[float, str]:
    best = max(model_tier, loss_tier)
    both = min(model_tier, loss_tier)
    if model_tier >= 2 and loss_tier >= 2:   return 1.00, "HIGH"
    if best >= 2 and both >= 1:              return 0.75, "HIGH"
    if model_tier >= 1 and loss_tier >= 1:   return 0.50, "MEDIUM"
    if best >= 1 and both == 0:              return 0.50, "MEDIUM"
    if best == -1:                           return 0.00, "LOW"   # neither detected
    return 0.20, "LOW"   # only LOW confidence detection

CONF_TIER = {"HIGH": 2, "MEDIUM": 1, "LOW": 0, None: -1}

# ── helpers ───────────────────────────────────────────────────────────────────

def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def repo_dir_from_id(paper_id: str) -> Path:
    safe_id = re.sub(r"[^a-zA-Z0-9_\-]", "_", paper_id)
    return REPOS_DIR / safe_id


def all_files(repo_dir: Path) -> list[Path]:
    """Return all non-.git files recursively."""
    return [
        f for f in repo_dir.rglob("*")
        if f.is_file() and ".git" not in f.parts
    ]


def top_level_dirs(repo_dir: Path) -> set[str]:
    try:
        return {d.name.lower() for d in repo_dir.iterdir()
                if d.is_dir() and d.name != ".git"}
    except Exception:
        return set()


def read_head(path: Path, n_lines: int = CONTENT_SCAN_LINES) -> str:
    try:
        lines = path.read_text(errors="ignore").splitlines()[:n_lines]
        return "\n".join(lines)
    except Exception:
        return ""

# ── Layer 1: path-based detection ─────────────────────────────────────────────

def detect_layer1(files: list[Path], tl_dirs: set[str],
                  comp_cfg: dict) -> bool:
    """
    HIGH confidence: any filename match OR component-specific directory present.
    """
    fname_set = {f.name.lower() for f in files}
    for fn in comp_cfg.get("filenames", []):
        if fn.lower() in fname_set:
            return True
    for d in comp_cfg.get("directories", []):
        if d.lower() in tl_dirs:
            return True
    return False

# ── Layer 2: content-based detection ─────────────────────────────────────────

def detect_layer2(files: list[Path], comp_cfg: dict,
                  exe_exts: set[str]) -> bool:
    """
    MEDIUM confidence: keyword found in first CONTENT_SCAN_LINES lines
    of any code file (up to CONTENT_SCAN_FILES files).
    Known limitation: keywords are PyTorch/TF-specific; non-Python repos
    will not trigger this layer.
    """
    keywords = comp_cfg.get("content_keywords", [])
    if not keywords:
        return False

    code_files = [f for f in files if f.suffix in exe_exts][:CONTENT_SCAN_FILES]
    for cf in code_files:
        text = read_head(cf)
        if any(kw in text for kw in keywords):
            return True
    return False

# ── Layer 3: broad ML structure ───────────────────────────────────────────────

def detect_layer3(tl_dirs: set[str], struct_dirs: set[str]) -> bool:
    """
    LOW confidence: no component-specific patterns found, but repo has
    ≥ STRUCTURE_DIR_MIN general ML project directories.
    """
    return len(tl_dirs & struct_dirs) >= STRUCTURE_DIR_MIN

# ── Component detection ───────────────────────────────────────────────────────

def detect_component(files: list[Path], tl_dirs: set[str],
                     comp_cfg: dict, exe_exts: set[str],
                     struct_dirs: set[str]) -> ComponentSignal:
    """Run 3-layer heuristic for one component. Return ComponentSignal."""
    if detect_layer1(files, tl_dirs, comp_cfg):
        return ComponentSignal(detected=True, confidence="HIGH",
                               detection_layer="path")
    if detect_layer2(files, comp_cfg, exe_exts):
        return ComponentSignal(detected=True, confidence="MEDIUM",
                               detection_layer="content")
    if detect_layer3(tl_dirs, struct_dirs):
        return ComponentSignal(detected=True, confidence="LOW",
                               detection_layer="directory")
    return ComponentSignal(detected=False)

# ── Experiment signals ────────────────────────────────────────────────────────

def detect_experiment(files: list[Path], tl_dirs: set[str],
                      repo_dir: Path, cfg: dict,
                      readme_text: str) -> ExperimentSignals:
    exp_cfg      = cfg.get("experiment_patterns", {})
    metric_kws   = exp_cfg.get("metric_keywords", [])
    config_exts  = set(exp_cfg.get("config_extensions", []))
    config_dirs  = set(exp_cfg.get("config_directories", []))

    eval_filenames = {"eval.py", "evaluate.py", "test.py",
                      "benchmark.py", "score.py"}
    fname_set = {f.name.lower() for f in files}

    # has_eval_script
    has_eval = bool(fname_set & eval_filenames)

    # has_config: YAML/YML anywhere (dominant ML config format), OR any
    # config-extension file inside a named config directory.
    yaml_exts = {".yaml", ".yml"}
    has_config = (
        any(f.suffix in yaml_exts for f in files)
        or any(
            f.suffix in config_exts and any(part in config_dirs for part in f.parts)
            for f in files
        )
    )

    # metric_keywords: scan README + eval script files
    scan_text = readme_text
    for f in files:
        if f.name.lower() in eval_filenames:
            scan_text += "\n" + read_head(f)
    found_metrics = [kw for kw in metric_kws if kw in scan_text]
    # Deduplicate case-insensitively
    seen, deduped = set(), []
    for kw in found_metrics:
        k = kw.lower()
        if k not in seen:
            seen.add(k)
            deduped.append(kw)
    found_metrics = deduped

    # eval_confidence
    if has_eval and found_metrics:
        eval_conf = "HIGH"
    elif has_eval or found_metrics:
        eval_conf = "MEDIUM"
    else:
        eval_conf = "LOW"

    # metric_confidence
    if len(found_metrics) >= 3:
        metric_conf = "HIGH"
    elif len(found_metrics) >= 1:
        metric_conf = "MEDIUM"
    else:
        metric_conf = "LOW"

    return ExperimentSignals(
        has_eval_script=has_eval,
        eval_confidence=eval_conf,
        metric_keywords=found_metrics,
        metric_confidence=metric_conf,
        has_config=has_config,
    )

# ── Readiness ─────────────────────────────────────────────────────────────────

def compute_readiness(cs: ComponentSignals,
                      es: ExperimentSignals) -> Readiness:
    model_tier = CONF_TIER.get(cs.model.confidence if cs.model.detected else None, -1)
    loss_tier  = CONF_TIER.get(cs.loss.confidence  if cs.loss.detected  else None, -1)

    mc_score, mc_level = _readiness(model_tier, loss_tier)

    er_ready = es.has_eval_script and bool(es.metric_keywords) and es.has_config
    er_score = 1.0 if er_ready else 0.0
    er_level = "HIGH" if er_ready else "LOW"

    return Readiness(
        missing_component=ReadinessScore(score=mc_score, level=mc_level),
        experiment_repair=ReadinessScore(score=er_score, level=er_level),
    )

# ── Task suitability ──────────────────────────────────────────────────────────

def compute_suitability(cs: ComponentSignals,
                        readiness: Readiness,
                        alignment_level: str | None) -> list[str]:
    tasks = []

    # Both task types require MEDIUM+ alignment — the paper must actually
    # describe the code in this repo, otherwise the paper provides no useful
    # specification for the task (no method description, no expected results).
    if alignment_level not in ("STRONG", "MEDIUM"):
        return tasks

    # missing_component: model or loss at MEDIUM+ AND readiness MEDIUM+
    model_ok = cs.model.detected and cs.model.confidence in ("HIGH", "MEDIUM")
    loss_ok  = cs.loss.detected  and cs.loss.confidence  in ("HIGH", "MEDIUM")
    mc_level = readiness.missing_component.level
    if (model_ok or loss_ok) and mc_level in ("HIGH", "MEDIUM"):
        tasks.append("missing_component")

    # experiment_repair: eval script + metric keywords + config
    if readiness.experiment_repair.level == "HIGH":
        tasks.append("experiment_repair")

    return tasks

# ── Process one pair ──────────────────────────────────────────────────────────

def process_pair(record: dict, cfg: dict) -> dict:
    # Pass-through conditions
    if not record.get("clone_success") or record.get("repo_no_executable_code"):
        return record
    if record.get("repo_too_sparse"):
        # Keep empty signals, mark as processed
        record["component_signals"]  = ComponentSignals().model_dump()
        record["experiment_signals"] = ExperimentSignals().model_dump()
        record["readiness"]          = Readiness().model_dump()
        record["supported_tasks"]    = []
        return record

    exe_exts    = set(cfg.get("executable_code_extensions", []))
    struct_dirs = set(cfg.get("structure_pattern_directories", []))
    comp_cfg    = cfg.get("component_patterns", {})
    readme_names = cfg.get("repo_thresholds", {}).get("readme_filenames", ["README.md"])

    paper_id = record.get("paper_id") or ""
    rd       = repo_dir_from_id(paper_id)
    if not rd.exists():
        return record

    files   = all_files(rd)
    tl_dirs = top_level_dirs(rd)

    # README text for experiment signal scan
    readme_text = ""
    for name in readme_names:
        p = rd / name
        if p.exists():
            try:
                readme_text = p.read_text(errors="ignore")[:20_000]
                break
            except Exception:
                pass

    # Component signals
    cs = ComponentSignals(
        model=detect_component(files, tl_dirs, comp_cfg.get("model", {}),
                               exe_exts, struct_dirs),
        loss=detect_component(files, tl_dirs, comp_cfg.get("loss", {}),
                              exe_exts, struct_dirs),
        eval=detect_component(files, tl_dirs, comp_cfg.get("eval", {}),
                              exe_exts, struct_dirs),
    )

    # Experiment signals
    es = detect_experiment(files, tl_dirs, rd, cfg, readme_text)

    # Readiness + suitability
    alignment_level = (record.get("alignment") or {}).get("level")
    readiness       = compute_readiness(cs, es)
    supported_tasks = compute_suitability(cs, readiness, alignment_level)

    record["component_signals"]  = json.loads(cs.model_dump_json())
    record["experiment_signals"] = json.loads(es.model_dump_json())
    record["readiness"]          = json.loads(readiness.model_dump_json())
    record["supported_tasks"]    = supported_tasks
    return record

# ── main ──────────────────────────────────────────────────────────────────────

def main(input_path: Path = INPUT_PATH,
         output_path: Path = OUTPUT_DIR / "pairs_phase4.jsonl"):
    cfg = load_config()

    records: list[dict] = []
    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    print(f"Loaded {len(records)} pairs from {input_path}")

    stats: dict = {
        "total": len(records),
        "processed": 0,
        "skipped_no_clone": 0,
        "skipped_no_code": 0,
        "sparse_passthrough": 0,
        "component": {
            "model":  {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "none": 0},
            "loss":   {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "none": 0},
            "eval":   {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "none": 0},
        },
        "experiment": {
            "has_eval_script": 0,
            "has_config": 0,
            "has_metrics": 0,
        },
        "readiness": {"HIGH": 0, "MEDIUM": 0, "LOW": 0},
        "tasks": {"missing_component": 0, "experiment_repair": 0, "both": 0, "none": 0},
    }

    with open(output_path, "w") as out_f:
        for record in tqdm(records, desc="Phase 4"):
            if not record.get("clone_success"):
                stats["skipped_no_clone"] += 1
                out_f.write(json.dumps(record) + "\n")
                continue
            if record.get("repo_no_executable_code"):
                stats["skipped_no_code"] += 1
                out_f.write(json.dumps(record) + "\n")
                continue

            record = process_pair(record, cfg)

            if record.get("repo_too_sparse"):
                stats["sparse_passthrough"] += 1
            else:
                stats["processed"] += 1

                cs = record.get("component_signals") or {}
                for comp in ("model", "loss", "eval"):
                    sig = cs.get(comp) or {}
                    if sig.get("detected"):
                        conf = sig.get("confidence") or "LOW"
                        stats["component"][comp][conf] += 1
                    else:
                        stats["component"][comp]["none"] += 1

                es = record.get("experiment_signals") or {}
                if es.get("has_eval_script"):   stats["experiment"]["has_eval_script"] += 1
                if es.get("has_config"):         stats["experiment"]["has_config"] += 1
                if es.get("metric_keywords"):    stats["experiment"]["has_metrics"] += 1

                rd = (record.get("readiness") or {}).get("missing_component") or {}
                lvl = rd.get("level") or "LOW"
                stats["readiness"][lvl] = stats["readiness"].get(lvl, 0) + 1

                tasks = record.get("supported_tasks") or []
                has_mc = "missing_component"  in tasks
                has_er = "experiment_repair"  in tasks
                if has_mc and has_er:    stats["tasks"]["both"] += 1
                elif has_mc:             stats["tasks"]["missing_component"] += 1
                elif has_er:             stats["tasks"]["experiment_repair"] += 1
                else:                    stats["tasks"]["none"] += 1

            out_f.write(json.dumps(record) + "\n")

    # ── summary ───────────────────────────────────────────────────────────────
    n = stats["processed"]
    print(f"\n{'='*55}")
    print("  PHASE 4 RESULTS")
    print(f"{'='*55}")
    print(f"  Total pairs:             {stats['total']}")
    print(f"  Processed:               {n}")
    print(f"  Skipped (no clone):      {stats['skipped_no_clone']}")
    print(f"  Skipped (no code):       {stats['skipped_no_code']}")
    print(f"  Sparse (empty signals):  {stats['sparse_passthrough']}")
    print(f"\n  Component detection (of {n} processed):")
    for comp in ("model", "loss", "eval"):
        c = stats["component"][comp]
        detected = c["HIGH"] + c["MEDIUM"] + c["LOW"]
        print(f"    {comp:<6}  HIGH={c['HIGH']}  MEDIUM={c['MEDIUM']}  LOW={c['LOW']}  none={c['none']}  → detected {detected}/{n}")
    print(f"\n  Experiment signals:")
    for k, v in stats["experiment"].items():
        print(f"    {k:<20} {v}/{n}")
    print(f"\n  Readiness (missing_component):")
    for lvl in ("HIGH", "MEDIUM", "LOW"):
        print(f"    {lvl:<8} {stats['readiness'].get(lvl, 0)}")
    print(f"\n  Task suitability:")
    print(f"    missing_component only:   {stats['tasks']['missing_component']}")
    print(f"    experiment_repair only:   {stats['tasks']['experiment_repair']}")
    print(f"    both:                     {stats['tasks']['both']}")
    print(f"    none:                     {stats['tasks']['none']}")
    total_mc = stats['tasks']['missing_component'] + stats['tasks']['both']
    total_er = stats['tasks']['experiment_repair'] + stats['tasks']['both']
    print(f"    → supports missing_component: {total_mc}/{n}")
    print(f"    → supports experiment_repair: {total_er}/{n}")
    print(f"\n  Output: {output_path}")

    stats_path = output_path.parent / f"stats_{output_path.stem}.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)


if __name__ == "__main__":
    os.chdir(ROOT)
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default=str(INPUT_PATH))
    parser.add_argument("--output", default=str(OUTPUT_DIR / "pairs_phase4.jsonl"))
    args = parser.parse_args()
    main(input_path=Path(args.input), output_path=Path(args.output))
