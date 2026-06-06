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
  → Musician
? Age bracket ANY
  → 80s+
? Age ANY
  → 90
? Occupation skill 1 ANY
  → Persuade
? Any occupation skill 1 ANY
  → Fighting (Spear)
? Any occupation skill 2 ANY
  → Climb
? Any occupation skill 3 ANY
  → Sleight of Hand
? Any occupation skill 4 ANY
  → Intimidate
? Personal interest 1 ANY
  → Accounting
? Personal interest 2 ANY
  → Firearms (Heavy Weapons)
? Personal interest 3 ANY
  → Firearms (Machine Gun)
? Personal interest 4 ANY
  → Art/Craft (Pottery)
? Skill distribution Generalist
  → Credit Rating             23
  → Art/Craft (instrument)    23
  → Persuade                  28
  → Listen                    31
  → Psychology                32
  → Fighting (Spear)          29
  → Climb                     30
  → Sleight of Hand           29
  → Intimidate                41
  → Accounting                42
  → Firearms (Heavy Weapons)  32
  → Firearms (Machine Gun)    30
  → Art/Craft (Pottery)       26
? Output To Terminal
════════════════════════════════════════════════
  CALL OF CTHULHU INVESTIGATOR  ·  1920s
════════════════════════════════════════════════

  Musician  ·  Age 90

  CHARACTERISTICS ──────────────────────────────
  STR 28   CON 22   SIZ 70   DEX 20
  APP 35   INT 65   POW 60   EDU 73

  DERIVED ──────────────────────────────────────
  Hit Points    9      Sanity    60 / 99
  Magic Points  12     Luck      50
  Move Rate     2      Build     0
  Damage Bonus  None

  SKILLS ───────────────────────────────────────
  Accounting .............................  47
  Art/Craft (Pottery) ....................  31
  Art/Craft (instrument) .................  24
  Climb ..................................  50
  Credit Rating ..........................  23
  Fighting (Spear) .......................  49
  Firearms (Heavy Weapons) ...............  42
  Firearms (Machine Gun) .................  40
  Intimidate .............................  56
  Listen .................................  51
  Persuade ...............................  38
  Psychology .............................  42
  Sleight of Hand ........................  39

════════════════════════════════════════════════
```
