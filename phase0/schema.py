"""
Output JSON schema for the PWC pipeline.
All pipeline phases write into this structure.
Fields are added progressively per phase — missing fields remain None.
"""

from typing import Optional
from pydantic import BaseModel, Field


# --- Phase 1: Paper Parsing ---

class PaperSemantics(BaseModel):
    task_hint: Optional[str] = None
    method_hint: Optional[str] = None
    domain_hint: Optional[str] = None
    abstract: Optional[str] = None
    keywords: list[str] = Field(default_factory=list)
    source: Optional[str] = None  # "title_extraction" | "arxiv_html" | "title_extraction+arxiv_html"


# --- Phase 2: Alignment Scoring ---

class LLMAlignment(BaseModel):
    level: Optional[str] = None   # STRONG | MEDIUM | WEAK
    reason: Optional[str] = None


class AlignmentResult(BaseModel):
    score: Optional[float] = None
    level: Optional[str] = None        # STRONG | MEDIUM | WEAK
    confidence: Optional[str] = None   # HIGH | MEDIUM | LOW
    has_contradiction: bool = False
    contradiction_note: Optional[str] = None
    signals_fired: list[str] = Field(default_factory=list)
    signal_count: int = 0
    llm_called: bool = False
    llm_alignment: Optional[LLMAlignment] = None


# --- Phase 4: Component Signals ---

class ComponentSignal(BaseModel):
    detected: bool = False
    confidence: Optional[str] = None   # HIGH | MEDIUM | LOW
    detection_layer: Optional[str] = None  # path | content | directory


class ComponentSignals(BaseModel):
    model: ComponentSignal = Field(default_factory=ComponentSignal)
    loss: ComponentSignal = Field(default_factory=ComponentSignal)
    eval: ComponentSignal = Field(default_factory=ComponentSignal)


class ExperimentSignals(BaseModel):
    has_eval_script: bool = False
    eval_confidence: Optional[str] = None
    metric_keywords: list[str] = Field(default_factory=list)
    metric_confidence: Optional[str] = None
    has_config: bool = False


# --- Phase 4: Readiness + Suitability ---

class ReadinessScore(BaseModel):
    score: Optional[float] = None
    level: Optional[str] = None  # HIGH | MEDIUM | LOW


class Readiness(BaseModel):
    missing_component: ReadinessScore = Field(default_factory=ReadinessScore)
    experiment_repair: ReadinessScore = Field(default_factory=ReadinessScore)


# --- Top-level pair record ---

class PairRecord(BaseModel):
    # Identity
    paper_id: Optional[str] = None
    paper_title: Optional[str] = None
    paper_arxiv_id: Optional[str] = None
    repo_url: Optional[str] = None
    is_official: Optional[bool] = None
    mentioned_in_paper: Optional[bool] = None
    mentioned_in_github: Optional[bool] = None

    # Phase 1: Paper parsing
    paper_fetch_success: Optional[bool] = None
    paper_fetch_error: Optional[str] = None
    paper_semantics: Optional[PaperSemantics] = None

    # Phase 1: Repo acquisition
    clone_success: Optional[bool] = None
    clone_error_type: Optional[str] = None   # timeout | not_found | private | size_too_large
    repo_too_large: bool = False
    repo_size_mb: Optional[float] = None

    # Phase 1: Repo pre-check
    repo_no_executable_code: bool = False   # only docs/supplementary — skip entirely
    repo_too_sparse: bool = False           # some code but < 3 files — LOW confidence
    executable_code_file_count: Optional[int] = None
    repo_has_readme: bool = False

    # Phase 2+3: Alignment
    alignment: Optional[AlignmentResult] = None

    # Phase 4: Component + experiment signals
    component_signals: Optional[ComponentSignals] = None
    experiment_signals: Optional[ExperimentSignals] = None
    readiness: Optional[Readiness] = None

    # Phase 4: Task suitability
    supported_tasks: list[str] = Field(default_factory=list)
