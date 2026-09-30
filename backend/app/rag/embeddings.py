from pathlib import Path
import json

from sentence_transformers import SentenceTransformer


PROCESSED_DIR = Path("data/processed")
OUTPUT_DIR = Path("data/embeddings")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# Local embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embeddings():

    for file in PROCESSED_DIR.glob("*.md"):

        print(f"Embedding: {file.name}")

        text = file.read_text(
            encoding="utf-8"
        )

        # Same chunking logic used previously
        chunk_size = 800
        overlap = 100

        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start = end - overlap

        print(
            f"Found {len(chunks)} chunks"
        )

        # Generate embeddings
        vectors = model.encode(
            chunks,
            show_progress_bar=True
        )

        output = []

        for i, (chunk, vector) in enumerate(
            zip(chunks, vectors)
        ):

            output.append({
                "id": i,
                "text": chunk,
                "embedding": vector.tolist(),
                "source": file.name
            })

        output_file = (
            OUTPUT_DIR /
            f"{file.stem}.json"
        )

        output_file.write_text(
            json.dumps(
                output,
                indent=2
            ),
            encoding="utf-8"
        )

        print(
            f"Saved embeddings: {output_file}"
        )


if __name__ == "__main__":
    create_embeddings()