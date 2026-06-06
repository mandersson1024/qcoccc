# qcoccc
Quick Call of Cthulhu Character Creator

## Setup

Create and activate a virtual environment, then install dependencies:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The virtual environment only needs to be created once. On subsequent sessions, just activate it:

```
source .venv/bin/activate
```

## Run

```
python -m qcoccc
```

To pretty-print an existing character sheet JSON file:

```
python -m qcoccc -p character.json
```

## Example output

```
% python -m qcoccc
? Era 1920s
? Occupation ANY
  → Military Officer
? Age bracket ANY
  → 70s
? Age ANY
  → 78
? Firearms specialization ANY
  → Handgun
? Occupation skill 1 ANY
  → Persuade
? Occupation skill 2 ANY
  → Charm
? Survival specialization ANY
  → Arctic
? Any occupation skill 1 ANY
  → Science (Engineering)
? Personal interest 1 ANY
  → Climb
? Personal interest 2 ANY
  → Science (Astronomy)
? Personal interest 3 ANY
  → Throw
? Personal interest 4 ANY
  → Art/Craft (Carpentry)
? Skill distribution Generalist
  → Credit Rating          51
  → Accounting             16
  → Firearms (Handgun)     29
  → Navigate               21
  → Persuade               29
  → Charm                  23
  → Psychology             20
  → Survival (Arctic)      26
  → Science (Engineering)  15
  → Climb                  24
  → Science (Astronomy)    27
  → Throw                  34
  → Art/Craft (Carpentry)  35
? Output To Terminal
════════════════════════════════════════════════
  CALL OF CTHULHU INVESTIGATOR  ·  1920s
════════════════════════════════════════════════

  Military Officer  ·  Age 78

  CHARACTERISTICS ──────────────────────────────
  STR 52   CON 46   SIZ 85   DEX 37
  APP 10   INT 60   POW 60   EDU 63

  DERIVED ──────────────────────────────────────
  Hit Points    13     Sanity    60 / 99
  Magic Points  12     Luck      45
  Move Rate     3      Build     1
  Damage Bonus  +1D4

  SKILLS ───────────────────────────────────────
  Accounting .............................  21
  Art/Craft (Carpentry) ..................  40
  Charm ..................................  38
  Climb ..................................  44
  Credit Rating ..........................  51
  Firearms (Handgun) .....................  49
  Navigate ...............................  31
  Persuade ...............................  39
  Psychology .............................  30
  Science (Astronomy) ....................  28
  Science (Engineering) ..................  16
  Survival (Arctic) ......................  36
  Throw ..................................  54

════════════════════════════════════════════════
```
