# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pip install -e .          # install in editable mode (run once after cloning)

raga lookup <name>        # look up a raga by name (fuzzy match)
raga list                 # list all ragas
raga list --thaat Kalyan  # filter by thaat
raga list --time evening  # filter by time of day
raga list --mood devotional
```

## Architecture

`src/raga/` is a single Python package installed as the `raga` CLI command.

- **`cli.py`** — Typer app; registers `lookup` and `list` as subcommands
- **`models.py`** — Pydantic `Raga` model + `load_ragas()` (cached, reads `data/ragas.json`)
- **`display.py`** — Rich text helpers: `format_swara()` colorizes komal (yellow) / tivra (magenta) swaras; `format_scale()` renders a full arohana/avarohana list
- **`commands/lookup.py`** — fuzzy raga search via `rapidfuzz`, renders a Rich `Panel`
- **`commands/list_ragas.py`** — filterable Rich `Table` of all ragas
- **`data/ragas.json`** — static raga data; add new ragas here

## Swara notation in ragas.json

Swaras are stored as plain strings: `"Sa"`, `"Re"`, `"komal Re"`, `"Ga"`, `"komal Ga"`, `"Ma"`, `"tivra Ma"`, `"Pa"`, `"Dha"`, `"komal Dha"`, `"Ni"`, `"komal Ni"`, `"SA"` (upper octave).

`display.py` maps these to colored Rich text at render time — do not use other conventions.

## Time values

Valid values for the `time` field: `dawn`, `morning`, `afternoon`, `evening`, `dusk`, `night`, `late night`, `midnight`, `any`.
