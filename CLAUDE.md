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

## Design decisions

**Era-specific skills:** The schema defines all skills as a superset across all eras. Era logic (which skills are available) lives in the Python script. The schema includes an `era` field to record which era the character belongs to, since investigator sheets differ between eras.

## What exists so far

- `qcoccc.py` — main entry point
- `character_sheet.schema.json` — JSON Schema defining the investigator sheet format
