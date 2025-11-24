# app.py
import streamlit as st
import json

from agents.planner_agent import create_study_plan
from agents.teacher_agent import generate_notes, make_flashcards
from agents.evaluator_agent import create_quiz, grade_answers
from tools.memory import get_user_profile, update_user_profile


# ---------- Utility ----------

def init_session():
    if "user_id" not in st.session_state:
        st.session_state.user_id = "demo_user"
    if "profile" not in st.session_state:
        st.session_state.profile = get_user_profile(st.session_state.user_id)


def refresh_profile():
    st.session_state.profile = get_user_profile(st.session_state.user_id)


# ---------- Pages ----------

def page_set_goal():
    st.title("🧠 Set Study Goal (Planner Agent)")
    st.write("Define what you want to study, and the Planner Agent will design a plan.")

    goal = st.text_area(
        "Your study goal:",
        placeholder="Example: Study basics of Logistic Regression for my exam today."
    )

    days = st.number_input(
        "Number of days:",
        min_value=1,
        max_value=7,
        value=1,
        step=1
    )

    if st.button("Generate Study Plan", type="primary"):
        if not goal.strip():
            st.warning("Please enter a goal.")
            return

        weak_topics = st.session_state.profile.get("weak_topics", [])

        with st.spinner("Planner Agent is creating your study plan..."):
            plan = create_study_plan(goal, days=days, weak_topics=weak_topics)

        st.subheader("📌 Study Plan (parsed if available)")
        st.json(plan)

        profile = st.session_state.profile
        profile["goals"].append(goal)
        update_user_profile(st.session_state.user_id, profile)
        refresh_profile()
        st.success("Study plan generated and goal saved to memory.")


def page_study_notes():
    st.title("📚 Study Notes & Flashcards (Teacher Agent)")

    topic = st.text_input(
        "Topic you want to study:",
        placeholder="Example: Logistic Regression basics"
    )

    level = st.selectbox(
        "Difficulty level:",
        ["beginner", "intermediate", "advanced"]
    )

    if st.button("Generate Notes & Flashcards", type="primary"):
        if not topic.strip():
            st.warning("Please enter a topic.")
            return

        with st.spinner("Teacher Agent is generating notes..."):
            notes = generate_notes(topic, level=level)
        with st.spinner("Teacher Agent is generating flashcards..."):
            flashcards = make_flashcards(topic, num_cards=5)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📝 Notes")
            st.write(notes)

        with col2:
            st.subheader("🔖 Flashcards")
            if isinstance(flashcards, list):
                st.json(flashcards)
            else:
                st.code(flashcards, language="json")


def page_take_quiz():
    st.title("🧪 Take Quiz (Evaluator Agent)")

    topic = st.text_input(
        "Topic for quiz:",
        placeholder="Example: Logistic Regression basics"
    )

    st.write("We will ask 3 generic questions based on your understanding of this topic.")

    if st.button("Generate Sample Questions (optional)"):
        if not topic.strip():
            st.warning("Enter a topic first.")
        else:
            with st.spinner("Evaluator Agent is creating sample questions..."):
                quiz = create_quiz(topic, num_questions=3)
            st.subheader("Sample Quiz (raw):")
            if isinstance(quiz, list):
                st.json(quiz)
            else:
                st.code(quiz, language="json")

    st.markdown("---")
    st.subheader("✍️ Your Answers")

    q1 = st.text_input("Q1: Explain one key concept of this topic.")
    q2 = st.text_input("Q2: Where is this topic/algorithm commonly used?")
    q3 = st.text_input("Q3: Mention one important detail or formula about this topic.")

    if st.button("Submit & Get Feedback", type="primary"):
        if not topic.strip():
            st.warning("Please enter a topic.")
            return

        answers = [q1, q2, q3]
        if not any(a.strip() for a in answers):
            st.warning("Please fill at least one answer.")
            return

        questions = [
            "Explain one key concept of this topic.",
            "Where is this topic/algorithm commonly used?",
            "Mention one important detail or formula about this topic.",
        ]

        with st.spinner("Evaluator Agent is grading your answers..."):
            result = grade_answers(topic, questions, answers)

        st.subheader("📊 Evaluation Result")
        st.json(result)

        if isinstance(result, dict) and "weak_topics" in result:
            profile = st.session_state.profile
            profile["weak_topics"] = list(
                set(profile.get("weak_topics", []) + result.get("weak_topics", []))
            )
            profile["history"].append({
                "topic": topic,
                "overall_score": result.get("overall_score")
            })
            update_user_profile(st.session_state.user_id, profile)
            refresh_profile()
            st.success("Your performance has been saved to memory.")
        else:
            st.info("Result could not be parsed into full structure; see JSON above.")


def page_view_progress():
    st.title("📈 View Progress & Memory")

    st.write("This is what EduMentor currently knows about you (Memory module).")
    st.json(st.session_state.profile)

    goals = st.session_state.profile.get("goals", [])
    history = st.session_state.profile.get("history", [])
    weak_topics = st.session_state.profile.get("weak_topics", [])

    st.markdown("### 🔍 Quick summary")
    st.write(f"- **Total goals set:** {len(goals)}")
    st.write(f"- **Study sessions recorded:** {len(history)}")
    st.write(f"- **Weak topics tracked:** {len(weak_topics)}")

    if weak_topics:
        st.write("Weak topics:")
        st.write(", ".join(sorted(set(weak_topics))))


# ---------- Main ----------

def main():
    st.set_page_config(
        page_title="EduMentor - AI Study Coach",
        page_icon="🎓",
        layout="wide",
    )

    init_session()

    st.sidebar.title("🎓 EduMentor")
    st.sidebar.write("Multi-Agent AI Study Coach")

    st.sidebar.text_input(
        "User ID",
        value=st.session_state.user_id,
        key="user_id",
        help="Change this to simulate different users."
    )

    if st.sidebar.button("Load / Create Profile"):
        refresh_profile()
        st.sidebar.success("Profile loaded/created.")

    page = st.sidebar.radio(
        "Navigate",
        ["Set Study Goal", "Study Notes", "Take Quiz", "View Progress"],
        index=0
    )

    if page == "Set Study Goal":
        page_set_goal()
    elif page == "Study Notes":
        page_study_notes()
    elif page == "Take Quiz":
        page_take_quiz()
    else:
        page_view_progress()


if __name__ == "__main__":
    main()
