
import json
import re
import os

from dotenv import load_dotenv
from groq import Groq

from app.models.schemas import EligibilityResult


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_json(content: str):

    if not content:
        raise ValueError(
            "Eligibility Agent returned an empty response."
        )

    content = content.strip()

    content = re.sub(
        r"^```json\s*",
        "",
        content,
        flags=re.IGNORECASE
    )

    content = re.sub(
        r"\s*```$",
        "",
        content
    )

    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "Eligibility Agent did not return JSON."
        )

    return json.loads(
        content[start:end + 1]
    )


def normalize_text(text):

    return " ".join(
        str(text).split()
    ).lower()


def find_matching_evidence(
    source,
    chunk_id,
    excerpt,
    research_lookup
):

    original = research_lookup.get(
        (
            source,
            chunk_id
        )
    )

    if original is None:
        return None

    original_text = original.get(
        "text",
        ""
    )

    # Exact match
    if excerpt in original_text:
        return original

    # Normalized match
    normalized_excerpt = normalize_text(
        excerpt
    )

    normalized_original = normalize_text(
        original_text
    )

    if (
        normalized_excerpt
        and normalized_excerpt in normalized_original
    ):
        return original

    return None


def analyze_eligibility(state):

    research = state.get(
        "research",
        []
    )

    user_input = state.get(
        "user_input",
        ""
    )

    intent = state.get(
        "intent",
        {}
    )

    if not research:

        return EligibilityResult(
            applicable=False,
            processes=[],
            conditions=[],
            missing_information=[
                "No government research evidence was available."
            ],
            evidence=[],
            uncertainties=[
                "Eligibility could not be determined."
            ]
        )

    # --------------------------------------------------
    # Build lookup from ALL research
    # --------------------------------------------------

    research_lookup = {}

    for item in research:

        key = (
            str(
                item.get(
                    "source",
                    ""
                )
            ),
            int(
                item.get(
                    "chunk_id",
                    0
                )
            )
        )

        research_lookup[key] = item

    # --------------------------------------------------
    # Prepare research context
    # --------------------------------------------------

    research_context = research[:10]

    context = []

    for item in research_context:

        context.append({
            "source": item.get(
                "source",
                ""
            ),
            "chunk_id": item.get(
                "chunk_id",
                0
            ),
            "text": item.get(
                "text",
                ""
            )[:1500]
        })

    prompt = f"""
You are the Eligibility Agent for CivicFlow.

Determine which government processes
are applicable to the user's request.

USER REQUEST:
{user_input}

USER INTENT:
{json.dumps(
    intent,
    ensure_ascii=False,
    indent=2
)}

RESEARCH EVIDENCE:
{json.dumps(
    context,
    ensure_ascii=False,
    indent=2
)}

RULES:

1. Use ONLY supplied evidence.
2. Do not invent requirements.
3. Identify applicable government processes.
4. Identify conditions supported by evidence.
5. Identify information that is still missing.
6. Every process must have supporting evidence.
7. For evidence, COPY A CONTIGUOUS SENTENCE
   OR SENTENCE-LIKE PASSAGE from the supplied
   research text.
8. Do not paraphrase evidence.
9. source and chunk_id MUST exactly match
   the supplied evidence.
10. Do not invent URLs or metadata.
11. Return ONLY valid JSON.

IMPORTANT:

If the evidence says that a system can identify
licenses or approvals, do NOT claim that a specific
license is mandatory unless the supplied evidence
explicitly establishes that.

Return exactly:

{{
    "applicable": true,
    "processes": [
        {{
            "process": "process name",
            "source": "source identifier",
            "chunk_id": 0,
            "excerpt": "exact contiguous evidence passage"
        }}
    ],
    "conditions": [
        "condition"
    ],
    "missing_information": [
        "missing information"
    ]
}}
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Determine eligibility only "
                        "from supplied government evidence. "
                        "Never invent requirements. "
                        "Return valid JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            reasoning_effort="low",
            max_completion_tokens=900
        )

        result = extract_json(
            response.choices[0].message.content
        )

    except Exception as e:

        print(
            "\n===== ELIGIBILITY JSON ERROR ====="
        )

        print(str(e))

        print(
            "==================================\n"
        )

        return EligibilityResult(
            applicable=False,
            processes=[],
            conditions=[],
            missing_information=[],
            evidence=[],
            uncertainties=[
                "Eligibility analysis failed."
            ]
        )

    # --------------------------------------------------
    # Validate evidence
    # --------------------------------------------------

    evidence = []

    for item in result.get(
        "processes",
        []
    ):

        if not isinstance(
            item,
            dict
        ):
            continue

        process = str(
            item.get(
                "process",
                ""
            )
        ).strip()

        source = str(
            item.get(
                "source",
                ""
            )
        ).strip()

        try:

            chunk_id = int(
                item.get(
                    "chunk_id",
                    0
                )
            )

        except Exception:

            continue

        excerpt = str(
            item.get(
                "excerpt",
                ""
            )
        ).strip()

        if (
            not process
            or not source
            or not excerpt
        ):
            continue

        original = find_matching_evidence(
            source,
            chunk_id,
            excerpt,
            research_lookup
        )

        if original is None:
            continue

        evidence.append({
            "process": process,
            "source": source,
            "chunk_id": chunk_id,
            "excerpt": excerpt,
            "organization": original.get(
                "organization"
            ),
            "document_title": original.get(
                "document_title"
            ),
            "source_type": original.get(
                "source_type"
            ),
            "official_url": original.get(
                "official_url"
            ),
            "publication_date": original.get(
                "publication_date"
            ),
            "updated_date": original.get(
                "updated_date"
            )
        })

    # --------------------------------------------------
    # Derive processes ONLY from validated evidence
    # --------------------------------------------------

    processes = list(
        dict.fromkeys(
            item["process"]
            for item in evidence
            if item.get("process")
        )
    )

    conditions = [
        str(condition).strip()
        for condition in result.get(
            "conditions",
            []
        )
        if str(condition).strip()
    ]

    missing_information = [
        str(item).strip()
        for item in result.get(
            "missing_information",
            []
        )
        if str(item).strip()
    ]

    uncertainties = []

    if not evidence:

        uncertainties.append(
            "No applicable government process "
            "could be validated from the evidence."
        )

    return EligibilityResult(
        applicable=bool(
            result.get(
                "applicable",
                False
            )
        ),
        processes=processes,
        conditions=conditions,
        missing_information=missing_information,
        evidence=evidence,
        uncertainties=uncertainties
    )