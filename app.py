import matplotlib.pyplot as plt
import streamlit as st

from agents.coordinator_agent import CoordinatorAgent
from tools.database_tool import DatabaseTool
if "student_answers" not in st.session_state:
    st.session_state.student_answers = {}
# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="StudyOS AI",
    page_icon="🎓",
    layout="wide"
)
history = DatabaseTool().get_last_reports(limit=100)
# ==========================================
# Coordinator
# ==========================================
coordinator = CoordinatorAgent()

# ==========================================
# Session State
# ==========================================
if "planner_output" not in st.session_state:
    st.session_state.planner_output = None

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if "student_answers" not in st.session_state:
    st.session_state.student_answers = {}

# ==========================================
# Header
# ==========================================
st.title("🎓 StudyOS AI")
st.caption("Your Personal Multi-Agent Learning Coach")

st.divider()
from tools.database_tool import DatabaseTool
db = DatabaseTool()

history = db.get_last_reports(limit=100)

total_quizzes = len(history)

average_accuracy = round(
    sum(row[4] for row in history) / len(history),
    2
) if history else 0

best_accuracy = max(
    [row[4] for row in history]
) if history else 0

col1, col2, col3 = st.columns(3)

col1.metric(
    "📚 Total Quizzes",
    total_quizzes
)

col2.metric(
    "🎯 Average Accuracy",
    f"{average_accuracy}%"
)

col3.metric(
    "🏆 Best Accuracy",
    f"{best_accuracy}%"
)

st.divider()
# ==========================================
# User Inputs
# ==========================================
exam = st.selectbox(
    "Select Exam",
    [
        "JEE",
        "NEET",
        "UPSC",
        "SSC",
        "DDCET",
        "Custom"
    ]
)

days_left = st.number_input(
    "Days Remaining",
    min_value=1,
    value=180
)

study_hours = st.slider(
    "Daily Study Hours",
    min_value=1,
    max_value=12,
    value=4
)

st.divider()

# ==========================================
# Generate Study Plan
# ==========================================
if st.button("🚀 Generate Study Plan", use_container_width=True):

    planner_data = {
        "exam": exam,
        "days_left": days_left,
        "study_hours": study_hours
    }

    st.session_state.planner_output = coordinator.execute(
        "study_plan",
        planner_data
    )
    
    # Reset Quiz
    st.session_state.quiz = None
    st.session_state.quiz_started = False
    st.session_state.student_answers = {}

# ==========================================
# Display Study Plan
# ==========================================
if st.session_state.planner_output is not None:

    st.success("✅ Your personalized study plan is ready!")

    st.subheader("📅 Study Plan")

    study_plan = st.session_state.planner_output.get("study_plan")

    if study_plan is None:

        st.error("Planner did not return a study plan.")
        st.write(st.session_state.planner_output)
        st.stop()

    if isinstance(study_plan, list):

        for item in study_plan:
            st.write(f"• {item}")

    else:

        st.markdown(study_plan)

    st.divider()

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"],
        index=1
    )

    num_questions = st.selectbox(
        "Number of Questions",
        [5, 10, 15, 20, 25, 30],
        index=1
    )

    if st.button("📝 Start Today's Quiz", use_container_width=True):

        st.session_state.quiz = coordinator.execute(
            "generate_quiz",
            {
                "exam": exam,
                "topics": st.session_state.planner_output["today_topics"],
                "difficulty": difficulty,
                "num_questions": num_questions
            }
        )

        st.session_state.student_answers = {}
        st.session_state.quiz_started = True

        st.rerun()

# ==========================================
# Display Quiz
# ==========================================

if st.session_state.quiz_started and st.session_state.quiz:

    st.divider()

    st.header("📝 Today's Quiz")

    # Display every question
    for i, question in enumerate(st.session_state.quiz):

        st.markdown(f"### Question {i+1}")

        st.write(question["question"])

        option_map = {
            "A": question["options"]["A"],
            "B": question["options"]["B"],
            "C": question["options"]["C"],
            "D": question["options"]["D"],
        }

        selected_text = st.radio(
            f"Choose answer for Question {i+1}",
            list(option_map.values()),
            index=None,
            key=f"question_{i}"
        )

        if selected_text is not None:

            for key, value in option_map.items():

                if value == selected_text:

                    st.session_state.student_answers[i] = key
                    break

        st.markdown("---")

    # Submit button AFTER all questions
    if st.button(
        "✅ Submit Quiz",
        type="primary",
        use_container_width=True
    ):

        report = coordinator.execute(
            "evaluate_quiz",
            {
                "quiz": st.session_state.quiz,
                "student_answers": st.session_state.student_answers
            }
        )
        coordinator.execute(

            "save_report",

            {

                "exam": exam,

                "score": report["score"],

                "total": report["total"],

                "accuracy": report["accuracy"],

                "strong_topics": report["strong_topics"],

                "weak_topics": report["weak_topics"]

            }
        )
        mentor_feedback = coordinator.execute(
            "mentor_feedback",
            {}
        )
        # st.session_state.report = report
        # st.session_state.mentor_feedback = mentor_feedback

        # st.rerun()

        st.header("🤖 AI Mentor")

        st.markdown(mentor_feedback)
        
        st.divider()
        st.header("📖 Answer Review")

        for i, question in enumerate(st.session_state.quiz):

            st.subheader(f"Question {i+1}")

            st.write(question["question"])

            user_answer = st.session_state.student_answers.get(i, "Not Answered")

            st.write(f"Your Answer: {user_answer}")

            st.write(f"Correct Answer: {question['correct_answer']}")

            st.info(question["explanation"])

        st.success("🎉 Quiz Submitted Successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Score",
                f"{report['score']} / {report['total']}"
            )

        with col2:
            st.metric(
                "Accuracy",
                f"{report['accuracy']}%"
            )

        st.subheader("❌ Weak Topics")

        if report["weak_topics"]:

            for topic in report["weak_topics"]:
                st.error(topic)

        else:
            st.success("No weak topics detected!")

        st.subheader("✅ Strong Topics")

        if report["strong_topics"]:

            for topic in report["strong_topics"]:
                st.success(topic)

        else:
            st.info("No strong topics yet.")

history = DatabaseTool().get_last_reports(limit=100)

accuracies = [row[4] for row in history[::-1]]

fig, ax = plt.subplots(figsize=(8, 3))

ax.plot(accuracies, marker="o")

ax.set_xlabel("Quiz Attempted")
ax.set_ylabel("Accuracy")

st.pyplot(fig)