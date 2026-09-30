

from app.rag.retrieval import search_documents
from app.agents.web_search import fetch_sources
from app.agents.relevance import filter_relevant_web_research


def research_agent(state):

    user_input = state.get(
        "user_input",
        ""
    )

    intent = state.get(
        "intent",
        {}
    )

    sources = state.get(
        "sources",
        []
    )

    # ==================================================
    # 1. QDRANT RESEARCH
    # ==================================================

    query = f"""
User goal:
{user_input}

Location:
{intent.get("location", "")}

Domain:
{intent.get("domain", "")}

Process type:
{intent.get("process_type", "")}

Find government evidence relevant to this request.

Focus on:
- eligibility
- approvals
- registrations
- licenses
- procedures
- documents
- regulations
- fees
- application processes
"""

    qdrant_results = search_documents(
        query,
        limit=10
    )

    research = []

    for item in qdrant_results:

        research.append({
            "text": item.get(
                "text",
                ""
            ),
            "source": item.get(
                "source",
                ""
            ),
            "chunk_id": item.get(
                "chunk_id",
                0
            ),
            "score": item.get(
                "score",
                0
            ),
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
            ),
            "research_source": "qdrant"
        })

    # ==================================================
    # 2. LIVE OFFICIAL WEB RESEARCH
    # ==================================================

    web_research = []

    if sources:

        print(
            "\n===== FETCHING DISCOVERED SOURCES ====="
        )

        web_results = fetch_sources(
            sources,
            user_input=user_input
        )

        print(
            f"\nFetched {len(web_results)} relevant "
            f"web chunks."
        )

        # fetch_sources() already returns a FLAT LIST
        # of chunks.
        #
        # Do NOT expect:
        # {
        #     "source": {...},
        #     "chunks": [...]
        # }

        for item in web_results:

            if not isinstance(
                item,
                dict
            ):
                continue

            text = item.get(
                "text",
                ""
            )

            if not text:
                continue

            web_research.append({

                "text": text,

                "source": item.get(
                    "source",
                    ""
                ),

                "chunk_id": item.get(
                    "chunk_id",
                    0
                ),

                "score": item.get(
                    "score",
                    0
                ),

                "organization": item.get(
                    "organization",
                    ""
                ),

                "document_title": item.get(
                    "title",
                    ""
                ),

                "source_type": item.get(
                    "source_type",
                    "government_web_source"
                ),

                "official_url": item.get(
                    "source",
                    ""
                ),

                "publication_date": item.get(
                    "publication_date"
                ),

                "updated_date": item.get(
                    "updated_date"
                ),

                "research_source": "web"
            })

        print(
            f"Raw web research chunks: "
            f"{len(web_research)}"
        )

    # ==================================================
    # 3. WEB RELEVANCE
    # ==================================================

    if web_research:

        print(
            "\n===== WEB RESEARCH RELEVANCE FILTER ====="
        )

        relevance_query = f"""
User goal:
{user_input}

Location:
{intent.get("location", "")}

Domain:
{intent.get("domain", "")}

Process:
{intent.get("process_type", "")}

Find evidence about:
eligibility, government approvals,
registrations, licenses, documents,
procedures and regulations.
"""

        relevant_web_research = (
            filter_relevant_web_research(
                query=relevance_query,
                chunks=web_research,
                top_k=20,
                min_score=0.30
            )
        )

        print(
            "Relevant web chunks: "
            f"{len(relevant_web_research)}"
        )

        for item in relevant_web_research[:10]:

            print(
                f"\nScore: "
                f"{item.get('score', 0)}"
            )

            print(
                f"Source: "
                f"{item.get('official_url', '')}"
            )

            print(
                f"Text: "
                f"{item.get('text', '')[:250]}"
            )

        research.extend(
            relevant_web_research
        )

    # ==================================================
    # 4. REMOVE DUPLICATE RESEARCH
    # ==================================================

    unique_research = []

    seen = set()

    for item in research:

        text = item.get(
            "text",
            ""
        ).strip()

        source = item.get(
            "source",
            ""
        )

        chunk_id = item.get(
            "chunk_id",
            0
        )

        key = (
            source,
            chunk_id,
            text[:200]
        )

        if key in seen:
            continue

        seen.add(key)

        unique_research.append(
            item
        )

    research = unique_research

    # ==================================================
    # 5. FINAL SUMMARY
    # ==================================================

    print(
        "\n===== RESEARCH SUMMARY ====="
    )

    print(
        f"Qdrant results: "
        f"{len(qdrant_results)}"
    )

    print(
        f"Raw web chunks: "
        f"{len(web_research)}"
    )

    print(
        f"Final research items: "
        f"{len(research)}"
    )

    print(
        "============================\n"
    )

    return {
        "research": research
    }