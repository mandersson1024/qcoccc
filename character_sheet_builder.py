def build(context: dict) -> dict:
    return {
        "era": context["era"],
        "identity": {
            "name": "TBD",
            "occupation": context["occupation"],
            "age": context["age"],
            "sex": "TBD",
            "birthplace": "TBD",
            "residence": "TBD",
        },
        "characteristics": "TBD",
        "derived_attributes": "TBD",
        "skills": "TBD",
        "backstory": "TBD",
        "finances": "TBD",
    }
