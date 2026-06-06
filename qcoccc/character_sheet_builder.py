from .skills_data import SCHEMA_KEY, ARRAY_GROUPS


def _build_skills(skills: dict) -> dict:
    result = {}
    for display_name, value in skills.items():
        if "(" in display_name:
            group = display_name[: display_name.index("(")].strip()
            spec = display_name[display_name.index("(") + 1 : display_name.index(")")]
            schema_key = ARRAY_GROUPS.get(group)
            if schema_key:
                result.setdefault(schema_key, []).append({"name": spec, "value": value})
        else:
            schema_key = SCHEMA_KEY.get(display_name)
            if schema_key:
                result[schema_key] = value
    return result


def build(context: dict) -> dict:
    return {
        "era": context["era"],
        "identity": {
            "occupation": context["occupation"],
            "age": context["age"],
        },
        "characteristics": {
            "STR": context["STR"],
            "CON": context["CON"],
            "SIZ": context["SIZ"],
            "DEX": context["DEX"],
            "APP": context["APP"],
            "INT": context["INT"],
            "POW": context["POW"],
            "EDU": context["EDU"],
        },
        "derived_attributes": {
            "luck":          context["luck"],
            "sanity_points": context["sanity"],
            "max_sanity":    context["max_sanity"],
            "hit_points":    context["hp"],
            "magic_points":  context["magic_points"],
            "move_rate":     context["move_rate"],
            "damage_bonus":  context["damage_bonus"],
            "build":         context["build"],
        },
        "skills": _build_skills(context.get("skills", {})),
    }
