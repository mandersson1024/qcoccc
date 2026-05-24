import random
import questionary
from engine.question import Question

_ERAS = ["1920s", "Modern", "Other"]


class EraQuestion(Question):
    allow_any = True

    @property
    def key(self) -> str:
        return "era"

    def ask(self, context: dict) -> str:
        choice = questionary.select(
            "Era",
            choices=["ANY"] + _ERAS,
        ).ask()
        return random.choice(_ERAS) if choice == "ANY" else choice
