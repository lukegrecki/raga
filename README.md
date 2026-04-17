# raga

A terminal reference tool for Hindustani classical music — look up ragas and talas, browse by time, mood, or feel, and get suggestions suited to the moment.

## Installation

```bash
pip install -e .          # install CLI commands
pip install -e ".[dev]"   # also installs pytest
```

Requires Python 3.11+.

## Commands

### raga

```bash
raga lookup <name>              # look up a raga by name (fuzzy match)
raga list                       # list all ragas
raga list --thaat Kalyan        # filter by thaat
raga list --time evening        # filter by time of day
raga list --mood devotional
raga list --season spring

raga suggest                    # suggest ragas for the current time of day
raga suggest --time morning     # suggest for a specific time
raga suggest --mood romantic    # suggest by mood
raga suggest --time dusk --mood solemn --count 5
```

### tala

```bash
tala lookup <name>              # look up a tala by name (fuzzy match)
tala list                       # list all talas
tala list --beats 16            # filter by beat count
tala list --feel stately        # filter by feel
tala list --tempo vilambit      # filter by tempo

tala suggest                    # suggest talas from the full collection
tala suggest --beats 16         # suggest talas with a specific beat count
tala suggest --feel lively      # suggest by feel
tala suggest --tempo drut --count 2
```

## Reference

### Raga time values

`dawn` · `morning` · `afternoon` · `evening` · `dusk` · `night` · `late night` · `midnight` · `any`

`raga suggest` defaults to the current time of day when called with no arguments.

### Swara notation

Swaras are displayed with color: komal (flat) notes in yellow, tivra (sharp) Ma in magenta. Upper-octave SA is bold.

### Tala theka notation

Bols prefixed with `~` are khali (unaccented) beats, rendered dim and italic.

## Data

Ragas and talas are stored as JSON in `src/raga/data/`. To add entries, edit `ragas.json` or `talas.json` directly — no code changes needed.

## Development

```bash
python -m pytest tests/ -v
```
