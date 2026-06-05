import json
import os
import jsonschema
from engine.flow import QuestionFlow
from questions.era import EraQuestion
from questions.occupation import OccupationQuestion, load_occupation_data
from questions.age_bracket import AgeBracketQuestion
from questions.age import AgeQuestion
from questions.skill_distribution import SkillDistributionQuestion
from questions.output import OutputQuestion
from character_sheet_builder import build
from characteristics import roll_characteristics
from skill_resolver import resolve_occupation_skills, allocate_skills

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "json-schemas", "character_sheet.schema.json")


def main():
    context = QuestionFlow([
        EraQuestion(),
        OccupationQuestion(),
        AgeBracketQuestion(),
        AgeQuestion(),
    ]).run()

    context.update(roll_characteristics(
        context["era"],
        context["occupation"],
        context["age_bracket"],
        context["age"],
    ))

    occ_data = load_occupation_data(context["occupation"], context["era"])
    resolved = resolve_occupation_skills(occ_data["skills"], context)

    context.update(QuestionFlow([
        SkillDistributionQuestion(),
        OutputQuestion(),
    ]).run())

    context["skills"] = allocate_skills(
        occ_data, resolved, context, context["distribution_mode"]
    )

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
