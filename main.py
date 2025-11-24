# main.py
from agents.planner_agent import create_study_plan
from agents.teacher_agent import generate_notes, make_flashcards
from agents.evaluator_agent import create_quiz, grade_answers
from tools.memory import get_user_profile, update_user_profile

import json


USER_ID = "demo_user"


def print_menu():
    print("\n=== EduMentor — AI Study Coach (CLI) ===")
    print("1️⃣  Set Study Goal (Planner Agent)")
    print("2️⃣  Study Notes & Flashcards (Teacher Agent)")
    print("3️⃣  Take Quiz (Evaluator Agent)")
    print("4️⃣  View Memory / Progress")
    print("0️⃣  Exit")


def cli_main():
    profile = get_user_profile(USER_ID)

    while True:
        print_menu()
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            goal = input("\nEnter your study goal: ").strip()
            if not goal:
                print("⚠️ Please enter a goal.")
                continue

            weak_topics = profile.get("weak_topics", [])
            plan = create_study_plan(goal, days=1, weak_topics=weak_topics)

            print("\n📌 Study Plan (parsed if available):")
            print(json.dumps(plan, indent=2, ensure_ascii=False))

            profile["goals"].append(goal)
            update_user_profile(USER_ID, profile)
            print("\n💾 Goal saved to memory.")

        elif choice == "2":
            topic = input("\nEnter topic to study: ").strip()
            if not topic:
                print("⚠️ Please enter a topic.")
                continue

            level = input("Enter level (beginner/intermediate/advanced): ").strip() or "beginner"

            print("\n⏳ Generating notes...")
            notes = generate_notes(topic, level=level)
            print("\n📝 Notes:")
            print(notes)

            print("\n⏳ Generating flashcards...")
            flashcards = make_flashcards(topic, num_cards=3)

            print("\n🔖 Flashcards:")
            if isinstance(flashcards, list):
                print(json.dumps(flashcards, indent=2, ensure_ascii=False))
            else:
                print(flashcards)

        elif choice == "3":
            topic = input("\nEnter topic for quiz: ").strip()
            if not topic:
                print("⚠️ Please enter a topic.")
                continue

            print("\n⏳ Creating sample quiz questions...")
            quiz = create_quiz(topic, num_questions=3)
            print("\n🧪 Quiz questions (raw):")
            if isinstance(quiz, list):
                print(json.dumps(quiz, indent=2, ensure_ascii=False))
            else:
                print(quiz)

            print("\nNow answer these generic questions based on your understanding:")
            questions = [
                "Explain one key concept of this topic.",
                "Where is this topic/algorithm commonly used?",
                "Mention one important detail or formula related to this topic.",
            ]

            answers = []
            for i, q in enumerate(questions, start=1):
                print(f"\nQ{i}: {q}")
                ans = input("Your answer: ")
                answers.append(ans)

            print("\n⏳ Grading your answers...")
            result = grade_answers(topic, questions, answers)

            print("\n📊 Evaluation Result:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            if isinstance(result, dict) and "weak_topics" in result:
                profile["weak_topics"] = list(
                    set(profile.get("weak_topics", []) + result.get("weak_topics", []))
                )
                profile["history"].append({
                    "topic": topic,
                    "overall_score": result.get("overall_score")
                })
                update_user_profile(USER_ID, profile)
                print("\n💾 Memory updated with weak topics & score.")
            else:
                print("\nℹ️ Could not parse result into structured feedback. See raw response above.")

        elif choice == "4":
            profile = get_user_profile(USER_ID)
            print("\n📚 Current Memory / Profile:")
            print(json.dumps(profile, indent=2, ensure_ascii=False))

        elif choice == "0":
            print("\n👋 Goodbye!")
            break

        else:
            print("❗ Invalid option, please try again.")


if __name__ == "__main__":
    cli_main()
