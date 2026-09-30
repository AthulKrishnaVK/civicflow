from app.agents.relevance import filter_relevant_web_research


web_results = [
    {
        "text": """
        Food business operators must obtain
        appropriate food registration or licence
        through the Food Safety Compliance System.
        """,
        "source": "https://foscos.fssai.gov.in/",
        "chunk_id": 0,
        "organization": "FSSAI",
        "document_title": "FoSCoS",
        "source_type": "government_service",
        "official_url": "https://foscos.fssai.gov.in/"
    },
    {
        "text": """
        Kerala transport department provides
        services related to driving licences,
        vehicle registration and road transport.
        """,
        "source": "https://mvd.kerala.gov.in/",
        "chunk_id": 0,
        "organization": "Kerala MVD",
        "document_title": "Motor Vehicles Department",
        "source_type": "government_service",
        "official_url": "https://mvd.kerala.gov.in/"
    },
    {
        "text": """
        Kerala local governments provide trade
        licences for various businesses and
        commercial activities.
        """,
        "source": "https://lsgd.kerala.gov.in/",
        "chunk_id": 0,
        "organization": "Kerala LSGD",
        "document_title": "Trade License",
        "source_type": "government_service",
        "official_url": "https://lsgd.kerala.gov.in/"
    }
]


intent = {
    "location": "Kerala",
    "domain": "Food and Beverage",
    "process_type": "Food business registration",
}


results = filter_relevant_web_research(
    web_results,
    "I want to start a small food business in Kerala",
    intent,
    top_k=5,
    min_score=0.30
)


print("\n==============================")
print("RELEVANCE FILTER RESULTS")
print("==============================")

for result in results:

    print(
        "\nScore:",
        result["relevance_score"]
    )

    print(
        "Source:",
        result["official_url"]
    )

    print(
        "Text:",
        result["text"][:300]
    )