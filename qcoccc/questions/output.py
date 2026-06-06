import questionary
from ..engine.question import Question


class OutputQuestion(Question):
    @property
    def key(self) -> str:
        return "output"

    def ask(self, context: dict) -> dict:
        destination = questionary.select(
            "Output",
            choices=["To Terminal", "To File", "Both"],
        ).ask()

        filename = None
        if destination in ("To File", "Both"):
            occupation_slug = context["occupation"].lower().replace(" ", "-")
            default = f"{context['era']}-{occupation_slug}-{context['age']}.json"
            filename = questionary.text(
                "Filename",
                default=default,
            ).ask()

        return {"destination": destination, "filename": filename}
