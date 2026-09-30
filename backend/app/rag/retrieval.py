from sentence_transformers import SentenceTransformer

from app.rag.vector_store import (
    client,
    COLLECTION_NAME
)


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def search_documents(
    query: str,
    limit: int = 5
):

    query_vector = model.encode(
        query
    ).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True
    )

    documents = []

    for result in results.points:

        payload = result.payload

        documents.append({

            # Retrieved content
            "text": payload.get(
                "text",
                ""
            ),

            # Source identification
            "source": payload.get(
                "source",
                ""
            ),

            "chunk_id": payload.get(
                "chunk_id",
                0
            ),

            # Retrieval score
            "score": result.score,

            # Source metadata
            "organization": payload.get(
                "organization"
            ),

            "document_title": payload.get(
                "document_title"
            ),

            "source_type": payload.get(
                "source_type"
            ),

            "official_url": payload.get(
                "official_url"
            ),

            "publication_date": payload.get(
                "publication_date"
            ),

            "updated_date": payload.get(
                "updated_date"
            )
        })

    return documents