import random
import questionary
from engine.question import Question

_MAX_AGE_OPEN_BRACKET = 99


class AgeQuestion(Question):
    allow_any = True

    @property
    def key(self) -> str:
        return "age"

    def ask(self, context: dict) -> int:
        label, min_age, max_age = context["age_bracket"]
        effective_max = max_age if max_age is not None else _MAX_AGE_OPEN_BRACKET

        def validate(value: str) -> bool | str:
            if value == "":
                return True
            if not value.isdigit():
                return "Please enter a number."
            age = int(value)
            if age < min_age:
                return f"Age must be at least {min_age} for the {label} bracket."
            if age > effective_max:
                return f"Age must be at most {effective_max} for the {label} bracket."
            return True

        answer = questionary.text(
            "Age",
            validate=validate,
            instruction="(or leave empty for random)",
        ).ask()

        if answer == "":
            result = random.randint(min_age, effective_max)
            print(f"  → {result}")
            return result
        return int(answer)
