import questionary
from engine.question import Question


class EraQuestion(Question):
    @property
    def key(self) -> str:
        return "era"

    def ask(self, context: dict) -> str:
        return questionary.select(
            "Era",
            choices=["1920s", "Modern", "Other"],
        ).ask()
