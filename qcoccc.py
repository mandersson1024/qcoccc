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

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "character_sheet.schema.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output.json")


def main():
    flow = QuestionFlow(questions=[
        EraQuestion(),
        OccupationQuestion(),
        AgeBracketQuestion(),
        AgeQuestion(),
        OutputQuestion(),
    ])
    context = flow.run()

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
    formatted = json.dumps(sheet, indent=2)

    if output in ("To Terminal", "Both"):
        print(formatted)

    if output in ("To File", "Both"):
        with open(OUTPUT_PATH, "w") as f:
            f.write(formatted)
        print(f"Written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
