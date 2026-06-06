# qcoccc — Quick Call of Cthulhu Character Creator

A Python script that lets the user quickly roll a new Call of Cthulhu (7th edition) character. The main use case is generating a quick NPC on the spot, or a quick replacement character to be fleshed out later. Speed is the priority — not completeness.

## Rules reference

The rulebook is `CoC-7e-rules.pdf` (gitignored). All mechanics must follow the 7th edition rules as written in that document.

## Development process

The developer owns all decisions about how the project works. Work in small steps, one thing at a time.

- When asked to **think** about something, discuss trade-offs and form a plan if appropriate. Do not write code.
- Do not suggest next steps, propose features, or start implementing anything unless explicitly asked.
- Ask clarifying questions before forming a plan.
- Present the plan and wait for explicit approval before writing any code.
- Ask first, then do.
- Never commit to git. All commits are done manually by the developer.
- Do not use memory files for project-specific information. Everything goes in CLAUDE.md.

## Design decisions

**Era-specific skills:** The schema defines all skills as a superset across all eras. Era logic (which skills are available) lives in the Python script. The schema has a top-level `era` field as a meta property of the sheet.

**Occupation folders:** Occupations are defined as JSON files under `occupations/`. One file = one occupation. Era-specific occupations go in `occupations/1920s/` or `occupations/modern/`. Occupations available in all eras go in `occupations/era-neutral/`. "Other" era loads all folders combined. Era determines which subfolders to load from (era folder + era-neutral) — no separate era config file.

**Schema required fields:** Fields are optional in the schema by default and promoted to `required` as they get implemented. This allows the script to produce valid output at every stage of development, with validation tightening over time.

**ANY option:** Select questions can offer "ANY" as the first choice, which resolves to a random value from the remaining options. The resolved value is printed on the next line (`→ value`). Free-text questions (like age) use empty input to trigger the same behaviour. The `allow_any` flag on the `Question` base class controls whether a question supports this. The `Output` question does not offer ANY.

**Characteristics and skills are plain integers:** The output sheet stores characteristics and skills as plain integers (e.g. `"STR": 45`, `"dodge": 21`). Half and fifth values are not stored — players calculate those at the table.

**Ctrl+C exits cleanly:** questionary's `ask()` returns `None` on Ctrl+C. The `QuestionFlow` runner checks for `None` after each question and exits with `Aborted.` instead of crashing.

**Skill cap at character creation:** No skill may exceed 75% through point allocation during character creation. This is the cap recommended in the Investigator's Handbook (no PDF available). Skills whose base value already equals or exceeds 75 receive no additional points. Credit Rating is exempt — it is set directly from the occupation's range, not via the distribution pool.

**Occupational skill point distribution:** Points are distributed randomly. Generalist mode assigns each point uniformly at random across the skill pool. Specialist mode draws weights from `random.expovariate(1)` — a skewed distribution — so one or two skills attract most of the points. Credit Rating is set to a random value within the occupation's range and its cost is deducted from the pool before distribution. Manual point allocation is not implemented (backlog).

**Age range:** The rules explicitly state investigators must be between 15 and 90 years old (rulebook p. 32). The 80s+ bracket covers 80–90. Ages outside this range require Keeper approval and are not supported by the tool.

**Characteristic rolling — standard method only:** STR/CON/DEX/APP/POW roll 3D6×5; SIZ/INT/EDU roll 2D6+6×5. Occupation `characteristic_ranges.min` values are enforced (stat bumped up if below minimum). `max` values are soft guidance — not enforced. Age deductions to STR/CON/DEX are distributed randomly across the three stats. Other rolling methods (Quick Fire, point buy, allocate-freely) are not implemented yet.

**Specialization weights:** Each entry in `SPECIALIZATIONS` is a `(name, base_value, weight)` tuple. Weight is used when resolving ANY — higher weight means more likely. Base values come from the rulebook; weights are curated by feel to make unusual specializations possible but rare (e.g. Brawl weight 50 vs Chainsaw weight 4, Boat weight 50 vs Submarine weight 5).

**Schema validation is permissive at runtime:** After building the sheet, `qcoccc.py` validates it against `character_sheet.schema.json` and prints any error, but continues to render and write the sheet regardless.

**`-p` / `--pretty-print` flag:** `python -m qcoccc -p <file.json>` loads a character sheet JSON, validates it against the schema, and prints the formatted sheet. If validation fails, it prints the error and exits without printing the sheet.

**`QuestionFlow.run()` accepts an initial context:** The second `QuestionFlow` call (for skill distribution and output questions) is seeded with the accumulated context so that `OutputQuestion` can read `occupation`, `era`, and `age` when generating the default filename.

## Project structure

```
qcoccc/                      — Python package; run with: python -m qcoccc
    __main__.py              — entry point for python -m qcoccc
    main.py                  — main() function; -p/--pretty-print flag to render an existing JSON sheet
    character_sheet_builder.py — assembles the character sheet dict from context
    characteristics.py       — rolls all 8 characteristics, applies age modifiers, derives attributes
    skills_data.py           — base values, specialization lists, display→schema key mappings
    skill_resolver.py        — resolves occupation skill entries interactively, evaluates formulas, distributes points
    pretty_print.py          — formats the character sheet as human-readable text for terminal output
    engine/
        question.py          — abstract Question base class (allow_any flag)
        flow.py              — QuestionFlow runner; run() accepts an optional seed context
    questions/
        era.py
        occupation.py        — also exposes load_occupation_data(name, era)
        age_bracket.py
        age.py
        skill_distribution.py
        output.py
json-schemas/
    character_sheet.schema.json  — JSON Schema for the investigator sheet
    occupation.schema.json       — JSON Schema for occupation files
occupations/
    era-neutral/             — occupation JSON files available in all eras
    1920s/                   — occupation JSON files exclusive to the 1920s era
    modern/                  — occupation JSON files exclusive to the modern era
tests/
    test_occupations.py      — validates all occupation JSON files against json-schemas/occupation.schema.json
    test_skills.py           — unit tests for skill base values, formula evaluation, and point allocation
    test_character_sheet.py  — generates a random character for each occupation and validates against character_sheet.schema.json
requirements.txt
```

## Current status

Roadmap items 1, 2, and 3 are **complete**.

Item 1 (full occupation list):
- All occupation JSON files created and validated against `occupation.schema.json`
- 19 era-neutral occupations in `occupations/era-neutral/`
- 8 1920s-exclusive occupations in `occupations/1920s/`
- 1 modern-exclusive occupation in `occupations/modern/` (hacker)
- `tests/test_occupations.py` validates all 28 occupation files — all passing

Item 2 (characteristic rolling):
- Standard rolling method implemented in `characteristics.py`
- Occupation minimums enforced, age modifiers applied, all derived attributes computed
- Output sheet now includes `characteristics` and `derived_attributes`

Item 5 (pretty-print output):
- `pretty_print.py` formats the sheet as a readable character sheet for terminal output
- Terminal destination now shows the formatted sheet; file destination still writes JSON
- Skills sorted alphabetically, specializations shown as "Group (Name)"

Item 4 (personal interest skill points):
- 4 skills chosen at random from the full skill list; "Other Language (any)" auto-resolved silently
- INT × 2 points distributed using the same mode (uniform/bell curve) chosen for occupation
- Results merged into the skills dict; occupation-improved skills continue from their occupation value
- Chosen skills printed for visibility before output

Item 3 (occupational skill points):
- `skills_data.py` defines base values for all skills and specialization lists (Fighting, Firearms, Art/Craft, Science, Pilot, Survival, Other Language)
- `skill_resolver.py` handles formula evaluation, interactive skill resolution (choices and specializations), and point distribution (linear or bell curve)
- Occupation skill point formula parsed and evaluated; Credit Rating set randomly within occupation range
- Skill choices (`{"choice": [...]}`, `{"choice": "any"}`) and `(any)` specializations presented as interactive questions with ANY option
- Output sheet now includes `skills`

**All roadmap items complete.**

## Roadmap

Planned order of implementation:

1. ✅ **Full occupation list** — foundation for everything else; each occupation gets occupational skills and reasonable characteristic ranges (soft guidance, not hard rules — e.g. a soldier is unlikely to have very low STR)
2. ✅ **Characteristic rolling** — roll all 8 characteristics per the rules, apply occupation characteristic ranges and age modifiers, derive HP, MP, move rate, damage bonus, build, Luck and Sanity
3. ✅ **Occupational skill points** — allocate EDU × multiplier across the occupation's skills
4. ✅ **Personal interest skill points** — allocate INT × 2 freely across any skills, independent of occupation
5. ✅ **Pretty-print output** — human-readable character sheet to terminal, not just formatted JSON

Out of scope: backstory generation, partial sheet saving/loading, re-rolling individual values.

## Question flow

1. **Era** — 1920s / Modern / Other
2. **Occupation** — loaded from era subfolder(s), sorted alphabetically
3. **Age bracket** — rulebook brackets: 15–19, 20s, 30s, 40s, 50s, 60s, 70s, 80s+
4. **Age** — free-text integer, validated against the chosen bracket
5. **Skill choices** — one question per `{"choice": [...]}` or `{"choice": "any"}` entry in the occupation; `(any)` suffixes trigger a specialization sub-question
6. **Skill distribution** — Generalist / Specialist
7. **Output** — To Terminal / To File / Both (no ANY)
