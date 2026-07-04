import plotly.graph_objects as go
import streamlit as st
from streamlit.components.v1 import html as components_html

from agents.coordinator_agent import CoordinatorAgent
from tools.database_tool import DatabaseTool

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="StudyOS AI",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# Coordinator
# ==========================================
coordinator = CoordinatorAgent()
db = DatabaseTool()

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

if "splash_seen" not in st.session_state:
    st.session_state.splash_seen = False


# ==========================================
# Premium Styling
# ==========================================
def inject_styles():
    st.markdown(
        """
        <style>
            :root {
                color-scheme: dark;
            }
            html, body, [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #050816 0%, #0b1026 45%, #111936 100%);
                color: #f6f7ff;
            }
            [data-testid="stHeader"] {
                background: rgba(7, 10, 24, 0.55);
                backdrop-filter: blur(16px);
            }
            .block-container {
                padding-top: 1rem;
                padding-bottom: 3rem;
                max-width: 1400px;
            }
            .hero-card, .glass-card {
                background: linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(29, 35, 64, 0.82));
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 24px;
                box-shadow: 0 22px 60px rgba(4, 8, 24, 0.45);
                padding: 1.25rem 1.35rem;
                margin-bottom: 1rem;
                position: relative;
                overflow: hidden;
                animation: fadeUp 700ms ease both;
            }
            .hero-card::before, .glass-card::before {
                content: "";
                position: absolute;
                inset: 0;
                background: radial-gradient(circle at top left, rgba(139, 92, 246, 0.18), transparent 45%);
                pointer-events: none;
            }
            .hero-title {
                font-size: 2.3rem;
                font-weight: 700;
                letter-spacing: -0.03em;
                margin-bottom: 0.2rem;
            }
            .hero-subtitle {
                color: #b6c2ff;
                font-size: 1rem;
                margin-bottom: 0.75rem;
            }
            .badge-pill {
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                padding: 0.3rem 0.7rem;
                border-radius: 999px;
                background: rgba(124, 58, 237, 0.16);
                border: 1px solid rgba(167, 139, 250, 0.24);
                color: #d8c2ff;
                font-size: 0.78rem;
                margin-bottom: 0.75rem;
            }
            .metric-card {
                background: rgba(9, 14, 31, 0.82);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 18px;
                padding: 0.9rem 1rem;
                min-height: 105px;
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
                transition: transform 220ms ease, box-shadow 220ms ease;
            }
            .metric-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 18px 40px rgba(76, 29, 149, 0.18);
            }
            .section-label {
                color: #8ea0ff;
                font-size: 0.8rem;
                letter-spacing: 0.16em;
                text-transform: uppercase;
                margin-bottom: 0.3rem;
            }
            .stButton > button {
                background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
                color: white;
                border: none;
                border-radius: 999px;
                padding: 0.7rem 1rem;
                font-weight: 600;
                box-shadow: 0 16px 32px rgba(79, 70, 229, 0.28);
                transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease;
            }
            .stButton > button:hover {
                transform: translateY(-2px) scale(1.01);
                box-shadow: 0 0 0 1px rgba(255,255,255,0.12), 0 0 28px rgba(139, 92, 246, 0.26);
                filter: brightness(1.06);
            }
            .stTextInput > div > div > input,
            .stSelectbox > div > div > div,
            .stNumberInput input,
            .stSlider > div > div {
                background: rgba(8, 12, 26, 0.9);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 12px;
                color: #f8f9ff;
            }
            .stRadio > div {
                background: rgba(8, 12, 26, 0.6);
                border-radius: 14px;
                padding: 0.4rem 0.6rem;
            }
            .stAlert, .stSuccess, .stError, .stInfo {
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
            }
            [data-testid="stMetricLabel"] {
                color: #9fb0ff;
            }
            [data-testid="stMetricValue"] {
                color: #ffffff;
                font-size: 1.2rem;
            }
            [data-testid="stSidebar"] {
                background: rgba(5, 8, 20, 0.92);
            }
            @keyframes fadeUp {
                from {
                    opacity: 0;
                    transform: translateY(12px) scale(0.985);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_styles()


def show_splash():
    if st.session_state.splash_seen:
        return

    splash_html = """
    <div id="studyos-splash">
        <div class="orb"></div>
        <div class="logo">S</div>
        <div class="title">StudyOS AI</div>
        <div class="subtitle">Your Personal Multi-Agent Learning Coach</div>
        <div class="line"></div>
    </div>
    <script>
        const splash = document.getElementById('studyos-splash');
        setTimeout(() => splash.classList.add('fade-out'), 1600);
        setTimeout(() => {
            splash.style.display = 'none';
        }, 2300);
    </script>
    """

    components_html(
        f"""
        <style>
            body {{ margin: 0; }}
            #studyos-splash {{
                position: fixed;
                inset: 0;
                z-index: 999999;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                background: radial-gradient(circle at top, rgba(124,58,237,0.2), rgba(2,6,23,0.98) 70%);
                color: white;
                font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }}
            #studyos-splash .orb {{
                width: 220px;
                height: 220px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(167,139,250,0.35), rgba(79,70,229,0.06) 55%, transparent 72%);
                filter: blur(14px);
                position: absolute;
                animation: pulse 1.6s ease-in-out infinite alternate;
            }}
            #studyos-splash .logo {{
                width: 84px;
                height: 84px;
                border-radius: 24px;
                display: grid;
                place-items: center;
                font-size: 2rem;
                font-weight: 700;
                background: linear-gradient(135deg, rgba(167,139,250,0.35), rgba(79,70,229,0.6));
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 0 45px rgba(139, 92, 246, 0.24);
                transform: scale(0.92);
                animation: zoomIn 1.2s ease forwards;
                backdrop-filter: blur(10px);
            }}
            #studyos-splash .title {{
                margin-top: 1rem;
                font-size: 2rem;
                font-weight: 700;
                letter-spacing: -0.03em;
                opacity: 0;
                animation: fadeIn 0.8s ease 0.35s forwards;
            }}
            #studyos-splash .subtitle {{
                margin-top: 0.45rem;
                color: #c5cbff;
                font-size: 0.95rem;
                opacity: 0;
                animation: fadeIn 0.8s ease 0.55s forwards;
            }}
            #studyos-splash .line {{
                width: 180px;
                height: 2px;
                border-radius: 999px;
                margin-top: 1rem;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent);
                transform: scaleX(0.2);
                transform-origin: center;
                animation: growLine 1s ease 0.8s forwards;
            }}
            #studyos-splash.fade-out {{
                opacity: 0;
                transition: opacity 0.45s ease;
            }}
            @keyframes pulse {{ from {{ transform: scale(0.9); }} to {{ transform: scale(1.04); }} }}
            @keyframes zoomIn {{ from {{ transform: scale(0.7); opacity: 0; }} to {{ transform: scale(1); opacity: 1; }} }}
            @keyframes fadeIn {{ to {{ opacity: 1; }} }}
            @keyframes growLine {{ to {{ transform: scaleX(1); }} }}
        </style>
        {splash_html}
        """,
        height=1000,
    )

    st.session_state.splash_seen = True


show_splash()


history = db.get_last_reports(limit=100)

total_quizzes = len(history)
average_accuracy = round(sum(row[4] for row in history) / len(history), 2) if history else 0
best_accuracy = max([row[4] for row in history]) if history else 0

# ==========================================
# Header
# ==========================================
st.markdown(
    """
    <div class="hero-card">
        <div class="badge-pill">✦ Premium AI Learning Workspace</div>
        <div class="hero-title">StudyOS AI</div>
        <div class="hero-subtitle">Your Personal Multi-Agent Learning Coach</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='section-label'>Performance snapshot</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("📚 Total Quizzes", total_quizzes)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("🎯 Average Accuracy", f"{average_accuracy}%")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric("🏆 Best Accuracy", f"{best_accuracy}%")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-label' style='margin-top: 1.2rem;'>Launch your next study cycle</div>", unsafe_allow_html=True)

# ==========================================
# User Inputs
# ==========================================
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# Generate Study Plan
# ==========================================
if st.button("🚀 Generate Study Plan", width="stretch"):
    planner_data = {
        "exam": exam,
        "days_left": days_left,
        "study_hours": study_hours
    }

    with st.spinner("Crafting your tailored study plan..."):
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
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.success("Your personalized study plan is ready!")

    st.subheader("📅 Study Plan")

    study_plan = st.session_state.planner_output.get("study_plan")

    if study_plan is None:
        st.error("Planner did not return a study plan.")
        st.write(st.session_state.planner_output)
        st.stop()

    if isinstance(study_plan, list):
        st.markdown("<div style='line-height: 1.7;'>", unsafe_allow_html=True)
        for item in study_plan:
            st.write(f"• {item}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(study_plan)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
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

    if st.button("📝 Start Today's Quiz", width="stretch"):
        with st.spinner("Designing your quiz experience..."):
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
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# Display Quiz
# ==========================================
if st.session_state.quiz_started and st.session_state.quiz:
    st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
    st.header("📝 Today's Quiz")
    st.markdown("</div>", unsafe_allow_html=True)

    for i, question in enumerate(st.session_state.quiz):
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
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

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "Submit Quiz",
        type="primary",
        width="stretch"
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

        with st.spinner("Your mentor is preparing feedback..."):
            mentor_feedback = coordinator.execute(
                "mentor_feedback",
                {}
            )

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.header("🤖 AI Mentor")
        st.markdown(mentor_feedback)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.header("📖 Answer Review")

        for i, question in enumerate(st.session_state.quiz):
            st.subheader(f"Question {i+1}")
            st.write(question["question"])

            user_answer = st.session_state.student_answers.get(i, "Not Answered")
            st.write(f"Your Answer: {user_answer}")
            st.write(f"Correct Answer: {question['correct_answer']}")
            st.info(question["explanation"])

        st.success("Quiz Submitted Successfully!")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Score", f"{report['score']} / {report['total']}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Accuracy", f"{report['accuracy']}%")
            st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("Weak Topics")
        if report["weak_topics"]:
            for topic in report["weak_topics"]:
                st.error(topic)
        else:
            st.success("No weak topics detected!")

        st.subheader("Strong Topics")
        if report["strong_topics"]:
            for topic in report["strong_topics"]:
                st.success(topic)
        else:
            st.info("No strong topics yet.")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-label' style='margin-top: 1.2rem;'>Learning analytics</div>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    history = db.get_last_reports(limit=100)
    accuracies = [row[4] for row in history[::-1]]

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=accuracies, mode="lines+markers", line=dict(color="#8b5cf6", width=3), marker=dict(color="#c084fc", size=8)))
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7ff"),
        xaxis=dict(showgrid=False, zeroline=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", zeroline=False),
    )
    st.plotly_chart(fig, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

st.header("🏗️ Multi-Agent Architecture")

st.markdown("""
This application uses a Coordinator Agent that routes every user request
to specialized AI agents.
            
                👤 User
                │
                ▼
        🎯 Coordinator Agent
                │
    ┌────────────┼─────────────┐
    │            │             │
    ▼            ▼             ▼
    📅 Planner 📝 Quiz 📊 Analytics
    │ 
    ▼ 
    🤖 Gemini API Performance Report
    │
    ▼
    🧠 Mentor Agent
    │
    ▼
    💾 Memory Agent (SQLite)
""")
st.subheader("🤖 AI Agents")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### 📅 Planner Agent

Creates a personalized study roadmap
based on:

- Exam
- Days Remaining
- Daily Study Hours

Uses Gemini AI.
""")

    st.info("""
### 📝 Quiz Agent

Generates adaptive MCQs from today's topics.

Uses Gemini AI.
""")

    st.info("""
### 📊 Analytics Agent

Evaluates quiz performance.

Calculates:

- Score
- Accuracy
- Strong Topics
- Weak Topics
""")

with col2:

    st.info("""
### 💾 Memory Agent

Stores every quiz inside SQLite.

Tracks long-term learning history.
""")

    st.info("""
### 🤖 Mentor Agent

Analyzes previous quiz history.

Provides:

- Performance Review
- Weak Areas
- Strong Areas
- Tomorrow's Plan
- Motivation
""")

    st.info("""
### 🎯 Coordinator Agent

Routes requests to the correct AI agent.

Acts as the brain of the system.
""")
st.divider()

st.subheader("⚙️ Tech Stack")

st.markdown("""
-  Python
-  Streamlit
-  Google Gemini 2.5 Flash
-  SQLite
-  Multi-Agent Architecture
-  Matplotlib
""")