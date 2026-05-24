import random
import questionary
from engine.question import Question


BRACKETS = [
    ("15–19", 15, 19),
    ("20s",   20, 29),
    ("30s",   30, 39),
    ("40s",   40, 49),
    ("50s",   50, 59),
    ("60s",   60, 69),
    ("70s",   70, 79),
    ("80s+",  80, None),
]


class AgeBracketQuestion(Question):
    allow_any = True

    @property
    def key(self) -> str:
        return "age_bracket"

    def ask(self, context: dict) -> tuple:
        choice = questionary.select(
            "Age bracket",
            choices=["ANY"] + [b[0] for b in BRACKETS],
        ).ask()
        if choice == "ANY":
            return random.choice(BRACKETS)
        return next(b for b in BRACKETS if b[0] == choice)
