# qcoccc — Quick Call of Cthulhu Character Creator

A Python script that lets the user quickly roll a new Call of Cthulhu (7th edition) character.

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

**Occupation folders:** Occupations are defined as JSON files under `occupations/<era>/`. One file = one occupation. "Other" era loads all folders combined. Era determines which subfolder to load from — no separate era config file.

**Schema required fields:** Fields are optional in the schema by default and promoted to `required` as they get implemented. This allows the script to produce valid output at every stage of development, with validation tightening over time.

## Project structure

```
qcoccc.py                    — main entry point
character_sheet_builder.py   — assembles the character sheet dict from context
character_sheet.schema.json  — JSON Schema for the investigator sheet
engine/
    question.py              — abstract Question base class
    flow.py                  — QuestionFlow runner
questions/
    era.py
    occupation.py
    age_bracket.py
    age.py
    output.py
occupations/
    1920s/                   — occupation JSON files for the 1920s era
    modern/                  — occupation JSON files for the modern era
```

## Question flow

1. **Era** — 1920s / Modern / Other
2. **Occupation** — loaded from era subfolder(s), sorted alphabetically
3. **Age bracket** — rulebook brackets: 15–19, 20s, 30s, 40s, 50s, 60s, 70s, 80s+
4. **Age** — free-text integer, validated against the chosen bracket
5. **Output** — To Terminal / To File / Both
