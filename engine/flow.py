import sys
from engine.question import Question


class QuestionFlow:
    def __init__(self, questions: list[Question]):
        self._questions = questions

    def run(self) -> dict:
        context = {}
        for question in self._questions:
            answer = question.ask(context)
            if answer is None:
                print("\nAborted.")
                sys.exit(0)
            context[question.key] = answer
        return context
