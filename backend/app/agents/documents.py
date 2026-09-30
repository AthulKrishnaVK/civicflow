

import json
import re

from groq import Groq
import os

from dotenv import load_dotenv

from app.models.schemas import DocumentResult

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_json(content: str):

    if not content:
        raise ValueError(
            "Document Agent returned an empty response."
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
            "Document Agent did not return JSON."
        )

    return json.loads(
        content[start:end + 1]
    )


def analyze_documents(state):

    research = state.get(
        "research",
        []
    )

    user_input = state.get(
        "user_input",
        ""
    )

    if not research:

        return DocumentResult(
            documents=[],
            evidence=[],
            uncertainties=[
                "No research evidence was available."
            ]
        )

    # Keep the context reasonably small
    research_context = research[:12]

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
            )
        })

    prompt = f"""
You are the Document Agent for CivicFlow.

Identify the government documents,
forms, declarations, certificates,
or other documentation that the user
may need for their government process.

USER REQUEST:
{user_input}

RESEARCH EVIDENCE:
{json.dumps(
    context,
    ensure_ascii=False,
    indent=2
)}

IMPORTANT:

Only identify documents that are supported
by the supplied research evidence.

Do not invent documents.

For every document provide:

1. name
2. source
3. chunk_id
4. excerpt

The excerpt must be copied from the
supplied research evidence.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "documents": [
        {{
            "name": "document name",
            "source": "source identifier",
            "chunk_id": 0,
            "excerpt": "exact supporting excerpt"
        }}
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
                        "Identify government documents "
                        "only from supplied evidence. "
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
            max_completion_tokens=1400
        )

        result = extract_json(
            response.choices[0].message.content
        )

    except Exception as e:

        print(
            "\n===== DOCUMENT JSON ERROR ====="
        )

        print(str(e))

        print(
            "================================\n"
        )

        return DocumentResult(
            documents=[],
            evidence=[],
            uncertainties=[
                "The document analysis returned invalid JSON."
            ]
        )

    # --------------------------------------------------
    # Build lookup table from original research
    # --------------------------------------------------

    research_lookup = {}

    for item in research:

        key = (
            str(item.get("source", "")),
            int(item.get("chunk_id", 0))
        )

        research_lookup[key] = item

    documents = []
    evidence = []

    # --------------------------------------------------
    # Validate LLM output
    # --------------------------------------------------

    for item in result.get(
        "documents",
        []
    ):

        if not isinstance(item, dict):
            continue

        name = str(
            item.get(
                "name",
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

        if not name or not source or not excerpt:
            continue

        key = (
            source,
            chunk_id
        )

        original = research_lookup.get(
            key
        )

        if original is None:
            continue

        original_text = original.get(
            "text",
            ""
        )

        # Evidence must actually exist
        if excerpt not in original_text:
            continue

        # Store only the document name
        documents.append(name)

        # Metadata comes from research,
        # NOT from the LLM
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

    # Remove duplicate document names
    documents = list(
        dict.fromkeys(documents)
    )

    uncertainties = []

    if not documents:

        uncertainties.append(
            "No government documents were "
            "identified from the available evidence."
        )

    return DocumentResult(
        documents=documents,
        evidence=evidence,
        uncertainties=uncertainties
    )