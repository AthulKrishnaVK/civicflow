import os
import json
import re
from urllib.parse import urlparse

from dotenv import load_dotenv
from groq import Groq
from ddgs import DDGS

from app.models.schemas import SourceDiscoveryResult


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# Domains that are generally appropriate for
# Indian government information.
TRUSTED_DOMAIN_PATTERNS = [

    ".gov.in",
    ".nic.in",
    ".gov",
    ".kerala.gov.in",

    # Known government service domains.
    "india.gov.in",
    "services.india.gov.in",
    "fssai.gov.in",
    "foscos.fssai.gov.in",
    "passportindia.gov.in",
    "parivahan.gov.in",
]


def is_official_government_url(url: str):

    try:

        hostname = (
            urlparse(url)
            .hostname
            or ""
        ).lower()

    except Exception:

        return False


    hostname = hostname.split(":")[0]


    for pattern in TRUSTED_DOMAIN_PATTERNS:

        if (
            hostname.endswith(pattern)
            or hostname == pattern
            or pattern in hostname
        ):

            return True


    return False


def extract_json(content: str):

    if not content:
        raise ValueError(
            "Source Discovery Agent returned an empty response."
        )

    content = content.strip()


    content = re.sub(
        r"^```json\s*",
        "",
        content,
        flags=re.IGNORECASE
    )


    content = re.sub(
        r"\s*```$",
        "",
        content
    )


    start = content.find("{")
    end = content.rfind("}")


    if start == -1 or end == -1:

        raise ValueError(
            "Source Discovery Agent did not return JSON."
        )


    return json.loads(
        content[start:end + 1]
    )


def generate_search_queries(
    user_input,
    intent
):

    prompt = f"""
You are the Source Discovery Agent for CivicFlow.

Your job is to determine what official government
information should be searched for in order to answer
the user's request.

USER REQUEST:

{user_input}


USER INTENT:

{json.dumps(
    intent,
    ensure_ascii=False,
    indent=2
)}


Generate up to 5 focused search queries.

The queries should target:

- official government services
- government departments
- government regulations
- official application portals
- official eligibility requirements
- official documents and procedures

Prefer queries that include the user's location
when location is known.

Do NOT include:
- blogs
- Reddit
- Quora
- news websites
- private consultants
- commercial websites
- generic SEO websites

Return ONLY:

{{
    "search_queries": [
        "query 1",
        "query 2"
    ]
}}
"""


    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[

                {
                    "role": "system",
                    "content": (
                        "Generate search queries for "
                        "finding official government "
                        "sources. Return only JSON."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0,

            reasoning_effort="low",

            max_completion_tokens=700
        )


        content = (
            response
            .choices[0]
            .message
            .content
        )


        result = extract_json(
            content
        )


        queries = result.get(
            "search_queries",
            []
        )


        return [
            str(query).strip()
            for query in queries[:5]
            if str(query).strip()
        ]


    except Exception as e:

        print(
            "\n===== QUERY GENERATION ERROR ====="
        )

        print(str(e))

        print(
            "==================================\n"
        )

        return [
            f"{user_input} official government",
        ]


def search_official_sources(
    queries,
    max_results=10
):

    discovered = {}

    try:

        with DDGS() as ddgs:

            for query in queries:

                print(
                    f"\nSearching: {query}"
                )


                try:

                    results = ddgs.text(
                        query,
                        max_results=max_results
                    )

                except Exception as e:

                    print(
                        "Search error:",
                        str(e)
                    )

                    continue


                for result in results:

                    url = result.get(
                        "href",
                        ""
                    )

                    title = result.get(
                        "title",
                        ""
                    )

                    body = result.get(
                        "body",
                        ""
                    )


                    if not url:
                        continue


                    if not is_official_government_url(
                        url
                    ):
                        continue


                    if url not in discovered:

                        discovered[url] = {

                            "title": (
                                title
                                or "Government Source"
                            ),

                            "url": url,

                            "snippet": body
                        }


    except Exception as e:

        print(
            "\n===== SEARCH ENGINE ERROR ====="
        )

        print(str(e))

        print(
            "================================\n"
        )


    return list(
        discovered.values()
    )


def analyze_sources(
    user_input,
    intent
):

    queries = generate_search_queries(
        user_input,
        intent
    )


    print(
        "\n===== SOURCE DISCOVERY QUERIES ====="
    )

    for query in queries:

        print(
            query
        )

    print(
        "=====================================\n"
    )


    search_results = search_official_sources(
        queries
    )


    print(
        "\n===== OFFICIAL SOURCES FOUND ====="
    )

    for item in search_results:

        print(
            item["title"]
        )

        print(
            item["url"]
        )

        print()


    print(
        "===================================\n"
    )


    source_candidates = []


    for item in search_results[:15]:

        source_candidates.append({

            "title": item["title"],

            "url": item["url"],

            "snippet": item["snippet"]
        })


    prompt = f"""
You are the Source Selection Agent in CivicFlow.

Select the government sources that are genuinely
relevant to answering the user's request.

USER REQUEST:

{user_input}


USER INTENT:

{json.dumps(
    intent,
    ensure_ascii=False,
    indent=2
)}


OFFICIAL SOURCE CANDIDATES:

{json.dumps(
    source_candidates,
    ensure_ascii=False,
    indent=2
)}


RULES:

1. Use ONLY the supplied source candidates.

2. Select only sources that are relevant to
   the user's request.

3. Every selected source must be an official
   government source.

4. Do not invent URLs.

5. Do not invent organizations.

6. Do not select commercial websites.

7. Prefer primary government departments,
   government service portals and regulators.

8. Maximum 8 sources.

9. Return ONLY valid JSON.

10. Do not use markdown.


Return exactly:

{{
    "sources": [
        {{
            "title": "source title",
            "url": "official URL",
            "organization": "government organization",
            "reason": "why this source is relevant",
            "source_type": "government_service"
        }}
    ],
    "uncertainties": []
}}
"""


    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[

                {
                    "role": "system",
                    "content": (
                        "Select only relevant official "
                        "government sources. "
                        "Never invent URLs. "
                        "Return only valid JSON."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0,

            reasoning_effort="low",

            max_completion_tokens=1200
        )


        content = (
            response
            .choices[0]
            .message
            .content
        )


        result = extract_json(
            content
        )


    except Exception as e:

        print(
            "\n===== SOURCE SELECTION ERROR ====="
        )

        print(str(e))

        print(
            "===================================\n"
        )

        return SourceDiscoveryResult(

            search_queries=queries,

            sources=[],

            uncertainties=[
                "Official source discovery failed."
            ]
        )


    validated_sources = []


    candidate_map = {

        item["url"]: item

        for item in source_candidates
    }


    for source in result.get(
        "sources",
        []
    )[:8]:

        if not isinstance(
            source,
            dict
        ):
            continue


        url = str(
            source.get(
                "url",
                ""
            )
        ).strip()


        if not url:
            continue


        if url not in candidate_map:
            continue


        if not is_official_government_url(
            url
        ):
            continue


        candidate = candidate_map[url]


        validated_sources.append({

            "title": candidate.get(
                "title",
                "Government Source"
            ),

            "url": url,

            "organization": str(
                source.get(
                    "organization",
                    ""
                )
            ).strip(),

            "reason": str(
                source.get(
                    "reason",
                    ""
                )
            ).strip(),

            "source_type": str(
                source.get(
                    "source_type",
                    "government_source"
                )
            ).strip()
        })


    uncertainties = [

        str(x)

        for x in result.get(
            "uncertainties",
            []
        )[:5]

    ]


    if not validated_sources:

        uncertainties.append(
            "No relevant official government sources were discovered."
        )


    return SourceDiscoveryResult(

        search_queries=queries,

        sources=validated_sources,

        uncertainties=uncertainties
    )