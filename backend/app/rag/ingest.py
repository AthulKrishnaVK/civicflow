from pathlib import Path

from docling.document_converter import DocumentConverter


DOCUMENT_DIR = Path("data/documents")
OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def process_documents():

    converter = DocumentConverter()

    for file in DOCUMENT_DIR.rglob("*"):

        if not file.is_file():
            continue

        print(f"Processing: {file}")

        # PDF files
        if file.suffix.lower() == ".pdf":

            result = converter.convert(
                str(file)
            )

            markdown = (
                result.document.export_to_markdown()
            )

        # Markdown files
        elif file.suffix.lower() == ".md":

            markdown = file.read_text(
                encoding="utf-8"
            )

        # Ignore other file types
        else:
            continue

        # Preserve the source folder
        relative_path = file.relative_to(
            DOCUMENT_DIR
        )

        output_name = (
            str(relative_path)
            .replace("\\", "_")
            .replace("/", "_")
        )

        # Remove extension
        output_name = output_name.rsplit(
            ".",
            1
        )[0]

        output_file = (
            OUTPUT_DIR /
            f"{output_name}.md"
        )

        output_file.write_text(
            markdown,
            encoding="utf-8"
        )

        print(
            f"Saved: {output_file}"
        )


if __name__ == "__main__":
    process_documents()