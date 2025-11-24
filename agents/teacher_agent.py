# agents/teacher_agent.py
from typing import List, Union, Dict, Any
import json

from config import get_model

model = get_model()


def generate_notes(topic: str, level: str = "beginner") -> str:
    """
    Generate structured notes for a topic as markdown-like text.
    """
    prompt = f"""
You are a helpful teacher.

Explain the topic "{topic}" for a {level} level learner.

Structure your response as:

# Topic title
## Short Introduction
- Bullet point 1
- Bullet point 2
- ...

## Simple Example
- Give one simple, intuitive example.
"""
    res = model.generate_content(prompt)
    return res.text.strip()


def make_flashcards(topic: str, num_cards: int = 5) -> Union[List[Dict[str, str]], str]:
    """
    Generate flashcards as a list of {{"question": "...", "answer": "..."}} dicts.
    Falls back to raw text string if JSON parsing fails.
    """
    prompt = f"""
Create {num_cards} flashcards for the topic "{topic}".

Each flashcard should have a simple question and a short answer.

Return ONLY valid JSON in this format:
[
  {{"question": "Q1", "answer": "A1"}},
  {{"question": "Q2", "answer": "A2"}}
]
"""
    res = model.generate_content(prompt)
    text = res.text.strip()

    try:
        cards = json.loads(text)
        if isinstance(cards, list):
            return cards
        return text
    except json.JSONDecodeError:
        return text
