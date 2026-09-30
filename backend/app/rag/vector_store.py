# from qdrant_client import QdrantClient


# client = QdrantClient(
#     path="./qdrant_data"
# )

# COLLECTION_NAME = "government_documents"

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


# Local Qdrant database
client = QdrantClient(
    path="./qdrant_data"
)

COLLECTION_NAME = "government_documents"

VECTOR_SIZE = 384


def create_collection():

    collections = client.get_collections()

    existing_names = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME not in existing_names:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )

        print(
            f"Created collection: {COLLECTION_NAME}"
        )

    else:

        print(
            f"Collection already exists: "
            f"{COLLECTION_NAME}"
        )


if __name__ == "__main__":

    create_collection()