import json
import os
import random

import jsonschema
import pytest

from qcoccc.character_sheet_builder import build
from qcoccc.characteristics import roll_characteristics
from qcoccc.questions.age_bracket import BRACKETS
from qcoccc.questions.occupation import load_occupation_data
from qcoccc.skill_resolver import _get_full_skill_list, skill_base as _skill_base, allocate_personal_interest, allocate_skills
from qcoccc.skills_data import COMMON_LANGUAGES, SPECIALIZATIONS

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "json-schemas", "character_sheet.schema.json")
OCCUPATIONS_DIR = os.path.join(os.path.dirname(__file__), "..", "occupations")

_ERA_BY_FOLDER = {
    "era-neutral": "1920s",
    "1920s": "1920s",
    "modern": "Modern",
}


def _all_occupations():
    params = []
    for folder_name, era in _ERA_BY_FOLDER.items():
        folder = os.path.join(OCCUPATIONS_DIR, folder_name)
        if not os.path.isdir(folder):
            continue
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".json"):
                with open(os.path.join(folder, filename)) as f:
                    name = json.load(f)["name"]
                params.append(pytest.param(name, era, id=name))
    return params


def _resolve_spec_randomly(name: str) -> str:
    group = name[: name.index("(")].strip()
    specs = SPECIALIZATIONS.get(group, [])
    if specs:
        spec = random.choices([s for s, _, _ in specs], weights=[w for _, _, w in specs])[0]
    else:
        spec = random.choice(COMMON_LANGUAGES)
    return f"{group} ({spec})"


def _resolve_randomly(skills_list: list, context: dict) -> list[tuple[str, int]]:
    full_list = _get_full_skill_list()
    resolved = []
    for entry in skills_list:
        if isinstance(entry, str):
            if entry == "Credit Rating":
                continue
            name = _resolve_spec_randomly(entry) if entry.endswith("(any)") else entry
        else:
            choices_val = entry["choice"]
            chosen = random.choice(full_list) if choices_val == "any" else random.choice(choices_val)
            name = _resolve_spec_randomly(chosen) if chosen.endswith("(any)") else chosen
        resolved.append((name, _skill_base(name, context)))
    return resolved


def _random_age(bracket: tuple) -> int:
    _, lo, hi = bracket
    return random.randint(lo, hi if hi is not None else 90)


@pytest.mark.parametrize("occupation_name,era", _all_occupations())
def test_character_validates_against_schema(occupation_name, era):
    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    bracket = random.choice(BRACKETS)
    age = _random_age(bracket)
    occ_data = load_occupation_data(occupation_name, era)

    context = {
        "era": era,
        "occupation": occupation_name,
        "age_bracket": bracket,
        "age": age,
    }
    context.update(roll_characteristics(era, occupation_name, bracket, age))

    resolved = _resolve_randomly(occ_data["skills"], context)
    mode = random.choice(["Generalist", "Specialist"])
    context["skills"] = allocate_skills(occ_data, resolved, context, mode)
    full_list = [s for s in _get_full_skill_list() if not s.endswith("(any)")]
    personal = random.sample(full_list, 4)
    context["skills"].update(allocate_personal_interest(personal, context["skills"], context, mode))

    sheet = build(context)
    jsonschema.validate(sheet, schema)
