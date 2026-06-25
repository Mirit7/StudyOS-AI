import streamlit as st
from agents.planner_agent import create_study_plan
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

if st.button("Create Study Plan"):

    plan = create_study_plan(
        exam,
        days_left,
        study_hours
    )

    st.success("Study Plan Generated")

    for item in plan:
        st.write(item)