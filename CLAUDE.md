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

**Occupation folders:** Occupations are defined as JSON files under `occupations/<era>/`. One file = one occupation. "Other" era loads all folders combined. Era determines which subfolder to load from — no separate era config file.

**Schema required fields:** Fields are optional in the schema by default and promoted to `required` as they get implemented. This allows the script to produce valid output at every stage of development, with validation tightening over time.

**ANY option:** Select questions can offer "ANY" as the first choice, which resolves to a random value from the remaining options. The resolved value is printed on the next line (`→ value`). Free-text questions (like age) use empty input to trigger the same behaviour. The `allow_any` flag on the `Question` base class controls whether a question supports this. The `Output` question does not offer ANY.

## Project structure

```
qcoccc.py                    — main entry point
character_sheet_builder.py   — assembles the character sheet dict from context
character_sheet.schema.json  — JSON Schema for the investigator sheet
requirements.txt
engine/
    question.py              — abstract Question base class (allow_any flag)
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

## Roadmap

Planned order of implementation:

1. **Full occupation list** — foundation for everything else; each occupation gets occupational skills and reasonable characteristic ranges (soft guidance, not hard rules — e.g. a soldier is unlikely to have very low STR)
2. **Characteristic rolling** — roll all 8 characteristics per the rules, apply occupation characteristic ranges and age modifiers, derive HP, MP, move rate, damage bonus, build, Luck and Sanity
3. **Occupational skill points** — allocate EDU × multiplier across the occupation's skills

Later:
- **Personal interest skill points** — allocate INT × 2 across a selectable list of interests/hobbies representing groups of skills
- **Specialization skills** — let the user pick which specialization for Fighting, Firearms, Science, Language, etc.
- **Full skill list** with base values for all skills
- **Pretty-print output** — human-readable character sheet to terminal, not just formatted JSON
- **Custom occupation** — allow the user to define an occupation not in the list

Out of scope: backstory generation, partial sheet saving/loading, re-rolling individual values.

## Question flow

1. **Era** — 1920s / Modern / Other
2. **Occupation** — loaded from era subfolder(s), sorted alphabetically
3. **Age bracket** — rulebook brackets: 15–19, 20s, 30s, 40s, 50s, 60s, 70s, 80s+
4. **Age** — free-text integer, validated against the chosen bracket
5. **Output** — To Terminal / To File / Both (no ANY)
