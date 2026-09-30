from app.rag.retrieval import search_documents


def find_evidence(
    query: str,
    limit: int = 5
):

    results = search_documents(
        query,
        limit=limit
    )

    evidence = []

    for item in results:

        evidence.append({
            "source": item.get(
                "source",
                ""
            ),

            "chunk_id": item.get(
                "chunk_id",
                0
            ),

            "excerpt": item.get(
                "text",
                ""
            )[:500],

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
            )
        })

    return evidence