

from app.models.schemas import (
    AgentState,
    VerificationResult,
    VerificationEvidence
)


def normalize(text: str) -> str:
    return " ".join(
        str(text or "").lower().split()
    )


def evidence_text(evidence: dict) -> str:
    return normalize(
        " ".join([
            str(evidence.get("source", "")),
            str(evidence.get("document_title", "")),
            str(evidence.get("organization", "")),
            str(evidence.get("excerpt", "")),
            str(evidence.get("text", ""))
        ])
    )


def claim_matches_evidence(
    claim: str,
    evidence: dict
) -> bool:

    claim_text = normalize(claim)
    source_text = evidence_text(evidence)

    if not claim_text or not source_text:
        return False

    # Exact phrase
    if claim_text in source_text:
        return True

    # Important words from the claim
    words = [
        word
        for word in claim_text.split()
        if len(word) >= 4
    ]

    if not words:
        return False

    matches = sum(
        1
        for word in words
        if word in source_text
    )

    # Require reasonably strong lexical support.
    threshold = max(
        2,
        int(len(words) * 0.55)
    )

    return matches >= threshold


def make_verification_evidence(
    claim: str,
    evidence: dict
) -> VerificationEvidence:

    return VerificationEvidence(
        claim=claim,
        status="verified",
        evidence=str(
            evidence.get(
                "excerpt",
                evidence.get(
                    "text",
                    ""
                )
            )
        )
    )


def find_supporting_evidence(
    claim: str,
    research: list
):

    exact_matches = []

    for evidence in research:

        if not isinstance(evidence, dict):
            continue

        if claim_matches_evidence(
            claim,
            evidence
        ):
            exact_matches.append(
                evidence
            )

    return exact_matches


def collect_claims(
    state: AgentState
):

    claims = []

    eligibility = state.get(
        "eligibility",
        {}
    )

    documents = state.get(
        "documents",
        {}
    )

    regulations = state.get(
        "regulations",
        {}
    )

    procedure = state.get(
        "procedure",
        {}
    )

    # ------------------------------------------------
    # Eligibility processes
    # ------------------------------------------------

    for process in eligibility.get(
        "processes",
        []
    ):

        claims.append(process)

    # ------------------------------------------------
    # Document claims
    # ------------------------------------------------

    for document in documents.get(
        "documents",
        []
    ):

        claims.append(document)

    # ------------------------------------------------
    # Regulation claims
    # ------------------------------------------------

    for regulation in regulations.get(
        "regulations",
        []
    ):

        title = regulation.get(
            "title",
            ""
        )

        if title:
            claims.append(title)

    # ------------------------------------------------
    # Procedure claims
    # ------------------------------------------------

    for step in procedure.get(
        "steps",
        []
    ):

        title = step.get(
            "title",
            ""
        )

        if title:
            claims.append(title)

    # ------------------------------------------------
    # Remove duplicates
    # ------------------------------------------------

    unique_claims = []

    seen = set()

    for claim in claims:

        normalized = normalize(claim)

        if not normalized:
            continue

        if normalized in seen:
            continue

        seen.add(normalized)
        unique_claims.append(claim)

    return unique_claims


def verify_claims(
    state: AgentState
) -> VerificationResult:

    research = state.get(
        "research",
        []
    )

    claims = collect_claims(
        state
    )

    verified = []
    unsupported = []
    uncertainties = []

    for claim in claims:

        supporting = find_supporting_evidence(
            claim,
            research
        )

        if supporting:

            # Use the strongest available evidence.
            evidence = supporting[0]

            verified.append(
                make_verification_evidence(
                    claim,
                    evidence
                )
            )

        else:

            unsupported.append(
                VerificationEvidence(
                    claim=claim,
                    status="unsupported",
                    evidence=""
                )
            )

            uncertainties.append(
                f"No sufficiently matching research evidence "
                f"was found for claim: {claim}"
            )

    return VerificationResult(
        verified=verified,
        unsupported=unsupported,
        uncertainties=uncertainties
    )