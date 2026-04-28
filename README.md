# raga

[![PyPI version](https://img.shields.io/pypi/v/ragamala)](https://pypi.org/project/ragamala/)
[![Python versions](https://img.shields.io/pypi/pyversions/ragamala)](https://pypi.org/project/ragamala/)
[![License](https://img.shields.io/pypi/l/ragamala)](https://github.com/lukegrecki/raga/blob/main/LICENSE)
[![CI](https://github.com/lukegrecki/raga/actions/workflows/test.yml/badge.svg)](https://github.com/lukegrecki/raga/actions)

A terminal reference tool for Hindustani classical music — look up ragas and talas, browse by time, mood, or feel, and get suggestions suited to the moment.

## What is this?

Ragas and talas are the melodic and rhythmic foundations of Hindustani classical music. This tool helps you explore them: look up detailed information about any raga or tala, discover which ones suit a particular time of day or mood, and listen to audio previews. Whether you're a student learning Indian classical music, a listener discovering new ragas, or a musician planning your practice, this reference tool gives you quick access to the essential details.

## Demo

Try `raga suggest` to get ragas suited to the current time of day:

```
$ raga suggest
Suggesting 3 raga(s) for afternoon

╭─────────────────────── Madhuvanti ─────────────────────╮
│  Thaat           Todi                                  │
│  Time            Afternoon                             │
│  Mood            sweet, yearning, romantic             │
│  Arohana         Sa Re Ga Ma♯ Pa Ni SA                 │
│  Avarohana       SA Ni Dha Pa Ma♯ Ga Re Sa             │
│                                                        │
│  A relatively modern raga... [description continues]  │
╰────────────────────────────────────────────────────────╯
```

Or look up a specific raga with colored notation and detailed analysis:

```
$ raga lookup yaman

╭─────────────────── Yaman ─────────────────────────────╮
│  Thaat           Kalyan                                │
│  Time            Evening                               │
│  Vadi / Samvadi  Ga / Ni                               │
│  Mood            serene, romantic, devotional          │
│  Arohana         Sa Re Ga Ma♯ Pa Dha Ni SA             │
│  Avarohana       SA Ni Dha Pa Ma♯ Ga Re Sa             │
│                                                        │
│  One of the most foundational and widely taught       │
│  ragas... [description continues]                     │
╰────────────────────────────────────────────────────────╯
```

## Installation

```bash
pip install ragamala
```

Requires Python 3.11 or later.

## Quick Start

```bash
raga suggest                  # suggest ragas for the current time
raga lookup yaman             # detailed view of one raga
raga list --mood devotional   # filter by mood

tala lookup teentaal          # look up a tala by name
tala list --beats 16          # filter by beat count
```

## Optional: Audio Playback

The `raga play` command requires FluidSynth and a SoundFont file. The `lookup`, `list`, and `suggest` commands work without audio.

### Install FluidSynth

```bash
# macOS
brew install fluid-synth

# Debian/Ubuntu
apt install fluidsynth

# Windows
# Download from https://github.com/FluidSynth/fluidsynth/releases
```

### Install the audio extra

```bash
pip install ragamala[audio]
```

### Get a SoundFont

Download a free SoundFont file (e.g., `FluidR3_GM.sf2`) from the [FluidSynth project](https://github.com/FluidSynth/fluidsynth/wiki/SoundFont) or [MuseScore](https://musescore.org/en/handbook/3/soundfonts-and-sfz-files). Then pass it to `raga play`:

```bash
raga play yaman --soundfont /path/to/FluidR3_GM.sf2
```

Or set the `RAGA_SOUNDFONT` environment variable once:

```bash
export RAGA_SOUNDFONT=/path/to/FluidR3_GM.sf2
raga play yaman   # uses the env var
```

## Commands

### raga

```bash
raga lookup <name>              # look up a raga by name (fuzzy match)
raga list                       # list all ragas
raga list --thaat Kalyan        # filter by thaat
raga list --time evening        # filter by time of day
raga list --mood devotional
raga list --season spring
raga list --plain               # plain text output (no color, pipe-friendly)
raga list --output ragas.txt    # write plain text to a file

raga suggest                    # suggest ragas for the current time of day
raga suggest --time morning     # suggest for a specific time
raga suggest --mood romantic    # suggest by mood
raga suggest --time dusk --mood solemn --count 5

raga play <name>                # play arohana+avarohana via FluidSynth
raga play <name> --sa D4        # set Sa reference pitch (default: C4)
raga play <name> --tempo 60     # set tempo in BPM (default: 80)
raga play <name> --soundfont /path/to/FluidR3_GM.sf2
```

### tala

```bash
tala lookup <name>              # look up a tala by name (fuzzy match)
tala list                       # list all talas
tala list --beats 16            # filter by beat count
tala list --feel stately        # filter by feel
tala list --tempo vilambit      # filter by tempo
tala list --plain               # plain text output (no color, pipe-friendly)
tala list --output talas.txt    # write plain text to a file

tala suggest                    # suggest talas from the full collection
tala suggest --beats 16         # suggest talas with a specific beat count
tala suggest --feel lively      # suggest by feel
tala suggest --tempo drut --count 2
```

### Shell completions

Both `raga` and `tala` support tab completion for all options and their values (raga names, thaats, times, moods, seasons, feels, tempos, beat counts).

```bash
raga --install-completion       # install completion for your current shell
tala --install-completion

raga --show-completion          # print the completion script (for manual setup)
tala --show-completion
```

Supported shells: bash, zsh, fish, PowerShell.

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

To contribute, first install in development mode:

```bash
pip install -e ".[dev]"
```

Then run tests:

```bash
python -m pytest tests/ -v
```
