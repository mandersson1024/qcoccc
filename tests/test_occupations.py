import json
import os
import pytest
import jsonschema

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "json-schemas", "occupation.schema.json")
OCCUPATIONS_PATH = os.path.join(os.path.dirname(__file__), "..", "occupations")


def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def all_occupation_files():
    files = []
    for era in os.listdir(OCCUPATIONS_PATH):
        era_dir = os.path.join(OCCUPATIONS_PATH, era)
        if not os.path.isdir(era_dir):
            continue
        for filename in os.listdir(era_dir):
            if filename.endswith(".json"):
                files.append(os.path.join(era_dir, filename))
    return sorted(files)


@pytest.mark.parametrize("path", all_occupation_files())
def test_occupation_validates_against_schema(path):
    schema = load_schema()
    with open(path) as f:
        data = json.load(f)
    jsonschema.validate(data, schema)
