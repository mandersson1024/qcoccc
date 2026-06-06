import pytest

from qcoccc.skills_data import BASE_VALUES, SPECIALIZATIONS
from qcoccc.skill_resolver import skill_base as _skill_base, evaluate_formula, allocate_skills, _available_from_full_list, _available_from_choices, _get_full_skill_list


CTX = {"EDU": 70, "DEX": 60, "INT": 65, "STR": 55, "POW": 50, "APP": 45}

OCC_DATA = {
    "skill_points": "EDU * 4",
    "credit_rating_range": {"min": 10, "max": 50},
}


# ── Base values ───────────────────────────────────────────────────────────────

@pytest.mark.parametrize("skill, expected", [
    ("Accounting",            5),
    ("Charm",                15),
    ("Climb",                20),
    ("Computer Use",          5),
    ("Disguise",              5),
    ("Drive Auto",           20),
    ("Electrical Repair",    10),
    ("Electronics",           1),
    ("Fast Talk",             5),
    ("First Aid",            30),
    ("History",               5),
    ("Intimidate",           15),
    ("Jump",                 20),
    ("Law",                   5),
    ("Library Use",          20),
    ("Listen",               20),
    ("Locksmith",             1),
    ("Mechanical Repair",    10),
    ("Medicine",              1),
    ("Natural World",        10),
    ("Navigate",             10),
    ("Occult",                5),
    ("Operate Heavy Machinery", 1),
    ("Persuade",             10),
    ("Psychoanalysis",        1),
    ("Psychology",           10),
    ("Ride",                  5),
    ("Sleight of Hand",      10),
    ("Spot Hidden",          25),
    ("Stealth",              20),
    ("Swim",                 20),
    ("Throw",                20),
    ("Track",                10),
    ("Anthropology",          1),
    ("Appraise",              5),
    ("Archaeology",           1),
    ("Credit Rating",         0),
])
def test_plain_skill_base(skill, expected):
    assert _skill_base(skill, CTX) == expected


@pytest.mark.parametrize("skill, expected", [
    ("Fighting (Brawl)",      25),
    ("Fighting (Axe)",        15),
    ("Fighting (Chainsaw)",   10),
    ("Fighting (Flail)",      10),
    ("Fighting (Garrote)",    15),
    ("Fighting (Spear)",      20),
    ("Fighting (Sword)",      20),
    ("Fighting (Whip)",        5),
    ("Firearms (Bow)",        15),
    ("Firearms (Handgun)",    20),
    ("Firearms (Heavy Weapons)", 10),
    ("Firearms (Flamethrower)", 10),
    ("Firearms (Machine Gun)", 10),
    ("Firearms (Rifle/Shotgun)", 25),
    ("Firearms (Submachine Gun)", 15),
    ("Science (Astronomy)",    1),
    ("Science (Biology)",      1),
    ("Science (Chemistry)",    1),
    ("Science (Mathematics)", 10),
    ("Science (Physics)",      1),
    ("Pilot (Aircraft)",       1),
    ("Survival (Arctic)",     10),
    ("Survival (Desert)",     10),
    ("Art/Craft (Acting)",     5),
    ("Art/Craft (Photography)", 5),
    ("Other Language (Latin)", 1),
])
def test_specialization_base(skill, expected):
    assert _skill_base(skill, CTX) == expected


def test_dodge_base_is_half_dex():
    ctx = {**CTX, "DEX": 60}
    assert _skill_base("Dodge", ctx) == 30


def test_dodge_base_rounds_down():
    ctx = {**CTX, "DEX": 65}
    assert _skill_base("Dodge", ctx) == 32


def test_own_language_base_equals_edu():
    ctx = {**CTX, "EDU": 72}
    assert _skill_base("Own Language", ctx) == 72


# ── Formula evaluation ────────────────────────────────────────────────────────

def test_formula_simple_multiplier():
    assert evaluate_formula("EDU * 4", CTX) == 70 * 4


def test_formula_two_terms():
    assert evaluate_formula("EDU * 2 + DEX * 2", CTX) == 70 * 2 + 60 * 2


def test_formula_or_takes_max():
    # EDU*2 + max(DEX*2, STR*2) — DEX=60, STR=55, so DEX wins
    assert evaluate_formula("EDU * 2 + DEX * 2 or STR * 2", CTX) == 70 * 2 + 60 * 2


def test_formula_or_takes_higher_value():
    ctx = {**CTX, "DEX": 40, "STR": 70}
    assert evaluate_formula("EDU * 2 + DEX * 2 or STR * 2", ctx) == 70 * 2 + 70 * 2


# ── Allocation ────────────────────────────────────────────────────────────────

def _allocate(resolved, mode="Generalist", occ=OCC_DATA, ctx=CTX):
    return allocate_skills(occ, resolved, ctx, mode)


def test_allocation_starts_from_base_not_zero():
    resolved = [("First Aid", 30), ("History", 5)]
    result = _allocate(resolved)
    # Final value must be at least the base value even with 0 extra points
    assert result["First Aid"] >= 30
    assert result["History"] >= 5


def test_allocation_adds_on_top_of_base():
    # With EDU*4 = 280 points and 2 skills, both must end up above their bases
    resolved = [("Medicine", 1), ("Psychology", 10)]
    result = _allocate(resolved)
    assert result["Medicine"] >= 1
    assert result["Psychology"] >= 10


def test_skill_capped_at_75():
    # Single skill in the pool guarantees all points go to it — must be exactly 75
    occ = {"skill_points": "EDU * 4", "credit_rating_range": {"min": 0, "max": 0}}
    result = allocate_skills(occ, [("First Aid", 30)], CTX, "Generalist")
    assert result["First Aid"] == 75


def test_skill_above_75_base_receives_no_points():
    # If base already at or above cap, no points should be added
    occ = {"skill_points": "EDU * 4", "credit_rating_range": {"min": 0, "max": 0}}
    result = allocate_skills(occ, [("Own Language", 80)], CTX, "Generalist")
    assert result["Own Language"] == 80


def test_credit_rating_within_occupation_range():
    occ = {"skill_points": "EDU * 4", "credit_rating_range": {"min": 20, "max": 70}}
    for _ in range(30):
        result = allocate_skills(occ, [("History", 5)], CTX, "Generalist")
        assert 20 <= result["Credit Rating"] <= 70


def test_credit_rating_min_zero():
    occ = {"skill_points": "EDU * 4", "credit_rating_range": {"min": 0, "max": 15}}
    for _ in range(20):
        result = allocate_skills(occ, [("History", 5)], CTX, "Generalist")
        assert 0 <= result["Credit Rating"] <= 15


def test_excess_points_redistributed_when_skill_hits_cap():
    # First Aid (base 70) has only 5 points of headroom before hitting the cap.
    # With 20 points to distribute across two skills, the 15 that can't go into
    # First Aid must flow to Psychology — none should be wasted.
    occ = {"skill_points": "EDU * 2", "credit_rating_range": {"min": 0, "max": 0}}
    ctx = {**CTX, "EDU": 10}  # EDU * 2 = 20 points
    resolved = [("First Aid", 70), ("Psychology", 10)]
    result = allocate_skills(occ, resolved, ctx, "Generalist")
    assert result["First Aid"] == 75
    # All 20 points must be accounted for across both skills (none wasted)
    assert (result["First Aid"] - 70) + (result["Psychology"] - 10) == 20


def test_duplicate_skill_entries_merged():
    # Same skill chosen twice — should appear once with points allocated once
    resolved = [("Psychology", 10), ("Psychology", 10)]
    result = _allocate(resolved)
    assert list(result.keys()).count("Psychology") == 1
    assert result["Psychology"] >= 10


# ── Skill availability filtering ──────────────────────────────────────────────

def test_available_from_full_list_excludes_chosen():
    chosen = {"History", "Psychology", "Charm"}
    available = _available_from_full_list(chosen)
    for skill in chosen:
        assert skill not in available


def test_available_from_full_list_empty_chosen_returns_full_list():
    assert _available_from_full_list(set()) == _get_full_skill_list()


def test_available_from_full_list_excludes_specialization():
    chosen = {"Fighting (Brawl)"}
    available = _available_from_full_list(chosen)
    assert "Fighting (Brawl)" not in available
    assert "Fighting (Axe)" in available


def test_available_from_choices_excludes_chosen():
    choices = ["Charm", "Fast Talk", "Intimidate", "Persuade"]
    available = _available_from_choices(choices, {"Charm", "Fast Talk"})
    assert "Charm" not in available
    assert "Fast Talk" not in available
    assert "Intimidate" in available
    assert "Persuade" in available


def test_available_from_choices_falls_back_when_all_taken():
    choices = ["Charm", "Fast Talk"]
    available = _available_from_choices(choices, {"Charm", "Fast Talk"})
    assert available == ["Charm", "Fast Talk"]


def test_personal_interest_excludes_occupation_skills():
    occupation_skills = {"History", "Psychology", "Library Use", "Spot Hidden"}
    available = _available_from_full_list(occupation_skills)
    for skill in occupation_skills:
        assert skill not in available


def test_personal_interest_excludes_previous_personal_interest_picks():
    first_pick = "Charm"
    available_after_first = _available_from_full_list({first_pick})
    assert first_pick not in available_after_first

    second_pick = "History"
    available_after_second = _available_from_full_list({first_pick, second_pick})
    assert first_pick not in available_after_second
    assert second_pick not in available_after_second
