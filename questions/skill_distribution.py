import questionary
from engine.question import Question


class SkillDistributionQuestion(Question):
    allow_any = False

    @property
    def key(self) -> str:
        return "distribution_mode"

    def ask(self, context: dict) -> str:
        return questionary.select(
            "Skill distribution",
            choices=["Generalist", "Specialist"],
        ).ask()
