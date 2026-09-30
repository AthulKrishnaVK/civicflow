
from sentence_transformers import SentenceTransformer
import numpy as np


# ============================================================
# EMBEDDING MODEL
# ============================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(a, b):
    """
    Calculate cosine similarity between two vectors.
    """

    a = np.array(a)
    b = np.array(b)

    denominator = (
        np.linalg.norm(a) *
        np.linalg.norm(b)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(a, b) / denominator
    )


# ============================================================
# GENERIC CHUNK RELEVANCE
# ============================================================

def filter_relevant_chunks(
    query: str,
    chunks: list,
    top_k: int = 20,
    min_score: float = 0.30
):
    """
    Semantic relevance filtering for research chunks.

    Expected chunk:

    {
        "source": "...",
        "chunk_id": 0,
        "text": "...",
        "title": "...",
        "organization": "..."
    }
    """

    if not chunks:
        return []

    query = query.strip()

    if not query:
        return chunks[:top_k]

    # --------------------------------------------------------
    # Prepare valid chunks
    # --------------------------------------------------------

    valid_chunks = []

    texts = []

    for chunk in chunks:

        if not isinstance(
            chunk,
            dict
        ):
            continue

        text = chunk.get(
            "text",
            ""
        )

        if not text:
            continue

        valid_chunks.append(
            chunk
        )

        texts.append(
            text
        )

    if not valid_chunks:
        return []

    # --------------------------------------------------------
    # Generate embeddings
    # --------------------------------------------------------

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    chunk_embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    # --------------------------------------------------------
    # Score chunks
    # --------------------------------------------------------

    scored_chunks = []

    for chunk, embedding in zip(
        valid_chunks,
        chunk_embeddings
    ):

        score = cosine_similarity(
            query_embedding,
            embedding
        )

        chunk_copy = dict(
            chunk
        )

        chunk_copy["score"] = round(
            score,
            4
        )

        scored_chunks.append(
            chunk_copy
        )

    # --------------------------------------------------------
    # Sort by relevance
    # --------------------------------------------------------

    scored_chunks.sort(
        key=lambda x: x.get(
            "score",
            0
        ),
        reverse=True
    )

    # --------------------------------------------------------
    # Threshold
    # --------------------------------------------------------

    filtered = [
        chunk
        for chunk in scored_chunks
        if chunk.get(
            "score",
            0
        ) >= min_score
    ]

    # --------------------------------------------------------
    # Top K
    # --------------------------------------------------------

    filtered = filtered[
        :top_k
    ]

    print(
        f"Relevance filtering: "
        f"{len(chunks)} → "
        f"{len(filtered)} chunks"
    )

    return filtered


# ============================================================
# WEB RESEARCH COMPATIBILITY FUNCTION
# ============================================================

def filter_relevant_web_research(
    query: str,
    chunks: list,
    top_k: int = 20,
    min_score: float = 0.30
):
    """
    Compatibility wrapper used by research.py.

    This calls the generic chunk relevance filter.
    """

    return filter_relevant_chunks(
        query=query,
        chunks=chunks,
        top_k=top_k,
        min_score=min_score
    )