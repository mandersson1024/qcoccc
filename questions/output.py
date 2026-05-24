import questionary
from engine.question import Question


class OutputQuestion(Question):
    @property
    def key(self) -> str:
        return "output"

    def ask(self, context: dict) -> str:
        return questionary.select(
            "Output",
            choices=["To Terminal", "To File", "Both"],
        ).ask()
