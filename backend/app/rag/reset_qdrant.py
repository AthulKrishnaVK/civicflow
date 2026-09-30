from app.rag.vector_store import (
    client,
    COLLECTION_NAME
)


if __name__ == "__main__":

    collections = client.get_collections()

    names = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME in names:

        print(
            f"Deleting collection: "
            f"{COLLECTION_NAME}"
        )

        client.delete_collection(
            collection_name=COLLECTION_NAME
        )

        print("Collection deleted.")

    else:

        print(
            "Collection does not exist."
        )