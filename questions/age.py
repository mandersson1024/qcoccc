import questionary
from engine.question import Question


class AgeQuestion(Question):
    @property
    def key(self) -> str:
        return "age"

    def ask(self, context: dict) -> int:
        label, min_age, max_age = context["age_bracket"]

        def validate(value: str) -> bool | str:
            if not value.isdigit():
                return "Please enter a number."
            age = int(value)
            if age < min_age:
                return f"Age must be at least {min_age} for the {label} bracket."
            if max_age is not None and age > max_age:
                return f"Age must be at most {max_age} for the {label} bracket."
            return True

        answer = questionary.text("Age", validate=validate).ask()
        return int(answer)
