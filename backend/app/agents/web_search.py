

import requests
from bs4 import BeautifulSoup

from app.agents.relevance import filter_relevant_chunks


MIN_TEXT_LENGTH = 300

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


# ============================================================
# URL VALIDATION
# ============================================================

def is_trusted_government_url(url: str):
    """
    Check whether the URL belongs to an official
    government / recognized government service domain.
    """

    if not url:
        return False

    url_lower = url.lower()

    trusted_domains = [
        ".gov.in",
        ".nic.in",
        "kerala.gov.in",
        "fssai.gov.in",
        "foscos.fssai.gov.in",
        "lsgd.kerala.gov.in",
        "kswift.kerala.gov.in"
    ]

    return any(
        domain in url_lower
        for domain in trusted_domains
    )


# ============================================================
# TEXT EXTRACTION
# ============================================================

def extract_text(url: str):
    """
    Fetch a webpage and extract readable text.
    """

    print(f"\nFetching: {url}")

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        print(
            f"Status: {response.status_code}"
        )

        if response.status_code != 200:

            print(
                "Skipped: HTTP request failed."
            )

            return None

        content_type = response.headers.get(
            "content-type",
            ""
        ).lower()

        if (
            "text/html"
            not in content_type
        ):

            print(
                "Skipped: not an HTML page."
            )

            return None

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary elements
        for tag in soup([
            "script",
            "style",
            "noscript",
            "nav",
            "footer",
            "header",
            "form",
            "svg"
        ]):

            tag.decompose()

        text = soup.get_text(
            separator="\n",
            strip=True
        )

        if not text:

            print(
                "Skipped: no readable text."
            )

            return None

        if len(text) < MIN_TEXT_LENGTH:

            print(
                "Skipped: insufficient "
                f"readable content "
                f"({len(text)} characters)."
            )

            return None

        return text

    except requests.exceptions.RequestException as e:

        print(
            f"Request error: {e}"
        )

        return None

    except Exception as e:

        print(
            f"Extraction error: {e}"
        )

        return None


# ============================================================
# CHUNKING
# ============================================================

def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 150
):
    """
    Split webpage text into overlapping chunks.
    """

    if not text:

        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[
            start:end
        ].strip()

        if chunk:

            chunks.append(
                chunk
            )

        start += (
            chunk_size - overlap
        )

    return chunks


# ============================================================
# FETCH SOURCES
# ============================================================

def fetch_sources(
    sources: list,
    user_input: str = ""
):
    """
    Fetch official government sources,
    extract their text, chunk them and apply
    semantic relevance filtering.

    This function is intentionally named
    fetch_sources because research.py imports it.
    """

    print("\n==============================")
    print("WEB SOURCE RESEARCH")
    print("==============================")

    raw_chunks = []

    # --------------------------------------------------------
    # Fetch every discovered source
    # --------------------------------------------------------

    for source in sources:

        # Source may be a dictionary
        if isinstance(
            source,
            dict
        ):

            url = source.get(
                "url",
                ""
            )

            title = source.get(
                "title",
                ""
            )

            organization = source.get(
                "organization",
                ""
            )

        # Source may be a Pydantic object
        else:

            url = getattr(
                source,
                "url",
                ""
            )

            title = getattr(
                source,
                "title",
                ""
            )

            organization = getattr(
                source,
                "organization",
                ""
            )

        if not url:

            continue

        # ----------------------------------------------------
        # Government domain validation
        # ----------------------------------------------------

        if not is_trusted_government_url(
            url
        ):

            print(
                f"\nSkipped non-government URL: "
                f"{url}"
            )

            continue

        # ----------------------------------------------------
        # Fetch webpage
        # ----------------------------------------------------

        text = extract_text(
            url
        )

        if not text:

            continue

        # ----------------------------------------------------
        # Chunk webpage
        # ----------------------------------------------------

        chunks = chunk_text(
            text
        )

        print(
            f"Extracted {len(text)} "
            f"characters → "
            f"{len(chunks)} chunks"
        )

        for index, chunk in enumerate(
            chunks
        ):

            raw_chunks.append({

                "source": url,

                "chunk_id": index,

                "text": chunk,

                "title": title,

                "organization": organization
            })

    print(
        f"\nRaw web chunks: "
        f"{len(raw_chunks)}"
    )

    if not raw_chunks:

        return []

    # --------------------------------------------------------
    # Semantic relevance filtering
    # --------------------------------------------------------

    relevant_chunks = (
        filter_relevant_chunks(
            user_input,
            raw_chunks,
            top_k=20,
            min_score=0.30
        )
    )

    print(
        f"Relevant web chunks: "
        f"{len(relevant_chunks)}"
    )

    return relevant_chunks