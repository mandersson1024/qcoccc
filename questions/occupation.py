import json
import os
import random
import questionary
from engine.question import Question

OCCUPATIONS_DIR = os.path.join(os.path.dirname(__file__), "..", "occupations")


def _load_occupations(era: str) -> list[str]:
    if era == "Other":
        folders = [
            os.path.join(OCCUPATIONS_DIR, d)
            for d in os.listdir(OCCUPATIONS_DIR)
            if os.path.isdir(os.path.join(OCCUPATIONS_DIR, d))
        ]
    else:
        folders = [
            os.path.join(OCCUPATIONS_DIR, era),
            os.path.join(OCCUPATIONS_DIR, "era-neutral"),
        ]

    names = set()
    for folder in folders:
        for filename in os.listdir(folder):
            if filename.endswith(".json"):
                with open(os.path.join(folder, filename)) as f:
                    names.add(json.load(f)["name"])

    return sorted(names)


class OccupationQuestion(Question):
    allow_any = True

    @property
    def key(self) -> str:
        return "occupation"

    def ask(self, context: dict) -> str:
        occupations = _load_occupations(context["era"])
        choice = questionary.select(
            "Occupation",
            choices=["ANY"] + occupations,
        ).ask()
        if choice == "ANY":
            result = random.choice(occupations)
            print(f"  → {result}")
            return result
        return choice
