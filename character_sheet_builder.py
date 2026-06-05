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
        "skills": {
            "dodge": context["dodge"],
        },
    }
