# Contributing to raga

Thanks for your interest in contributing! This guide covers the most common contribution tasks.

## Adding a raga

Ragas are stored in `src/raga/data/ragas.json`. To add a new raga:

1. Open `src/raga/data/ragas.json`
2. Add a new object with these required fields:
   - `name` (string): The raga's name
   - `thaat` (string, optional): The parent thaat (e.g. "Kalyan", "Bhairav")
   - `arohana` (list of strings): The ascending scale
   - `avarohana` (list of strings): The descending scale
   - `vadi` (string): The primary swara (important pitch)
   - `samvadi` (string): The secondary swara
   - `time` (string): When the raga is traditionally played (e.g. "morning", "evening", "any")

3. Optional fields:
   - `aliases` (list of strings): Alternative names
   - `mood` (list of strings): Emotional qualities (e.g. "devotional", "romantic", "energetic")
   - `season` (string): When traditionally played in the year (e.g. "spring", "winter")
   - `pakad` (string): A characteristic phrase or melodic pattern
   - `description` (string): Free-form notes

### Swara notation

Use the conventions documented in CLAUDE.md:
- Natural swaras: `"Sa"`, `"Re"`, `"Ga"`, `"Ma"`, `"Pa"`, `"Dha"`, `"Ni"`, `"SA"` (octave)
- Komal (flat): `"komal Re"`, `"komal Ga"`, etc.
- Tivra (sharp): `"tivra Ma"` (and others as needed)

Example:
```json
{
  "name": "Bhairav",
  "thaat": "Bhairav",
  "arohana": ["Sa", "komal Re", "Ga", "Ma", "Pa", "komal Dha", "Ni", "SA"],
  "avarohana": ["SA", "Ni", "komal Dha", "Pa", "Ma", "Ga", "komal Re", "Sa"],
  "vadi": "Ma",
  "samvadi": "Sa",
  "time": "dawn",
  "mood": ["devotional", "mystical"],
  "season": "winter"
}
```

## Adding a tala

Talas are stored in `src/raga/data/talas.json`. To add a new tala:

1. Open `src/raga/data/talas.json`
2. Add a new object with these required fields:
   - `name` (string): The tala's name
   - `beats` (integer): Total number of beats
   - `vibhags` (list of integers): Beat groupings (must sum to `beats`)
   - `theka` (list of strings): The bol sequence (must have `beats` elements)
   - `tempo` (list of strings): Applicable tempos ("vilambit", "madhya", "drut")

3. Optional fields:
   - `aliases` (list of strings): Alternative names
   - `feel` (list of strings): Descriptive qualities (e.g. "stately", "lively", "versatile")
   - `description` (string): Free-form notes

### Tala constraints

The following invariant must hold: `beats == len(theka) == sum(vibhags)`

Use `~` prefix in the theka to mark khali (unaccented) beats:
```json
{
  "name": "Teentaal",
  "beats": 16,
  "vibhags": [4, 4, 4, 4],
  "theka": ["dha", "dhin", "dhin", "dha", "dha", "dhin", "dhin", "dha", "dha", "dhin", "dhin", "dha", "~", "dhin", "dhin", "dha"],
  "tempo": ["madhya", "drut"],
  "feel": ["versatile", "common"]
}
```

## Running tests

Run the test suite to ensure your changes don't break anything:

```bash
pip install -e ".[dev]"
.venv/bin/python -m pytest tests/ -v
```

## Running the linter

Keep code style consistent:

```bash
.venv/bin/python -m ruff check src/ tests/
```

Fix issues automatically with:

```bash
.venv/bin/python -m ruff check --fix src/ tests/
```

## Development install

To set up a development environment:

```bash
pip install -e ".[dev]"
```

This installs the package in editable mode with development dependencies (pytest, ruff).

## Testing changes

After editing data files, test your changes:

```bash
raga lookup YourNewRaga
raga list
tala lookup YourNewTala
tala list
```

Use `--help` to verify that all commands and options display correctly.
