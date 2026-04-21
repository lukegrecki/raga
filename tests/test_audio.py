import json
from pathlib import Path

import pytest

from raga.audio import SWARA_SEMITONES, parse_note_name, swaras_to_midi

# --- parse_note_name ---

def test_parse_c4():
    assert parse_note_name("C4") == 60


def test_parse_a4():
    assert parse_note_name("A4") == 69


def test_parse_dsharp4():
    assert parse_note_name("D#4") == 63


def test_parse_eflat4():
    assert parse_note_name("Eb4") == 63


def test_parse_bad_input_raises():
    with pytest.raises(ValueError):
        parse_note_name("not-a-note")


def test_parse_missing_octave_raises():
    with pytest.raises(ValueError):
        parse_note_name("C")


# --- swaras_to_midi ---

def test_swaras_basic():
    assert swaras_to_midi(["Sa", "Re", "Ga"], 60) == [60, 62, 64]


def test_swaras_komal():
    assert swaras_to_midi(["komal Re", "komal Ga"], 60) == [61, 63]


def test_swaras_tivra():
    assert swaras_to_midi(["tivra Ma"], 60) == [66]


def test_swaras_sa_offset():
    # sa_midi=62 (D4)
    assert swaras_to_midi(["Sa", "Pa"], 62) == [62, 69]


def test_swaras_unknown_raises():
    with pytest.raises(ValueError, match="Unknown swara"):
        swaras_to_midi(["Xyz"], 60)


# --- SWARA_SEMITONES coverage ---

def test_all_ragas_json_swaras_in_map():
    data_path = Path(__file__).parent.parent / "src" / "raga" / "data" / "ragas.json"
    data = json.loads(data_path.read_text())
    unique_swaras = {
        swara
        for raga in data
        for field in ("arohana", "avarohana")
        for swara in raga[field]
    }
    missing = unique_swaras - SWARA_SEMITONES.keys()
    assert not missing, f"Swaras missing from SWARA_SEMITONES: {missing}"
