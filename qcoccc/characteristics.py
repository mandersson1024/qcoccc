import random
from .questions.occupation import load_occupation_data


def _d(sides):
    return random.randint(1, sides)


def _roll3d6x5():
    return (_d(6) + _d(6) + _d(6)) * 5


def _roll2d6p6x5():
    return (_d(6) + _d(6) + 6) * 5


def _edu_improvement_check(edu: int) -> int:
    if random.randint(1, 100) > edu:
        edu = min(99, edu + _d(10))
    return edu


def _distribute_deduction(stats: dict, keys: list[str], total: int) -> None:
    remaining = total
    eligible = [k for k in keys if stats[k] > 1]
    while remaining > 0 and eligible:
        key = random.choice(eligible)
        stats[key] -= 1
        remaining -= 1
        if stats[key] <= 1:
            eligible = [k for k in eligible if k != key]


def _apply_age_modifiers(stats: dict, label: str) -> int:
    if label == "15–19":
        target = random.choice(["STR", "SIZ"])
        stats[target] = max(1, stats[target] - 5)
        stats["EDU"] = max(1, stats["EDU"] - 5)
        luck = max(_roll3d6x5(), _roll3d6x5())

    elif label in ("20s", "30s"):
        stats["EDU"] = _edu_improvement_check(stats["EDU"])
        luck = _roll3d6x5()

    elif label == "40s":
        for _ in range(2):
            stats["EDU"] = _edu_improvement_check(stats["EDU"])
        _distribute_deduction(stats, ["STR", "CON", "DEX"], 5)
        stats["APP"] = max(1, stats["APP"] - 5)
        luck = _roll3d6x5()

    elif label == "50s":
        for _ in range(3):
            stats["EDU"] = _edu_improvement_check(stats["EDU"])
        _distribute_deduction(stats, ["STR", "CON", "DEX"], 10)
        stats["APP"] = max(1, stats["APP"] - 10)
        luck = _roll3d6x5()

    elif label == "60s":
        for _ in range(4):
            stats["EDU"] = _edu_improvement_check(stats["EDU"])
        _distribute_deduction(stats, ["STR", "CON", "DEX"], 20)
        stats["APP"] = max(1, stats["APP"] - 15)
        luck = _roll3d6x5()

    elif label == "70s":
        for _ in range(4):
            stats["EDU"] = _edu_improvement_check(stats["EDU"])
        _distribute_deduction(stats, ["STR", "CON", "DEX"], 40)
        stats["APP"] = max(1, stats["APP"] - 20)
        luck = _roll3d6x5()

    else:  # 80s+
        for _ in range(4):
            stats["EDU"] = _edu_improvement_check(stats["EDU"])
        _distribute_deduction(stats, ["STR", "CON", "DEX"], 80)
        stats["APP"] = max(1, stats["APP"] - 25)
        luck = _roll3d6x5()

    return luck


def _move_rate(str_val: int, dex_val: int, siz_val: int, label: str) -> int:
    if str_val < siz_val and dex_val < siz_val:
        mov = 7
    elif str_val > siz_val and dex_val > siz_val:
        mov = 9
    else:
        mov = 8
    age_penalties = {"40s": 1, "50s": 2, "60s": 3, "70s": 4, "80s+": 5}
    return max(1, mov - age_penalties.get(label, 0))


def _damage_bonus_and_build(str_val: int, siz_val: int) -> tuple[str, int]:
    total = str_val + siz_val
    if total <= 64:   return "-2", -2
    if total <= 84:   return "-1", -1
    if total <= 124:  return "None", 0
    if total <= 164:  return "+1D4", 1
    if total <= 204:  return "+1D6", 2
    if total <= 284:  return "+2D6", 3
    if total <= 364:  return "+3D6", 4
    if total <= 444:  return "+4D6", 5
    return "+5D6", 6


def roll_characteristics(era: str, occupation_name: str, age_bracket: tuple, age: int) -> dict:
    label = age_bracket[0]

    stats = {
        "STR": _roll3d6x5(),
        "CON": _roll3d6x5(),
        "DEX": _roll3d6x5(),
        "APP": _roll3d6x5(),
        "POW": _roll3d6x5(),
        "SIZ": _roll2d6p6x5(),
        "INT": _roll2d6p6x5(),
        "EDU": _roll2d6p6x5(),
    }

    occ_data = load_occupation_data(occupation_name, era)
    for stat, rng in occ_data.get("characteristic_ranges", {}).items():
        if "min" in rng and stats[stat] < rng["min"]:
            stats[stat] = rng["min"]

    luck = _apply_age_modifiers(stats, label)

    db, build = _damage_bonus_and_build(stats["STR"], stats["SIZ"])

    return {
        **stats,
        "luck":         luck,
        "hp":           (stats["CON"] + stats["SIZ"]) // 10,
        "sanity":       stats["POW"],
        "max_sanity":   99,
        "magic_points": stats["POW"] // 5,
        "move_rate":    _move_rate(stats["STR"], stats["DEX"], stats["SIZ"], label),
        "damage_bonus": db,
        "build":        build,
        "dodge":        stats["DEX"] // 2,
    }
