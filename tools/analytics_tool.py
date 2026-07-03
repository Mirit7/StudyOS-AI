class AnalyticsTool:

    def evaluate_quiz(self, quiz, student_answers):

        total_questions = len(quiz)

        score = 0

        correct_questions = []

        wrong_questions = []

        topic_stats = {}

        for i, question in enumerate(quiz):

            correct_option = question["correct_answer"]

            user_answer = student_answers.get(i)

            topic = question.get("topic", "General")

            if topic not in topic_stats:

                topic_stats[topic] = {
                    "correct": 0,
                    "wrong": 0
                }

            if user_answer == correct_option:

                score += 1

                correct_questions.append(question)

                topic_stats[topic]["correct"] += 1

            else:

                wrong_questions.append(question)

                topic_stats[topic]["wrong"] += 1

        strong_topics = []
        weak_topics = []

        for topic, stats in topic_stats.items():

            if stats["correct"] > stats["wrong"]:

                strong_topics.append(topic)

            elif stats["wrong"] > stats["correct"]:

                weak_topics.append(topic)

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

            "strong_topics": strong_topics,

            "weak_topics": weak_topics,

            "topic_stats": topic_stats,

            "correct_questions": correct_questions,

            "wrong_questions": wrong_questions
        }