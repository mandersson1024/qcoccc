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
    @property
    def key(self) -> str:
        return "age_bracket"

    def ask(self, context: dict) -> tuple:
        label = questionary.select(
            "Age bracket",
            choices=[b[0] for b in BRACKETS],
        ).ask()
        return next(b for b in BRACKETS if b[0] == label)
