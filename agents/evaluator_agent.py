# agents/evaluator_agent.py
from typing import List, Dict, Any, Union
import json

from config import get_model

model = get_model()


def create_quiz(topic: str, num_questions: int = 5) -> Union[List[Dict[str, str]], str]:
    """
    Generate a list of quiz questions for the topic.
    Returns list of {"question": "..."} or raw text if parsing fails.
    """
    prompt = f"""
Create {num_questions} short-answer questions for the topic "{topic}".

Return ONLY valid JSON, in this format:
[
  {{"question": "Question 1?"}},
  {{"question": "Question 2?"}}
]
"""
    res = model.generate_content(prompt)
    text = res.text.strip()

    try:
        questions = json.loads(text)
        if isinstance(questions, list):
            return questions
        return text
    except json.JSONDecodeError:
        return text


def grade_answers(topic: str, questions: List[str], answers: List[str]) -> Dict[str, Any]:
    """
    Grade user's answers. Returns a structured dict if possible.

    Expected JSON from model:
    {
      "per_question": [
        {"question": "...", "answer": "...", "score": 0.7, "feedback": "..."}
      ],
      "overall_score": 75,
      "weak_topics": ["..."],
      "summary": "..."
    }
    """
    qa_pairs = [{"question": q, "answer": a} for q, a in zip(questions, answers)]

    prompt = f"""
You are a strict but helpful teacher.

Topic: {topic}

Student answers (JSON):
{json.dumps(qa_pairs, ensure_ascii=False)}

For each QA pair, give:
- score: number between 0 and 1
- feedback: short explanation

Also give:
- overall_score: 0 to 100
- weak_topics: list of 1-3 short strings (e.g. ["Bayes theorem", "notation"])
- summary: short paragraph of overall feedback

Return ONLY valid JSON in this format:
{{
  "per_question": [
    {{"question": "...", "answer": "...", "score": 0.7, "feedback": "..."}}
  ],
  "overall_score": 75,
  "weak_topics": ["..."],
  "summary": "..."
}}
"""
    res = model.generate_content(prompt)
    text = res.text.strip()

    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
        return {"raw_response": text}
    except json.JSONDecodeError:
        return {"raw_response": text}
