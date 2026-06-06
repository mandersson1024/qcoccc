import argparse
import json
import os
import sys
import jsonschema
from .engine.flow import QuestionFlow
from .questions.era import EraQuestion
from .questions.occupation import OccupationQuestion, load_occupation_data
from .questions.age_bracket import AgeBracketQuestion
from .questions.age import AgeQuestion
from .questions.skill_distribution import SkillDistributionQuestion
from .questions.output import OutputQuestion
from .character_sheet_builder import build
from .pretty_print import format_sheet
from .characteristics import roll_characteristics
from .skill_resolver import resolve_occupation_skills, allocate_skills, resolve_personal_interest_skills, allocate_personal_interest, skill_base

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "json-schemas", "character_sheet.schema.json")


def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def pretty_print_file(path):
    with open(path) as f:
        sheet = json.load(f)

    schema = load_schema()
    try:
        jsonschema.validate(sheet, schema)
    except jsonschema.ValidationError as e:
        path_str = " -> ".join(str(p) for p in e.absolute_path) or "(root)"
        print(f"Schema validation failed at '{path_str}': {e.message}")
        sys.exit(1)

    print(format_sheet(sheet))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pretty-print", metavar="FILE", help="Pretty-print a character sheet JSON file")
    args = parser.parse_args()

    if args.pretty_print:
        pretty_print_file(args.pretty_print)
        return

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
    personal = resolve_personal_interest_skills(context, exclude={name for name, _ in resolved})

    context.update(QuestionFlow([
        SkillDistributionQuestion(),
    ]).run(context))

    occ_skills = allocate_skills(occ_data, resolved, context, context["distribution_mode"])
    personal_skills = allocate_personal_interest(personal, occ_skills, context, context["distribution_mode"])

    resolved_bases = {name: base for name, base in resolved}
    alloc_lines = [("Credit Rating", occ_skills["Credit Rating"])]
    for name, base in resolved_bases.items():
        alloc_lines.append((name, occ_skills[name] - base))
    for name in personal:
        pre = occ_skills.get(name, skill_base(name, context))
        alloc_lines.append((name, personal_skills[name] - pre))
    col = max(len(name) for name, _ in alloc_lines)
    for name, pts in alloc_lines:
        print(f"  → {name:<{col}}  {pts}")

    context["skills"] = occ_skills
    context["skills"].update(personal_skills)

    context.update(QuestionFlow([
        OutputQuestion(),
    ]).run(context))

    sheet = build(context)

    schema = load_schema()

    try:
        jsonschema.validate(sheet, schema)
    except jsonschema.ValidationError as e:
        path = " -> ".join(str(p) for p in e.absolute_path) or "(root)"
        print(f"\nSchema validation failed at '{path}': {e.message}")

    output = context["output"]
    destination = output["destination"]
    formatted = json.dumps(sheet, indent=2)

    if destination in ("To Terminal", "Both"):
        print(format_sheet(sheet))

    if destination in ("To File", "Both"):
        filename = output["filename"]
        with open(filename, "w") as f:
            f.write(formatted)
        print(f"Written to {filename}")
