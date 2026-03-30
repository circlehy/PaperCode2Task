# PaperCode2Task

Automatic qualification and annotation pipeline for paper–code pairs from the [Papers With Code](https://paperswithcode.com/) dataset. Given 300,000+ paper–repo links, the pipeline filters, scores, and annotates pairs to produce a curated set of seed data for downstream task generation.

---

## Quick Start

### 1. Environment setup

```bash
conda create -n paper2env python=3.11
conda activate paper2env
pip install -r requirements.txt
```

### 2. Configure credentials

```bash
cp .env.example .env
# Edit .env and fill in your keys
```

See [Configuration](#configuration) for details on each key.

### 3. Run the pipeline

Each phase reads from the previous phase's output. Run them in order:

```bash
# Phase 1 — sample pairs, fetch abstracts, clone repos
python phase1/run.py

# Phase 2 — rule-based alignment scoring
python phase2/run.py

# Phase 3 — LLM verification for borderline pairs
python phase3/run.py --production

# Phase 4 — component detection, suitability annotation
python phase4/run.py

# Phase 5 — validation report and calibration analysis
python phase5/report.py
python phase5/calibrate.py
```

---

## Configuration

### `.env` keys

| Key | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | For Phase 3 | Used to call `gpt-4o-mini` for borderline pair verification. Without it, Phase 3 skips LLM calls and scores stay rule-based only. |
| `GITHUB_TOKEN` | Recommended | GitHub Personal Access Token. Raises API rate limit from 60 → 5,000 req/hour. Without it, Phase 1 will slow down significantly on large batches. Create at [github.com/settings/tokens](https://github.com/settings/tokens) — no special scopes needed. |

### `configs/patterns.yaml`

Controls all detection patterns used by Phase 2 and Phase 4 without touching any code:

| Section | What it controls |
|---|---|
| `executable_code_extensions` | File types that count as "real code" (`.py`, `.ipynb`, `.sh`, ...) |
| `document_extensions` | Non-executable types — repos with only these are flagged as `repo_no_executable_code` |
| `model_path_patterns` | Directory/file names used for Layer 1 model detection (`model.py`, `models/`, ...) |
| `loss_path_patterns` | Same for loss component |
| `eval_path_patterns` | Same for eval component |
| `model_content_keywords` | Code keywords for Layer 2 content scan (`nn.Module`, `forward`, ...) |
| `loss_content_keywords` | Same for loss (`CrossEntropyLoss`, `criterion`, ...) |
| `eval_content_keywords` | Same for eval (`evaluate`, `predict`, ...) |
| `ml_structure_dirs` | Directory names used for Layer 3 structure detection (`train/`, `configs/`, ...) |
| `metric_keywords` | Terms scanned in README + eval scripts for experiment signals |

---

## Phase Reference

### Phase 1 — Ingest & Clone

```bash
python phase1/run.py [OPTIONS]
```

| Argument | Default | Description |
|---|---|---|
| `--seed` | 42 | Random seed for stratified sampling |
| `--output` | `output/phase1/pairs.jsonl` | Output file path |
| `--exclude` | None | Path to JSON list of paper IDs to skip (prevents duplicates across batches) |
| `--pair-delay` | 0.3 | Seconds to wait between pairs (rate limiting) |

Samples 25 official + 25 non-official pairs, fetches arXiv abstracts, and clones repos with `--depth=1`.

---

### Phase 2 — Alignment Scoring

```bash
python phase2/run.py [OPTIONS]
```

| Argument | Default | Description |
|---|---|---|
| `--input` | `output/phase1/pairs.jsonl` | Input file |
| `--output` | `output/phase2/pairs_phase2.jsonl` | Output file |

Scores each pair using three signal categories (provenance, surface match, semantic overlap). No LLM calls.

---

### Phase 3 — LLM Integration

```bash
python phase3/run.py [OPTIONS]
```

| Argument | Default | Description |
|---|---|---|
| `--input` | `output/phase2/pairs_phase2.jsonl` | Input file |
| `--output` | `output/phase3/pairs_phase3.jsonl` | Output file |
| `--production` | off | Enable LLM calls. Without this flag, Phase 3 runs in dry-run mode (no API calls, no score changes). |

Calls `gpt-4o-mini` only for borderline scores (0.35–0.65). Results are cached — re-running the same data costs $0.

---

### Phase 4 — Component Detection & Suitability

```bash
python phase4/run.py [OPTIONS]
```

| Argument | Default | Description |
|---|---|---|
| `--input` | `output/phase3/pairs_phase3.jsonl` | Input file |
| `--output` | `output/phase4/pairs_phase4.jsonl` | Output file |

Inspects cloned repos for model/loss/eval components. Assigns `supported_tasks` to each pair.

---

### Phase 5 — Reports & Calibration

```bash
# Human-readable + CSV validation report
python phase5/report.py [--input OUTPUT_FROM_PHASE4]

# Score distribution and threshold sensitivity analysis
python phase5/calibrate.py [--input OUTPUT_FROM_PHASE4]
```

Both scripts default to `output/phase4/pairs_phase4.jsonl`. Pass `--input` to point at a different file (e.g. the combined overnight dataset).

---

## Output Files

| File | Description |
|---|---|
| `output/phase4/pairs_phase4.jsonl` | Full annotated dataset — one JSON record per pair |
| `output/phase5/validation_report.md` | Per-pair report grouped STRONG → MEDIUM → WEAK |
| `output/phase5/validation_report.csv` | Same data as CSV — open in Excel/Sheets, filter by `supported_tasks` |
| `output/phase5/calibration_analysis.md` | Score distribution and threshold sensitivity |
| `output/repos/{arxiv_id}/` | Cloned repositories (excluded from git) |

---

## Running Multiple Batches

For large-scale runs across many batches, use the overnight runner:

```bash
python run_overnight.py --batches 50
```

This handles output naming, exclusion lists, and combining results across batches automatically. Use `--resume` to continue a previously interrupted run.
