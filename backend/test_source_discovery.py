from app.agents.source_discovery import analyze_sources


result = analyze_sources(

    "I want to get a driving licence in Kerala",

    {
        "goal": "Get a driving licence",
        "location": "Kerala",
        "domain": "Driving and Transport",
        "process_type": "Driving licence application",
        "requires_research": True
    }

)


print("\n==============================")
print("SOURCE DISCOVERY RESULT")
print("==============================")

print(
    result.model_dump_json(
        indent=2
    )
)