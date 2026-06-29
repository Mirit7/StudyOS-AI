class AnalyticsTool:

    def evaluate_quiz(self, quiz, student_answers):

        total_questions = len(quiz)

        score = 0

        correct_questions = []

        wrong_questions = []

        weak_topics = set()

        strong_topics = set()

        for i, question in enumerate(quiz):

            correct_option = question["correct_answer"]

            user_answer = student_answers.get(i)

            topic = question.get("topic", "General")
            
            if user_answer == correct_option:
                score += 1

                correct_questions.append(question)

                strong_topics.add(topic)

            else:

                wrong_questions.append(question)

                weak_topics.add(topic)

        accuracy = 0

        if total_questions > 0:

            accuracy = round(
                (score / total_questions) * 100,
                2
            )

        return {

            "score": score,

            "total": total_questions,

            "accuracy": accuracy,

            "correct_questions": correct_questions,

            "wrong_questions": wrong_questions,

            "weak_topics": list(weak_topics),

            "strong_topics": list(strong_topics)

        }