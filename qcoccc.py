import json
import os
import jsonschema
from engine.flow import QuestionFlow
from questions.era import EraQuestion
from questions.occupation import OccupationQuestion
from questions.age_bracket import AgeBracketQuestion
from questions.age import AgeQuestion
from questions.output import OutputQuestion
from character_sheet_builder import build
from characteristics import roll_characteristics

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "json-schemas", "character_sheet.schema.json")


def main():
    flow = QuestionFlow(questions=[
        EraQuestion(),
        OccupationQuestion(),
        AgeBracketQuestion(),
        AgeQuestion(),
        OutputQuestion(),
    ])
    context = flow.run()
    context.update(roll_characteristics(
        context["era"],
        context["occupation"],
        context["age_bracket"],
        context["age"],
    ))

    sheet = build(context)

    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    try:
        jsonschema.validate(sheet, schema)
    except jsonschema.ValidationError as e:
        path = " -> ".join(str(p) for p in e.absolute_path) or "(root)"
        print(f"\nSchema validation failed at '{path}': {e.message}")
        return

    output = context["output"]
    destination = output["destination"]
    formatted = json.dumps(sheet, indent=2)

    if destination in ("To Terminal", "Both"):
        print(formatted)

    if destination in ("To File", "Both"):
        filename = output["filename"]
        with open(filename, "w") as f:
            f.write(formatted)
        print(f"Written to {filename}")


if __name__ == "__main__":
    main()
