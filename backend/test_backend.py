"""Quick local smoke test.
Run from backend folder after installing requirements:
python test_backend.py
"""
from agents.router_agent import route_intent
from agents.recommendation_agent import recommend_program
from rag.retriever import retrieve_context

questions = [
    "My child is 6 years old. Which program is suitable?",
    "My child is in class 6. Is it too late to join abacus?",
    "How does MathPath help with school maths?",
    "Where is MathPath located?",
]

for question in questions:
    intent = route_intent(question)
    program = recommend_program(question)
    results = retrieve_context(question, top_k=2)
    print("\nQ:", question)
    print("Intent:", intent)
    print("Program:", program)
    print("Top source:", results[0].source if results else "None")
