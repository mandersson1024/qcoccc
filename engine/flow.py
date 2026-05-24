from engine.question import Question


class QuestionFlow:
    def __init__(self, questions: list[Question]):
        self._questions = questions

    def run(self) -> dict:
        context = {}
        for question in self._questions:
            context[question.key] = question.ask(context)
        return context
