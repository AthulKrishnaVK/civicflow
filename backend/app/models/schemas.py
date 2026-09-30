

from typing import TypedDict

from pydantic import BaseModel


# =========================================================
# USER INTENT
# =========================================================

class UserIntent(BaseModel):

    goal: str

    location: str

    domain: str

    process_type: str

    requires_research: bool


# =========================================================
# SOURCE DISCOVERY
# =========================================================

class GovernmentSource(BaseModel):

    title: str

    url: str

    organization: str

    reason: str

    source_type: str


class SourceDiscoveryResult(BaseModel):

    search_queries: list[str]

    sources: list[GovernmentSource]

    uncertainties: list[str]


# =========================================================
# EVIDENCE
# =========================================================

class EvidenceReference(BaseModel):

    source: str

    chunk_id: int

    excerpt: str

    organization: str | None = None

    document_title: str | None = None

    source_type: str | None = None

    official_url: str | None = None

    publication_date: str | None = None

    updated_date: str | None = None


class EligibilityEvidence(EvidenceReference):

    process: str


class DocumentEvidence(EvidenceReference):

    pass


class RegulationEvidence(EvidenceReference):

    pass


class ProcedureEvidence(EvidenceReference):

    pass


# =========================================================
# ELIGIBILITY
# =========================================================

class EligibilityResult(BaseModel):

    applicable: bool

    processes: list[str]

    conditions: list[str]

    missing_information: list[str]

    evidence: list[EligibilityEvidence]

    uncertainties: list[str]


# =========================================================
# DOCUMENTS
# =========================================================

class DocumentResult(BaseModel):

    documents: list[str]

    evidence: list[DocumentEvidence]

    uncertainties: list[str]


# =========================================================
# REGULATIONS
# =========================================================

class RegulationItem(BaseModel):

    title: str

    description: str


class RegulationResult(BaseModel):

    regulations: list[RegulationItem]

    evidence: list[RegulationEvidence]

    uncertainties: list[str]


# =========================================================
# PROCEDURE
# =========================================================

class ProcedureStep(BaseModel):

    step: int

    title: str

    description: str

    required_documents: list[str]

    evidence: list[ProcedureEvidence]


class ProcedureResult(BaseModel):

    steps: list[ProcedureStep]

    uncertainties: list[str]


# =========================================================
# VERIFICATION
# =========================================================

class VerificationEvidence(BaseModel):

    claim: str

    status: str

    evidence: str


class VerificationResult(BaseModel):

    verified: list[VerificationEvidence]

    unsupported: list[VerificationEvidence]

    uncertainties: list[str]


# =========================================================
# LANGGRAPH STATE
# =========================================================

class AgentState(TypedDict):

    user_input: str

    intent: dict

    sources: list

    eligibility: dict

    research: list

    documents: dict

    regulations: dict

    procedure: dict

    verification: dict