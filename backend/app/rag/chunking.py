from pathlib import Path


PROCESSED_DIR = Path("data/processed")
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100


def chunk_text(text: str):
    chunks = []

    start = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - CHUNK_OVERLAP

    return chunks


def process_chunks():

    for file in PROCESSED_DIR.glob("*.md"):

        print(f"Chunking: {file.name}")

        text = file.read_text(
            encoding="utf-8"
        )

        chunks = chunk_text(text)

        print(
            f"Created {len(chunks)} chunks"
        )

        for i, chunk in enumerate(chunks[:3]):

            print(f"\n--- Chunk {i + 1} ---")
            print(chunk[:300])


if __name__ == "__main__":
    process_chunks()