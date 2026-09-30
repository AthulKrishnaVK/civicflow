from app.graph.workflow import civicflow_graph


initial_state = {
    "user_input": "I want to start a small food business in Kerala",
    "intent": {},
    "sources": [],
    "eligibility": {},
    "research": [],
    "documents": {},
    "regulations": {},
    "procedure": {},
    "verification": {}
}


print("\n========================================")
print("STARTING CIVICFLOW WORKFLOW")
print("========================================\n")


result = civicflow_graph.invoke(
    initial_state
)


print("\n========================================")
print("CIVICFLOW WORKFLOW COMPLETED")
print("========================================")


print("\n===== INTENT =====")
print(result.get("intent"))


print("\n===== SOURCES =====")
print(
    f"Sources discovered: "
    f"{len(result.get('sources', []))}"
)

for source in result.get("sources", []):
    print(
        source.get("title"),
        "->",
        source.get("url")
    )


print("\n===== RESEARCH =====")
print(
    f"Research items: "
    f"{len(result.get('research', []))}"
)

for item in result.get("research", [])[:10]:
    print(
        "\nSource:",
        item.get("official_url")
    )

    print(
        "Score:",
        item.get(
            "relevance_score",
            item.get("score")
        )
    )

    print(
        "Text:",
        item.get("text", "")[:250]
    )


print("\n===== ELIGIBILITY =====")
print(result.get("eligibility"))


print("\n===== DOCUMENTS =====")
print(result.get("documents"))


print("\n===== REGULATIONS =====")
print(result.get("regulations"))


print("\n===== PROCEDURE =====")
print(result.get("procedure"))


print("\n===== VERIFICATION =====")
print(result.get("verification"))


print("\n========================================")
print("END")
print("========================================")