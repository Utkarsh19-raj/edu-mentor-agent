# EduMentor: Autonomous Study Coach using Google AI Agents

## Overview

EduMentor is a simple multi-agent AI study coach built with:

- Google AI Agent SDK
- Gemini (`google-generativeai`)
- Python

It includes:

- **Planner Agent** – breaks a goal into a study plan.
- **Teacher Agent** – generates explanations and flashcards.
- **Evaluator Agent** – creates quizzes and grades answers.
- **Memory** – stores user history and weak topics in a JSON file.

## How to Run

```bash
git clone <your-repo-url>
cd edu-mentor-agent
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create .env
echo "GEMINI_API_KEY=your_key_here" > .env

python main.py
