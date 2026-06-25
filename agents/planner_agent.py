def create_study_plan(exam, days_left, study_hours):
    
    plans = {
        "JEE": [
            "Physics",
            "Chemistry",
            "Mathematics"
        ],
        "NEET": [
            "Physics",
            "Chemistry",
            "Biology"
        ],
        "UPSC": [
            "History",
            "Polity",
            "Economics"
        ]
    }

    subjects = plans.get(
        exam,
        ["General Studies"]
    )

    study_plan = []

    for i, subject in enumerate(subjects):
        study_plan.append(
            f"Week {i+1}: {subject}"
        )

    return study_plan