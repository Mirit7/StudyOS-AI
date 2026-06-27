import streamlit as st
from agents.coordinator_agent import CoordinatorAgent
from agents.planner_agent import PlannerAgent
coordinator = CoordinatorAgent()
st.set_page_config(
    page_title="StudyOS AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 StudyOS AI")

st.subheader(
    "Multi-Agent Learning Coach for Competitive Exams"
)

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

study_hours = st.number_input(
    "Daily Study Hours",
    min_value=1,
    max_value=12,
    value=4
)

# if st.button("Create Study Plan"):

if st.button("Create Study Plan"):

    data = {
        "exam": exam,
        "days_left": days_left,
        "study_hours": study_hours
    }

    plan = coordinator.execute(
        "study_plan",
        data
    )

    st.markdown(plan)
    st.success("Study Plan Generated")

    for item in plan:
        st.write(item)