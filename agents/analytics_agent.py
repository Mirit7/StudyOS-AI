def evaluate_quiz(
    correct_answers,
    student_answers
):
    score = 0

    for correct, student in zip(
        correct_answers,
        student_answers
    ):
        if correct == student:
            score += 1

    return {
        "score": score,
        "total": len(correct_answers),
        "accuracy": round(
            score / len(correct_answers) * 100,
            2
        )
    }