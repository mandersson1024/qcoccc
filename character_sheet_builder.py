def build(context: dict) -> dict:
    return {
        "era": context["era"],
        "identity": {
            "occupation": context["occupation"],
            "age": context["age"],
        },
    }
