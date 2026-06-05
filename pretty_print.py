from skills_data import SCHEMA_KEY, ARRAY_GROUPS

_DISPLAY = {v: k for k, v in SCHEMA_KEY.items()}
_GROUP_DISPLAY = {v: k for k, v in ARRAY_GROUPS.items()}

WIDTH = 48


def _border():
    return "═" * WIDTH


def _section(title):
    fill = "─" * (WIDTH - 2 - len(title) - 1)
    return f"  {title} {fill}"


def _skill_line(name, value):
    prefix = f"  {name} "
    dots = "." * max(2, 42 - len(prefix))
    return f"{prefix}{dots}  {value}"


def _skills_flat(skills):
    rows = []
    for key, val in skills.items():
        if isinstance(val, list):
            group = _GROUP_DISPLAY.get(key, key)
            for entry in val:
                rows.append((f"{group} ({entry['name']})", entry["value"]))
        else:
            rows.append((_DISPLAY.get(key, key), val))
    return sorted(rows)


def format_sheet(sheet):
    c = sheet["characteristics"]
    d = sheet["derived_attributes"]
    identity = sheet["identity"]

    lines = [
        _border(),
        f"  CALL OF CTHULHU INVESTIGATOR  ·  {sheet['era']}",
        _border(),
        "",
        f"  {identity['occupation']}  ·  Age {identity['age']}",
        "",
        _section("CHARACTERISTICS"),
        f"  STR {c['STR']:<4} CON {c['CON']:<4} SIZ {c['SIZ']:<4} DEX {c['DEX']}",
        f"  APP {c['APP']:<4} INT {c['INT']:<4} POW {c['POW']:<4} EDU {c['EDU']}",
        "",
        _section("DERIVED"),
        f"  Hit Points    {d['hit_points']:<6} Sanity    {d['sanity_points']} / {d['max_sanity']}",
        f"  Magic Points  {d['magic_points']:<6} Luck      {d['luck']}",
        f"  Move Rate     {d['move_rate']:<6} Build     {d['build']}",
        f"  Damage Bonus  {d['damage_bonus']}",
    ]

    if sheet.get("skills"):
        lines += ["", _section("SKILLS")]
        for name, value in _skills_flat(sheet["skills"]):
            lines.append(_skill_line(name, value))

    lines += ["", _border()]
    return "\n".join(lines)
