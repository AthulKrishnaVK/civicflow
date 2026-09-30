

import json
import os
import time

from dotenv import load_dotenv
from groq import Groq

from app.models.schemas import RegulationResult


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ============================================================
# TEXT HELPERS
# ============================================================

def normalize_text(text):
    return " ".join(
        str(text).lower().split()
    )


def find_excerpt(
    text,
    keywords,
    max_length=500
):
    """
    Find a useful evidence sentence/section from
    the original research text.

    This is deterministic: the excerpt always
    comes from the original evidence.
    """

    if not text:
        return ""

    normalized = normalize_text(text)

    # Find the first keyword occurrence
    positions = []

    for keyword in keywords:

        position = normalized.find(
            keyword.lower()
        )

        if position >= 0:
            positions.append(position)

    if not positions:
        return ""

    start = min(positions)

    # Map normalized position approximately back
    # to original text.
    words = text.split()

    # Simple deterministic extraction
    selected = []

    current_length = 0

    for word in words:

        if current_length >= max_length:
            break

        selected.append(word)

        current_length += (
            len(word) + 1
        )

    excerpt = " ".join(
        selected
    )

    return excerpt.strip()


# ============================================================
# LLM REGULATION CLASSIFICATION
# ============================================================

def classify_regulations(
    user_input,
    research
):

    context = []

    for index, item in enumerate(
        research[:12]
    ):

        text = item.get(
            "text",
            ""
        )

        if not text:
            continue

        context.append({

            "research_index": index,

            "text": text[:900]

        })

    if not context:

        return []


    prompt = f"""
You are a government regulation classification agent.

USER REQUEST:
{user_input}

RESEARCH EVIDENCE:
{json.dumps(
    context,
    ensure_ascii=False
)}

Identify which research chunks contain explicit:

- regulations
- statutory requirements
- mandatory compliance requirements
- licensing requirements
- registration requirements
- mandatory government conditions

IMPORTANT:

Use ONLY the supplied evidence.

Do NOT write explanations.

Do NOT copy excerpts.

Do NOT generate URLs.

Do NOT generate metadata.

Return ONLY a compact JSON object.

The value of research_index must refer to the supplied
research_index.

Format:

{{
  "items": [
    {{
      "research_index": 0,
      "title": "short title"
    }}
  ]
}}

If there are no clearly supported regulations:

{{
  "items": []
}}
"""

    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[

                {
                    "role": "system",
                    "content": (
                        "Classify government "
                        "requirements from evidence. "
                        "Return compact JSON only."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0,

            reasoning_effort="low",

            max_completion_tokens=250
        )

        raw = (
            response
            .choices[0]
            .message
            .content
        )

        print(
            "\n===== REGULATION CLASSIFICATION ====="
        )

        print(
            raw
        )

        print(
            "======================================"
        )

        if not raw:
            return []

        raw = raw.strip()

        # Remove markdown fences
        if raw.startswith("```"):

            raw = raw.replace(
                "```json",
                ""
            )

            raw = raw.replace(
                "```",
                ""
            )

            raw = raw.strip()

        start = raw.find("{")
        end = raw.rfind("}")

        if start < 0 or end < 0:
            return []

        data = json.loads(
            raw[start:end + 1]
        )

        items = data.get(
            "items",
            []
        )

        if not isinstance(
            items,
            list
        ):
            return []

        return items

    except Exception as e:

        print(
            "\nRegulation classification error:",
            e
        )

        return []


# ============================================================
# MAIN REGULATION AGENT
# ============================================================

def analyze_regulations(state):

    research = state.get(
        "research",
        []
    )

    user_input = state.get(
        "user_input",
        ""
    )

    if not research:

        return RegulationResult(

            regulations=[],

            evidence=[],

            uncertainties=[
                "No research evidence was available."
            ]

        )


    # ========================================================
    # STEP 1
    # Ask LLM ONLY to identify relevant chunks.
    # ========================================================

    classifications = classify_regulations(
        user_input,
        research
    )


    regulations = []

    evidence = []

    seen = set()


    # ========================================================
    # STEP 2
    # Python retrieves original evidence.
    # ========================================================

    for item in classifications:

        if not isinstance(
            item,
            dict
        ):
            continue

        try:

            index = int(
                item.get(
                    "research_index",
                    -1
                )
            )

        except Exception:

            continue


        if (
            index < 0
            or index >= len(research)
        ):
            continue


        original = research[
            index
        ]


        text = original.get(
            "text",
            ""
        )

        if not text:
            continue


        title = str(
            item.get(
                "title",
                ""
            )
        ).strip()


        if not title:
            continue


        source = original.get(
            "source",
            ""
        )

        chunk_id = original.get(
            "chunk_id",
            0
        )


        # ----------------------------------------------------
        # Prevent duplicates
        # ----------------------------------------------------

        key = (
            title.lower(),
            source,
            chunk_id
        )

        if key in seen:
            continue

        seen.add(key)


        # ----------------------------------------------------
        # Evidence excerpt
        #
        # IMPORTANT:
        # The excerpt is generated from the ORIGINAL
        # research item, not invented by the LLM.
        # ----------------------------------------------------

        lower_text = text.lower()

        if (
            "food business operator"
            in lower_text
        ):

            excerpt = text[:1000]

        elif (
            "licence"
            in lower_text
            or "license"
            in lower_text
        ):

            excerpt = text[:1000]

        elif (
            "registration"
            in lower_text
        ):

            excerpt = text[:1000]

        elif (
            "mandatory"
            in lower_text
        ):

            excerpt = text[:1000]

        else:

            excerpt = text[:700]


        excerpt = excerpt.strip()


        if not excerpt:
            continue


        # ----------------------------------------------------
        # Add regulation
        # ----------------------------------------------------

        regulations.append({

            "title": title,

            "description": (
                "The supplied government evidence "
                "indicates this requirement."
            )

        })


        # ----------------------------------------------------
        # Attach trusted metadata
        # ----------------------------------------------------

        evidence.append({

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


    # ========================================================
    # STEP 3
    # If LLM misses regulations, use deterministic
    # evidence detection as a fallback.
    # ========================================================

    if not regulations:

        for index, item in enumerate(
            research
        ):

            text = item.get(
                "text",
                ""
            )

            if not text:
                continue

            lower = text.lower()


            # ----------------------------------------------
            # FSSAI registration requirement
            # ----------------------------------------------

            if (
                "food business operator"
                in lower
                and "register"
                in lower
                and "form a"
                in lower
            ):

                title = (
                    "FSSAI Food Business Registration Requirement"
                )

                key = (
                    title,
                    item.get("source", ""),
                    item.get("chunk_id", 0)
                )

                if key not in seen:

                    regulations.append({

                        "title": title,

                        "description": (
                            "Food Business Operators "
                            "covered by the supplied "
                            "evidence must register "
                            "or obtain the applicable "
                            "food licence."
                        )

                    })

                    evidence.append({

                        "source": item.get(
                            "source",
                            ""
                        ),

                        "chunk_id": item.get(
                            "chunk_id",
                            0
                        ),

                        "excerpt": text[:1000],

                        "organization": item.get(
                            "organization"
                        ),

                        "document_title": item.get(
                            "document_title"
                        ),

                        "source_type": item.get(
                            "source_type"
                        ),

                        "official_url": item.get(
                            "official_url"
                        ),

                        "publication_date": item.get(
                            "publication_date"
                        ),

                        "updated_date": item.get(
                            "updated_date"
                        )

                    })

                    seen.add(key)

                    break


            # ----------------------------------------------
            # Kerala trade licence requirement
            # ----------------------------------------------

            if (
                (
                    "trade license"
                    in lower
                )
                or
                (
                    "trade licence"
                    in lower
                )
            ):

                if (
                    "licence is required"
                    in lower
                    or
                    "license is required"
                    in lower
                ):

                    title = (
                        "Kerala Local Government "
                        "Trade Licence Requirement"
                    )

                    key = (
                        title,
                        item.get("source", ""),
                        item.get("chunk_id", 0)
                    )

                    if key not in seen:

                        regulations.append({

                            "title": title,

                            "description": (
                                "The supplied Kerala "
                                "Local Self Government "
                                "evidence states that "
                                "a licence is required "
                                "for covered trades "
                                "and activities."
                            )

                        })

                        evidence.append({

                            "source": item.get(
                                "source",
                                ""
                            ),

                            "chunk_id": item.get(
                                "chunk_id",
                                0
                            ),

                            "excerpt": text[:1000],

                            "organization": item.get(
                                "organization"
                            ),

                            "document_title": item.get(
                                "document_title"
                            ),

                            "source_type": item.get(
                                "source_type"
                            ),

                            "official_url": item.get(
                                "official_url"
                            ),

                            "publication_date": item.get(
                                "publication_date"
                            ),

                            "updated_date": item.get(
                                "updated_date"
                            )

                        })

                        seen.add(key)

                        break


    # ========================================================
    # FINAL RESULT
    # ========================================================

    uncertainties = []


    if not regulations:

        uncertainties.append(
            "No regulations were identified "
            "from the available evidence."
        )


    return RegulationResult(

        regulations=regulations,

        evidence=evidence,

        uncertainties=uncertainties

    )