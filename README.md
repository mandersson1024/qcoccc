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
  → Journalist
? Age bracket ANY
  → 50s
? Age ANY
  → 59
? Skill choice 1 ANY
  → Charm
? Free skill choice 1 ANY
  → Operate Heavy Machinery
? Free skill choice 2 ANY
  → Law
? Skill distribution Generalist
? Output To Terminal
Personal interest skills:
  → Appraise
  → Science (Physics)
  → Pilot (Boat)
  → Art/Craft (Dancing)
════════════════════════════════════════════════
  CALL OF CTHULHU INVESTIGATOR  ·  1920s
════════════════════════════════════════════════

  Journalist  ·  Age 59

  CHARACTERISTICS ──────────────────────────────
  STR 40   CON 49   SIZ 70   DEX 26
  APP 45   INT 85   POW 55   EDU 61

  DERIVED ──────────────────────────────────────
  Hit Points    11     Sanity    55 / 99
  Magic Points  11     Luck      60
  Move Rate     5      Build     0
  Damage Bonus  None

  SKILLS ───────────────────────────────────────
  Appraise ...............................  47
  Art/Craft (Dancing) ....................  51
  Art/Craft (Photography) ................  41
  Charm ..................................  40
  Credit Rating ..........................  27
  History ................................  36
  Law ....................................  32
  Library Use ............................  42
  Operate Heavy Machinery ................  28
  Own Language ...........................  75
  Pilot (Boat) ...........................  43
  Psychology .............................  45
  Science (Physics) ......................  41

════════════════════════════════════════════════
```
