# agents/planner_agent.py
from typing import Dict, Any, List, Optional
import json

from config import get_model

model = get_model()


def create_study_plan(goal: str, days: int = 1, weak_topics: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Uses the LLM to create a JSON study plan.

    Returns a dict:
    {
      "goal": ...,
      "days": [...],
      "raw_plan": "original_text_from_model"
    }
    """
    weak_topics = weak_topics or []
    prompt = f"""
You are an expert study planner.

User goal:
"{goal}"

Weak topics that need extra attention:
{weak_topics}

Create a study plan for the next {days} day(s).

Return ONLY valid JSON in this format:
{{
  "goal": "{goal}",
  "days": [
    {{
      "day": 1,
      "tasks": [
        {{"topic": "Topic name", "duration_min": 45}},
        {{"topic": "Another topic", "duration_min": 30}}
      ]
    }}
  ]
}}
"""
    res = model.generate_content(prompt)
    text = res.text.strip()

    plan: Dict[str, Any] = {"raw_plan": text}

    try:
        parsed = json.loads(text)
        # Ensure minimal structure
        plan.update(parsed)
    except json.JSONDecodeError:
        # Keep only raw_plan if parsing fails
        plan.setdefault("goal", goal)
        plan.setdefault("days", [])

    return plan
