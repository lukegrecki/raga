from __future__ import annotations

import re
import time
from collections.abc import Callable
from pathlib import Path

SWARA_SEMITONES: dict[str, int] = {
    "Sa": 0,
    "komal Re": 1,
    "Re": 2,
    "komal Ga": 3,
    "Ga": 4,
    "Ma": 5,
    "tivra Ma": 6,
    "Pa": 7,
    "komal Dha": 8,
    "Dha": 9,
    "komal Ni": 10,
    "Ni": 11,
    "SA": 12,
}

_NOTE_NAMES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_NOTE_RE = re.compile(r"^([A-G])(#|b)?(-?\d+)$")


def parse_note_name(name: str) -> int:
    m = _NOTE_RE.match(name)
    if not m:
        raise ValueError(
            f"Invalid note name: {name!r}. Expected format like C4, D#3, Eb5."
        )
    letter, accidental, octave_str = m.groups()
    semitone = _NOTE_NAMES[letter]
    if accidental == "#":
        semitone += 1
    elif accidental == "b":
        semitone -= 1
    octave = int(octave_str)
    # MIDI: C4 = 60, so C-1 = 0
    midi_value = (octave + 1) * 12 + semitone
    if not 0 <= midi_value <= 127:
        raise ValueError(
            f"Note {name!r} produces MIDI value {midi_value}, "
            f"outside valid range 0–127."
        )
    return midi_value


def swaras_to_midi(swaras: list[str], sa_midi: int) -> list[int]:
    result = []
    for swara in swaras:
        if swara not in SWARA_SEMITONES:
            raise ValueError(
                f"Unknown swara: {swara!r}. Must be one of {list(SWARA_SEMITONES)}"
            )
        midi_value = sa_midi + SWARA_SEMITONES[swara]
        if not 0 <= midi_value <= 127:
            raise ValueError(
                f"Swara {swara!r} with sa_midi={sa_midi} produces MIDI value "
                f"{midi_value}, outside valid range 0–127."
            )
        result.append(midi_value)
    return result


def play_notes(
    midi_notes: list[int],
    tempo_bpm: int,
    soundfont_path: Path,
    gap_indices: list[int] | None = None,
    on_note: Callable[[int | None], None] | None = None,
) -> None:
    try:
        import fluidsynth  # type: ignore[import-untyped]
    except ImportError as e:
        raise ImportError(
            "Audio playback requires the 'audio' extra. "
            "Install it with: pip install raga[audio]\n"
            "You also need FluidSynth installed on your system:\n"
            "  macOS: brew install fluid-synth\n"
            "  Debian/Ubuntu: apt install fluidsynth\n"
            "Then download a SoundFont (e.g., FluidR3_GM.sf2) and run "
            "raga play with --soundfont /path/to/soundfont.sf2 "
            "or set RAGA_SOUNDFONT environment variable."
        ) from e

    if tempo_bpm <= 0:
        raise ValueError(f"tempo_bpm must be positive, got {tempo_bpm}")
    beat_duration = 60.0 / tempo_bpm
    gap_set = set(gap_indices) if gap_indices else set()

    fs = fluidsynth.Synth()
    try:
        try:
            fs.start(driver="coreaudio")
        except RuntimeError as e:
            raise RuntimeError(
                "Failed to start FluidSynth audio driver. "
                "Ensure FluidSynth is installed: `brew install fluid-synth` (macOS)"
            ) from e

        try:
            sfid = fs.sfload(str(soundfont_path))
            if sfid == -1:
                raise RuntimeError("Invalid soundfont ID returned")
        except (RuntimeError, FileNotFoundError) as e:
            raise RuntimeError(
                f"Failed to load soundfont: {soundfont_path}\n"
                f"Check that the file exists and is a valid SoundFont.\n"
                f"Or set RAGA_SOUNDFONT environment variable to a valid SoundFont path."
            ) from e

        try:
            fs.program_select(0, sfid, 0, 0)
        except RuntimeError as e:
            raise RuntimeError(
                "Failed to select soundfont program. "
                "The soundfont file may be corrupted or incompatible."
            ) from e

        for i, note in enumerate(midi_notes):
            if on_note is not None:
                on_note(i)
            fs.noteon(0, note, 100)
            time.sleep(beat_duration)
            fs.noteoff(0, note)
            if i in gap_set:
                time.sleep(beat_duration)

        if on_note is not None:
            on_note(None)
    finally:
        fs.delete()
