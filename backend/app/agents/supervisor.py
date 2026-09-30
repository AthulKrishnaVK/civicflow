import os
import json

from dotenv import load_dotenv
from groq import Groq

from app.models.schemas import UserIntent


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_goal(user_goal: str) -> UserIntent:

    prompt = f"""
You are the Supervisor Agent of CivicFlow.

CivicFlow helps users understand government procedures
using official sources.

Analyze the user's goal and identify:

1. What the user wants to accomplish
2. Their location
3. The relevant government/business domain
4. The type of government process involved
5. Whether official-source research is required

Return ONLY valid JSON with exactly these fields:

{{
    "goal": "string",
    "location": "string",
    "domain": "string",
    "process_type": "string",
    "requires_research": true
}}

User goal:

{user_goal}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = json.loads(
        response.choices[0].message.content
    )

    return UserIntent.model_validate(result)