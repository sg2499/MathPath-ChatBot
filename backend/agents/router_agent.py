import os
from openai import OpenAI
from config import get_settings

def route_intent(message: str) -> str:
    """Use an LLM to accurately determine the intent of the user's message."""
    settings = get_settings()
    if not settings.openai_api_key or settings.openai_api_key == "your_openai_api_key_here":
        return "general_query"
        
    client = OpenAI(api_key=settings.openai_api_key)
    
    prompt = f"""You are a router agent for the MathPath Abacus Chatbot.
Based on the user's message, classify the intent into ONE of the following categories. 
Reply ONLY with the exact string of the category name, nothing else.

Categories:
- demo_booking (user wants to book a free demo, schedule a trial, or requests a callback)
- fees (user asks about pricing, cost, or fees)
- contact_location (user asks where it is, phone numbers, or addresses)
- program_recommendation (user provides child age/class and wants to know the right program)
- bridge_course (user asks about late joining or bridge course for older kids)
- parent_concern (user says child is weak in math, scared of math, or needs help with basics)
- general_query (anything else about the program structure, duration, apps, or competitions)

User message: "{message}"
Intent:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=10
        )
        intent = response.choices[0].message.content.strip().lower()
        valid_intents = ["demo_booking", "fees", "contact_location", "program_recommendation", "bridge_course", "parent_concern", "general_query"]
        if intent in valid_intents:
            return intent
        return "general_query"
    except Exception:
        return "general_query"
