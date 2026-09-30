# from pathlib import Path
# import json

# from qdrant_client.models import PointStruct

# from app.rag.vector_store import (
#     client,
#     COLLECTION_NAME,
#     create_collection
# )


# EMBEDDINGS_DIR = Path("data/embeddings")


# def load_embeddings():

#     create_collection()

#     points = []

#     for file in EMBEDDINGS_DIR.glob("*.json"):

#         print(f"Loading: {file.name}")

#         data = json.loads(
#             file.read_text(
#                 encoding="utf-8"
#             )
#         )

#         for item in data:

#             points.append(
#                 PointStruct(
#                     id=item["id"],
#                     vector=item["embedding"],
#                     payload={
#     "text": item["text"],
#     "source": item["source"],
#     "chunk_id": item["id"],

#     "organization": "Food Safety and Standards Authority of India",

#     "document_title": (
#         "Food Safety and Standards "
#         "(Licensing and Registration of Food Businesses) Regulations"
#     ),

#     "source_type": "government_regulation",

#     "official_url": None,

#     "publication_date": None,

#     "updated_date": None
# }
#                 )
#             )

#     if not points:

#         print("No embeddings found.")

#         return

#     client.upsert(
#         collection_name=COLLECTION_NAME,
#         points=points
#     )

#     print(
#         f"Inserted {len(points)} vectors into Qdrant."
#     )


# if __name__ == "__main__":
#     load_embeddings()
from pathlib import Path
import json
import uuid

from qdrant_client.models import PointStruct

from app.rag.vector_store import (
    client,
    COLLECTION_NAME,
    create_collection
)

from app.rag.source_registry import (
    get_source_metadata
)


EMBEDDINGS_DIR = Path("data/embeddings")


def identify_source(file_name: str):

    name = file_name.lower()

    if "fssai_foscos" in name:
        return "fssai_foscos"

    if name.startswith("fssai"):
        return "fssai"

    if "kerala_lsgd_trade_license" in name:
        return "kerala_lsgd_trade_license"

    if "kerala_kswift_know_your_approval" in name:
        return "kerala_kswift_kya"

    raise ValueError(
        f"Could not identify source for: {file_name}"
    )


def load_embeddings():

    create_collection()

    points = []

    for file in EMBEDDINGS_DIR.glob("*.json"):

        print(f"\nLoading: {file.name}")

        source_id = identify_source(
            file.name
        )

        metadata = get_source_metadata(
            source_id
        )

        print(
            f"Source: {metadata.organization}"
        )

        data = json.loads(
            file.read_text(
                encoding="utf-8"
            )
        )

        for item in data:

            chunk_id = item["id"]

            # Create deterministic globally unique ID
            point_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"{source_id}:{chunk_id}"
                )
            )

            points.append(
                PointStruct(
                    id=point_id,

                    vector=item["embedding"],

                    payload={

                        # Original chunk
                        "text": item["text"],

                        # Source identification
                        "source": source_id,
                        "chunk_id": chunk_id,

                        # Source metadata
                        "organization": (
                            metadata.organization
                        ),

                        "document_title": (
                            metadata.document_title
                        ),

                        "source_type": (
                            metadata.source_type
                        ),

                        "official_url": (
                            metadata.official_url
                        ),

                        "publication_date": (
                            metadata.publication_date
                        ),

                        "updated_date": (
                            metadata.updated_date
                        )
                    }
                )
            )

        print(
            f"Prepared {len(data)} chunks"
        )

    if not points:

        print(
            "No embeddings found."
        )

        return

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(
        f"\nInserted {len(points)} vectors "
        f"into Qdrant."
    )


if __name__ == "__main__":
    load_embeddings()