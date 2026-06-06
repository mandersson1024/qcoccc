import questionary
from ..engine.question import Question

_ERAS = ["1920s", "Modern", "Other"]


class EraQuestion(Question):
    allow_any = False

    @property
    def key(self) -> str:
        return "era"

    def ask(self, context: dict) -> str:
        return questionary.select(
            "Era",
            choices=_ERAS,
        ).ask()
