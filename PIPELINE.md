# Pipeline Design — PaperCode2Task

This document explains the conceptual design of each phase, why it was built that way, and what decisions were made along the way. For detailed results and statistics, see [doc/pipeline_report.md](doc/pipeline_report.md).

---

## The Problem

The [Papers With Code](https://paperswithcode.com/) dataset contains 300,000+ links between research papers and GitHub repositories. Not all of these links are useful for task generation:

- Many repos are community submissions that don't actually implement the linked paper
- Many are placeholders, notebooks-only, or too sparse to work with
- Even genuine implementations may lack the specific structure needed for the tasks we want to generate

**Goal:** Automatically filter this dataset down to a curated set of paper–repo pairs that are ready for downstream task generation — specifically two task types:

| Task Type | Description |
|---|---|
| `missing_component` | The repo implements most of a paper's method but is missing a key component (e.g. loss function). Generate a task to implement the missing piece. |
| `experiment_repair` | The repo has evaluation infrastructure and metrics but broken or incomplete experiments. Generate a task to repair them. |

Manual review of 300,000 pairs is not feasible. The pipeline automates this filtering using a combination of rule-based heuristics, LLM judgment, and code structure analysis.

---

## Pipeline Overview

```
PWC Dataset (300,161 pairs)
         │
         ▼
Phase 1: Ingest & Clone       ← stratified sample, arXiv fetch, git clone
         │
         ▼
Phase 2: Alignment Scoring    ← rule-based signals, 3-category weighted score
         │
         ▼
Phase 3: LLM Verification     ← LLM judgment for borderline pairs only
         │
         ▼
Phase 4: Component Analysis   ← code structure inspection, task suitability
         │
         ▼
Phase 5: Calibration          ← threshold analysis, human-readable reports
```

Each phase enriches the same JSONL record — no data is lost between phases. The final record contains everything from Phase 1 through Phase 4 in one place.

---

## Phase 1 — Ingest & Clone

**What it does:** Samples pairs from the PWC dataset, fetches paper abstracts from arXiv, and clones each repo with `git clone --depth=1`.

**Why stratified sampling (25 official + 25 non-official)?**

The PWC dataset is heavily imbalanced toward non-official repos. A pure random sample would be dominated by community submissions, making it hard to evaluate whether the scoring works for the more important official implementations. By fixing the split at 25 + 25 per batch, both populations are equally represented and results are comparable across batches.

**Why `--depth=1`?**

Full clone history is irrelevant for code analysis. A shallow clone reduces disk usage from potentially hundreds of MB to ~8 MB median per repo, and clone time from minutes to seconds.

**Why check repo size and code density before Phase 2?**

Phase 2 scoring takes time per pair. Filtering obvious non-starters early (repo > 500 MB, < 3 executable files, no executable code at all) avoids wasting compute on repos that will never qualify. This pre-check removes about 12% of sampled pairs.

---

## Phase 2 — Alignment Scoring

**What it does:** Scores how well a repo implements its linked paper using three categories of rule-based signals. No LLM calls — fully deterministic.

**Why three categories with per-category caps?**

The simplest design would be a flat list of signals. The problem: `is_official` (0.30) plus `mentioned_in_paper` (0.15) already totals 0.45 — a PWC-labeled official repo that cites itself is at MEDIUM before any code evidence is checked. Provenance signals would dominate entirely.

The three-category cap design solves this:

- **Cat A — Provenance** (cap 0.45): Is this repo officially linked to the paper? Does the paper cite this repo? Does the repo cite the paper?
- **Cat B — Surface match** (cap 0.25): Does the repo name or README mention the paper title, arXiv ID, or method name?
- **Cat C — Semantic overlap** (cap 0.30): Do the repo name and README show genuine domain/task overlap with the paper abstract?

Even if Cat A is fully saturated, a score ≥ 0.75 (STRONG) requires meaningful contributions from all three categories. An official repo with a blank README and no semantic overlap cannot reach STRONG.

**Score → Level thresholds:**

| Score | Level | Meaning |
|---|---|---|
| ≥ 0.75 | STRONG | High confidence this repo implements the paper |
| 0.45 – 0.74 | MEDIUM | Likely an implementation, not conclusive |
| < 0.45 | WEAK | Little or no evidence |

These thresholds were set by design reasoning before any data was collected. After processing 2,750 pairs, the score distribution showed natural gaps at exactly 0.35–0.45 and 0.70–0.75 — confirming the design was sound.

---

## Phase 3 — LLM Verification

**What it does:** For borderline pairs (Phase 2 score 0.35–0.65), calls `gpt-4o-mini` to judge whether the repo genuinely implements the paper. Adjusts the score upward by +0.05 or +0.10 based on the verdict.

**Why only call the LLM for borderline scores?**

- Score < 0.35: clearly WEAK — no rule-based evidence, LLM confirmation adds no value
- Score > 0.65: already MEDIUM/STRONG from rules — LLM agreement would only nudge the score marginally

The LLM is only useful in the middle zone where rules are genuinely uncertain. This reduces LLM calls by ~80% and keeps cost around $0.41 for 2,750 pairs.

**What does the LLM see?**

Only the paper title, abstract (up to 500 chars), repo name, and README (first 1,000 chars). No source code, no file tree. This means the LLM is judging based on documentation quality, not implementation quality. A repo with a correct README but empty code files could still pass — this is a known limitation.

**Why results are cached:**

LLM calls are keyed on `paper_id|repo_url`. Re-running Phase 3 on the same dataset costs $0. This is important for iterative development where Phase 3 may be re-run after Phase 2 changes.

**Confidence assignment:**

After all signals (including LLM) are known, Phase 3 assigns a confidence label that answers: *"How much should we trust this score?"*

| Confidence | Meaning |
|---|---|
| HIGH | Multiple corroborating signals, no contradiction — score is reliable |
| MEDIUM | Some evidence but not conclusive |
| LOW | Contradiction detected, sparse repo, or very few signals |

Pairs with < 2 signals and outside the borderline range (never LLM-called) receive no confidence label — there is simply too little evidence to classify them. These are treated as implicitly LOW for downstream filtering.

---

## Phase 4 — Component Detection & Suitability

**What it does:** Inspects each cloned repo's file structure and code content to detect model, loss, and eval components. Uses these signals to determine which task types a repo supports.

**Why model, loss, and eval specifically?**

These are the three components that make a `missing_component` task coherent. A repo with a model but no loss is a natural "implement the loss" task. A repo with model + loss but no eval is a natural "implement the evaluation" task. Other components (data loaders, optimizers, visualization) are harder to detect reliably with generic heuristics and don't map cleanly to the task types we want.

**3-Layer detection:**

Rather than a binary detected/not-detected, each component gets a confidence tier:

| Layer | How | Confidence | What it means |
|---|---|---|---|
| 1 | Filename or directory named for the component (`model.py`, `models/`) | HIGH | Explicit, intentional naming |
| 2 | Keyword scan of first 50 lines of up to 30 code files | MEDIUM | Component is used in code but not explicitly named |
| 3 | ≥ 2 general ML structure directories present | LOW | Looks like an ML project, component identity unclear |

Only **MEDIUM or HIGH** confidence components count toward task suitability. LOW means the evidence is too weak — a repo with only a `train/` folder is not a reliable indicator of what components are present or absent.

**Why alignment is required for task suitability:**

A repo could have excellent code structure — detectable model and loss, eval scripts, config files — but be implementing a completely different paper than the one it's linked to in PWC. Without requiring MEDIUM+ alignment, we would generate tasks like "implement the loss function described in Paper X" applied to a repo that has nothing to do with Paper X. The paper provides the task specification; if it doesn't describe what the code does, it's not useful as a spec.

This was a key design fix: the initial version of Phase 4 had no alignment requirement for suitability. After adding it, 491 pairs were removed from the qualified pool — all had good code structure but WEAK alignment.

---

## Phase 5 — Calibration & Reports

**What it does:** Produces human-readable and machine-readable reports over the full dataset. Analyzes score distributions and threshold sensitivity.

**Why a separate calibration phase?**

The scoring thresholds (0.45 / 0.75) were set by design. Phase 5 validates that they're well-placed by checking whether the score distribution has natural gaps where the thresholds sit, and whether moving them would significantly change the qualified pool size. It also identifies borderline pairs for manual review.

This phase does not modify any data — it only reports. All output is in `output/phase5/`.

---

## Key Design Principles

**Rule-based first, LLM second.** Rule-based signals are fast, free, deterministic, and inspectable. The LLM is only used where rules are genuinely uncertain (0.35–0.65). This keeps costs low and makes the pipeline auditable.

**Alignment gates everything.** A repo without a well-aligned paper is useless for task generation regardless of code quality. The paper is the task specification — without alignment, there's no spec.

**Progressive enrichment.** Each phase adds fields to the same record. No phase discards data from a previous phase. This means the full reasoning trail is always available for debugging and review.

**Configured, not hardcoded.** All detection patterns (keywords, directory names, file extensions) live in `configs/patterns.yaml`. Tuning detection does not require touching pipeline logic.

---

## Current Results

After processing 2,750 pairs across 55 batches:

| Metric | Value |
|---|---|
| Pairs scored | 2,409 (87.6%) |
| STRONG alignment | 231 (9.6%) — almost all official |
| MEDIUM alignment | 1,127 (46.8%) |
| WEAK alignment | 1,051 (43.6%) — almost all non-official |
| Qualified for any task | **744 pairs (33.2%)** |
| — `missing_component` | 724 pairs |
| — `experiment_repair` | 115 pairs |

These 744 pairs are the input for Phase 6: Task Generation.

---

## Limitations & Future Directions

**Current limitations:**

- The LLM judges based on README content only, not actual code. A well-documented empty repo can pass.
- Layer 2 keyword patterns are PyTorch/TensorFlow-centric — repos in R, Julia, or MATLAB fall to Layer 3 (LOW confidence).
- `is_official` labeling in PWC is community-maintained and sometimes inconsistent.
- `experiment_repair` is rare (7.9%) because all three conditions (eval script + metric keywords + config) must be met simultaneously.

**Potential improvements:**

- **Code quality check**: verify that detected `.py` files have non-trivial content (actual class/function definitions beyond stubs), not just the right filenames
- **Dependency analysis**: parse `requirements.txt` or `setup.py` — a repo importing `torch`, `transformers`, `numpy` is a stronger ML signal than filename matching alone
- **Citation verification**: when a README links to arXiv, fetch the paper and confirm the title matches the PWC record — would catch READMEs that name a different paper
- **Phase 6 feedback loop**: after generating tasks, run a self-consistency check asking the LLM whether the task is solvable given the code, and filter tasks that aren't before human review
