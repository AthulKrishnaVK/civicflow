

from app.models.schemas import (
    AgentState,
    ProcedureResult,
    ProcedureStep,
    ProcedureEvidence
)


def normalize(text: str) -> str:
    return " ".join(
        str(text or "").lower().split()
    )


def evidence_matches_process(
    evidence: dict,
    process: str
) -> bool:

    process_text = normalize(process)

    evidence_text = normalize(
        " ".join([
            str(evidence.get("source", "")),
            str(evidence.get("document_title", "")),
            str(evidence.get("organization", "")),
            str(evidence.get("excerpt", "")),
            str(evidence.get("text", ""))
        ])
    )

    keywords = [
        word
        for word in process_text.split()
        if len(word) > 3
    ]

    if not keywords:
        return False

    matches = sum(
        1
        for keyword in keywords
        if keyword in evidence_text
    )

    return matches >= min(2, len(keywords))


def make_procedure_evidence(
    evidence: dict
) -> ProcedureEvidence:

    return ProcedureEvidence(
        source=str(
            evidence.get(
                "source",
                "unknown"
            )
        ),
        chunk_id=int(
            evidence.get(
                "chunk_id",
                0
            )
        ),
        excerpt=str(
            evidence.get(
                "excerpt",
                evidence.get(
                    "text",
                    ""
                )
            )
        ),
        organization=evidence.get(
            "organization"
        ),
        document_title=evidence.get(
            "document_title"
        ),
        source_type=evidence.get(
            "source_type"
        ),
        official_url=evidence.get(
            "official_url"
        ),
        publication_date=evidence.get(
            "publication_date"
        ),
        updated_date=evidence.get(
            "updated_date"
        )
    )


def find_evidence_for_process(
    process: str,
    research: list,
    eligibility: dict
):

    matched = []

    # ------------------------------------------------
    # 1. Eligibility evidence
    # ------------------------------------------------

    for evidence in eligibility.get(
        "evidence",
        []
    ):

        if evidence_matches_process(
            evidence,
            process
        ):
            matched.append(evidence)


    # ------------------------------------------------
    # 2. Research evidence
    # ------------------------------------------------

    for evidence in research:

        if evidence_matches_process(
            evidence,
            process
        ):
            matched.append(evidence)


    # ------------------------------------------------
    # Remove duplicate evidence
    # ------------------------------------------------

    unique = []
    seen = set()

    for evidence in matched:

        key = (
            evidence.get("source"),
            evidence.get("chunk_id")
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(evidence)

    return unique


def build_fssai_steps(
    evidence: list
):

    if not evidence:
        return []

    primary = evidence[0]

    return [
        ProcedureStep(
            step=1,
            title="Determine the applicable FSSAI registration category",
            description=(
                "Confirm that the food business qualifies for "
                "the petty food business registration category "
                "before proceeding with the registration."
            ),
            required_documents=[],
            evidence=[
                make_procedure_evidence(primary)
            ]
        ),

        ProcedureStep(
            step=2,
            title="Prepare the FSSAI registration application",
            description=(
                "Submit the registration application in Form A "
                "under the applicable food-business regulations "
                "and provide the required fee and supporting "
                "declaration where applicable."
            ),
            required_documents=[
                "Form A",
                "Applicable fee",
                "Self-attested declaration of hygiene and safety compliance"
            ],
            evidence=[
                make_procedure_evidence(primary)
            ]
        ),

        ProcedureStep(
            step=3,
            title="Complete the FSSAI registration process",
            description=(
                "Submit the application through the applicable "
                "FSSAI registration process and retain the "
                "resulting registration information."
            ),
            required_documents=[],
            evidence=[
                make_procedure_evidence(primary)
            ]
        )
    ]


def build_trade_license_steps(
    evidence: list
):

    if not evidence:
        return []

    primary = evidence[0]

    return [
        ProcedureStep(
            step=1,
            title="Identify the responsible local government body",
            description=(
                "The trade licence is obtained through the "
                "relevant local self-government body."
            ),
            required_documents=[],
            evidence=[
                make_procedure_evidence(primary)
            ]
        ),

        ProcedureStep(
            step=2,
            title="Apply for the local government trade licence",
            description=(
                "Submit the application for the required trade "
                "licence through the applicable local-government "
                "digital service."
            ),
            required_documents=[],
            evidence=[
                make_procedure_evidence(primary)
            ]
        ),

        ProcedureStep(
            step=3,
            title="Complete the trade licence process",
            description=(
                "Complete the application and payment process "
                "through the applicable local-government portal "
                "and retain the issued licence."
            ),
            required_documents=[],
            evidence=[
                make_procedure_evidence(primary)
            ]
        )
    ]


def analyze_procedure(
    state: AgentState
) -> ProcedureResult:

    eligibility = state.get(
        "eligibility",
        {}
    )

    research = state.get(
        "research",
        []
    )

    processes = eligibility.get(
        "processes",
        []
    )

    all_steps = []
    uncertainties = []

    next_step_number = 1

    for process in processes:

        process_evidence = find_evidence_for_process(
            process,
            research,
            eligibility
        )

        process_lower = normalize(process)

        # --------------------------------------------
        # FSSAI food registration
        # --------------------------------------------

        if (
            "fssai" in process_lower
            or "food business registration" in process_lower
            or "petty food" in process_lower
        ):

            steps = build_fssai_steps(
                process_evidence
            )

            for step in steps:
                step.step = next_step_number
                next_step_number += 1
                all_steps.append(step)

            if not steps:
                uncertainties.append(
                    "No sufficiently supported evidence was found "
                    f"to construct the procedure for: {process}"
                )

        # --------------------------------------------
        # Kerala local government trade licence
        # --------------------------------------------

        elif (
            "trade license" in process_lower
            or "trade licence" in process_lower
            or "local government" in process_lower
        ):

            steps = build_trade_license_steps(
                process_evidence
            )

            for step in steps:
                step.step = next_step_number
                next_step_number += 1
                all_steps.append(step)

            if not steps:
                uncertainties.append(
                    "No sufficiently supported evidence was found "
                    f"to construct the procedure for: {process}"
                )

        # --------------------------------------------
        # Unknown process
        # --------------------------------------------

        else:

            uncertainties.append(
                "The process was identified, but a deterministic "
                f"procedure template has not yet been implemented "
                f"for: {process}"
            )

    # ------------------------------------------------
    # If no procedure could be constructed
    # ------------------------------------------------

    if not all_steps:

        uncertainties.append(
            "No procedure steps could be constructed from "
            "the currently validated government evidence."
        )

    return ProcedureResult(
        steps=all_steps,
        uncertainties=uncertainties
    )