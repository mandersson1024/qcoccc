import random
import sys
import questionary
from .skills_data import BASE_VALUES, SPECIALIZATIONS, COMMON_LANGUAGES, ARRAY_GROUPS


def evaluate_formula(formula: str, context: dict) -> int:
    total = 0
    for term in formula.split(" + "):
        term = term.strip()
        if " or " in term:
            parts = [p.strip() for p in term.split(" or ")]
            total += max(_eval_term(p, context) for p in parts)
        else:
            total += _eval_term(term, context)
    return total


def _eval_term(term: str, context: dict) -> int:
    stat, mult = term.split(" * ")
    return context[stat.strip()] * int(mult.strip())


def _abort():
    print("\nAborted.")
    sys.exit(0)


def _ask(prompt_fn):
    result = prompt_fn()
    if result is None:
        _abort()
    return result


def skill_base(name: str, context: dict) -> int:
    if name == "Own Language":
        return context["EDU"]
    if name == "Dodge":
        return context["DEX"] // 2
    if "(" in name:
        group = name[:name.index("(")].strip()
        spec = name[name.index("(") + 1 : name.index(")")]
        return {n: base for n, base, _ in SPECIALIZATIONS.get(group, [])}.get(spec, 1)
    return BASE_VALUES.get(name, 1)


def _resolve_any_suffix(name: str, context: dict) -> str:
    group = name[: name.index("(")].strip()
    specs = SPECIALIZATIONS.get(group, [])
    spec_names = [s for s, _, _ in specs]
    spec_weights = [w for _, _, w in specs]

    if not spec_names:
        # Other Language — free text
        choice = _ask(lambda: questionary.select(
            "Other Language", choices=["ANY", "Enter name..."]
        ).ask())
        if choice == "ANY":
            lang = random.choice(COMMON_LANGUAGES)
            print(f"  → {lang}")
        else:
            lang = _ask(lambda: questionary.text("Language name:").ask())
        return f"Other Language ({lang})"

    choices = ["ANY"] + spec_names + ["Enter custom..."]
    spec = _ask(lambda: questionary.select(
        f"{group} specialization", choices=choices
    ).ask())
    if spec == "ANY":
        spec = random.choices(spec_names, weights=spec_weights)[0]
        print(f"  → {spec}")
    elif spec == "Enter custom...":
        spec = _ask(lambda: questionary.text(f"{group} specialization:").ask())
    return f"{group} ({spec})"


_FULL_SKILL_LIST: list[str] | None = None


def _get_full_skill_list() -> list[str]:
    global _FULL_SKILL_LIST
    if _FULL_SKILL_LIST is None:
        skills = []
        for name in sorted(BASE_VALUES):
            if name in ("Credit Rating", "Cthulhu Mythos"):
                continue
            skills.append(name)
        for group in sorted(SPECIALIZATIONS):
            specs = SPECIALIZATIONS[group]
            if specs:
                for spec_name, _, _ in specs:
                    skills.append(f"{group} ({spec_name})")
            else:
                skills.append(f"{group} (any)")
        _FULL_SKILL_LIST = sorted(skills)
    return _FULL_SKILL_LIST


def _available_from_full_list(chosen: set) -> list[str]:
    return [s for s in _get_full_skill_list() if s not in chosen]


def _available_from_choices(choices_val: list, chosen: set) -> list[str]:
    available = [s for s in choices_val if s not in chosen]
    return available if available else list(choices_val)


def _skill_weight(skill_name: str, weights: dict) -> float:
    key = skill_name[:skill_name.index("(")].strip() if "(" in skill_name else skill_name
    return weights.get(key, 1.0)


def _resolve_entry(entry, context: dict, counters: dict, chosen: set, skill_weights: dict) -> str | None:
    if isinstance(entry, str):
        if entry == "Credit Rating":
            return None
        if entry.endswith("(any)"):
            return _resolve_any_suffix(entry, context)
        return entry

    choices_val = entry["choice"]

    if choices_val == "any":
        counters["any"] += 1
        n = counters["any"]
        label = f"Any occupation skill {n}"
        available = _available_from_full_list(chosen)
        skill = _ask(lambda: questionary.select(
            label, choices=["ANY"] + available
        ).ask())
        if skill == "ANY":
            w = [_skill_weight(s, skill_weights) for s in available]
            skill = random.choices(available, weights=w)[0]
            print(f"  → {skill}")
        if skill.endswith("(any)"):
            skill = _resolve_any_suffix(skill, context)
        return skill

    if "label" in entry:
        label = f"Occupation skill ({entry['label']})"
    else:
        counters["choice"] += 1
        n = counters["choice"]
        label = f"Occupation skill {n}"
    available = _available_from_choices(choices_val, chosen)
    skill = _ask(lambda: questionary.select(
        label, choices=["ANY"] + available
    ).ask())
    if skill == "ANY":
        skill = random.choice(available)
        print(f"  → {skill}")
    if skill.endswith("(any)"):
        skill = _resolve_any_suffix(skill, context)
    return skill


def resolve_occupation_skills(skills_list: list, context: dict, skill_weights: dict | None = None) -> list[tuple[str, int]]:
    resolved = []
    chosen = set()
    counters = {"any": 0, "choice": 0}
    _weights = skill_weights or {}
    for entry in skills_list:
        name = _resolve_entry(entry, context, counters, chosen, _weights)
        if name is None:
            continue
        resolved.append((name, skill_base(name, context)))
        chosen.add(name)
    return resolved


def allocate_skills(
    occ_data: dict,
    resolved: list[tuple[str, int]],
    context: dict,
    mode: str,
) -> dict[str, int]:
    total = evaluate_formula(occ_data["skill_points"], context)

    cr_range = occ_data["credit_rating_range"]
    cr = random.randint(cr_range["min"], cr_range["max"])
    remaining = max(0, total - cr)

    # Deduplicate: if same skill picked twice, it shares one pool entry
    skill_bases: dict[str, int] = {}
    for name, base in resolved:
        if name not in skill_bases:
            skill_bases[name] = base

    if remaining > 0 and skill_bases:
        if mode == "Specialist":
            allocation = _distribute_skewed(skill_bases, remaining)
        else:
            allocation = _distribute_linear(skill_bases, remaining)
    else:
        allocation = {s: 0 for s in skill_bases}

    result = {"Credit Rating": cr}
    for name, base in skill_bases.items():
        result[name] = base + min(allocation.get(name, 0), max(0, _SKILL_CAP - base))
    return result


def resolve_personal_interest_skills(context: dict, exclude: set, n_skills: int = 4) -> list[str]:
    full_list = _get_full_skill_list()
    chosen = []
    chosen_set = set(exclude)
    for i in range(n_skills):
        label = f"Personal interest {i + 1}"
        available = _available_from_full_list(chosen_set)
        skill = _ask(lambda: questionary.select(label, choices=["ANY"] + available).ask())
        if skill == "ANY":
            skill = random.choice(available)
            print(f"  → {skill}")
        if skill.endswith("(any)"):
            skill = _resolve_any_suffix(skill, context)
        chosen.append(skill)
        chosen_set.add(skill)
    return chosen


def allocate_personal_interest(
    chosen: list[str],
    occupation_skills: dict[str, int],
    context: dict,
    mode: str,
) -> dict[str, int]:
    total = context["INT"] * 2
    skill_bases = {
        name: occupation_skills.get(name, skill_base(name, context))
        for name in chosen
    }
    if mode == "Specialist":
        allocation = _distribute_skewed(skill_bases, total)
    else:
        allocation = _distribute_linear(skill_bases, total)
    return {name: min(_SKILL_CAP, base + allocation.get(name, 0)) for name, base in skill_bases.items()}


_SKILL_CAP = 75


def _distribute_linear(skill_bases: dict, points: int) -> dict:
    allocated = {s: 0 for s in skill_bases}
    eligible = [s for s in skill_bases if skill_bases[s] < _SKILL_CAP]
    for _ in range(points):
        if not eligible:
            break
        s = random.choice(eligible)
        allocated[s] += 1
        if skill_bases[s] + allocated[s] >= _SKILL_CAP:
            eligible = [e for e in eligible if e != s]
    return allocated


def _distribute_skewed(skill_bases: dict, points: int) -> dict:
    weights = {s: random.expovariate(1) for s in skill_bases}
    total_w = sum(weights.values())
    allocated = {s: 0 for s in skill_bases}
    remaining = points
    for s in sorted(skill_bases, key=lambda x: -weights[x]):
        if remaining <= 0:
            break
        max_add = max(0, _SKILL_CAP - skill_bases[s])
        share = round(points * weights[s] / total_w)
        add = min(share, max_add, remaining)
        allocated[s] = add
        remaining -= add
    for s in random.sample(list(skill_bases), len(skill_bases)):
        if remaining <= 0:
            break
        can_add = max(0, _SKILL_CAP - skill_bases[s] - allocated[s])
        add = min(can_add, remaining)
        allocated[s] += add
        remaining -= add
    return allocated
