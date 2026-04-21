# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pip install -e .              # install in editable mode (run once after cloning)
pip install -e ".[dev]"       # also installs pytest

raga lookup <name>            # look up a raga by name (fuzzy match)
raga list                     # list all ragas
raga list --thaat Kalyan      # filter by thaat
raga list --time evening      # filter by time of day
raga list --mood devotional
raga list --season spring

raga play <name>              # play arohana+avarohana via FluidSynth
raga play <name> --sa D4      # set Sa reference (default: C4)
raga play <name> --tempo 60   # set tempo in BPM (default: 80)
raga play <name> --soundfont /path/to/FluidR3_GM.sf2

tala lookup <name>            # look up a tala by name (fuzzy match)
tala list                     # list all talas
tala list --beats 16          # filter by beat count
tala list --feel stately      # filter by feel
tala list --tempo vilambit    # filter by tempo

python -m pytest tests/ -v    # run all tests
```

## Architecture

`src/raga/` is a single Python package installed as two CLI commands: `raga` and `tala`.

- **`cli.py`** — Typer app for `raga`; registers `lookup` and `list` as subcommands
- **`tala_cli.py`** — Typer app for `tala`; registers `lookup` and `list` as subcommands
- **`models.py`** — Pydantic `Raga` and `Tala` models + `load_ragas()` / `load_talas()` (cached, read from `data/`)
- **`display.py`** — Rich text helpers: `format_swara()` colorizes komal (yellow) / tivra (magenta) swaras; `format_scale()` renders a full arohana/avarohana list; `format_theka()` renders a tala's bol sequence grouped by vibhag
- **`commands/lookup.py`** — fuzzy raga search via `rapidfuzz`, renders a Rich `Panel`
- **`commands/list_ragas.py`** — filterable Rich `Table` of all ragas
- **`commands/lookup_tala.py`** — fuzzy tala search via `rapidfuzz`, renders a Rich `Panel`
- **`commands/list_talas.py`** — filterable Rich `Table` of all talas
- **`data/ragas.json`** — static raga data; add new ragas here
- **`data/talas.json`** — static tala data; add new talas here

## Swara notation in ragas.json

Swaras are stored as plain strings: `"Sa"`, `"Re"`, `"komal Re"`, `"Ga"`, `"komal Ga"`, `"Ma"`, `"tivra Ma"`, `"Pa"`, `"Dha"`, `"komal Dha"`, `"Ni"`, `"komal Ni"`, `"SA"` (upper octave).

`display.py` maps these to colored Rich text at render time — do not use other conventions.

## Tala fields in talas.json

- **`beats`** — total beat count; must equal `len(theka)` and `sum(vibhags)`
- **`vibhags`** — list of ints grouping beats into sections (e.g. `[4,4,4,4]` for Teentaal)
- **`theka`** — list of bol strings; prefix with `~` for khali (unaccented) beats (rendered dim/italic)
- **`feel`** — descriptive feel tags (e.g. `stately`, `lively`, `versatile`)
- **`tempo`** — valid values: `vilambit`, `madhya`, `drut`

## Time values

Valid values for the `time` field: `dawn`, `morning`, `afternoon`, `evening`, `dusk`, `night`, `late night`, `midnight`, `any`.

## Audio playback

`raga play` requires FluidSynth and a SoundFont file:

```bash
brew install fluid-synth          # macOS
pip install pyfluidsynth          # Python binding (already in dependencies)
```

Specify the SoundFont via `--soundfont /path/to/FluidR3_GM.sf2` or set the `RAGA_SOUNDFONT` env var. A free GM SoundFont (e.g. FluidR3_GM.sf2) can be downloaded from the FluidSynth project or MuseScore.
