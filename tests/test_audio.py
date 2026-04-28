import json
from pathlib import Path
from unittest.mock import MagicMock, patch

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


def test_parse_lowercase_letter_raises():
    """Lowercase note letters fail the regex"""
    with pytest.raises(ValueError, match="Invalid note name"):
        parse_note_name("c4")


def test_parse_double_accidental_raises():
    """Double accidentals fail the regex"""
    with pytest.raises(ValueError, match="Invalid note name"):
        parse_note_name("C##4")


def test_parse_invalid_letter_raises():
    """Invalid note letter (e.g. H) fails the regex"""
    with pytest.raises(ValueError, match="Invalid note name"):
        parse_note_name("H4")


def test_parse_out_of_range_low():
    """Note producing MIDI < 0 raises"""
    with pytest.raises(ValueError, match="outside valid range 0–127"):
        parse_note_name("C-2")  # Would be MIDI -12


def test_parse_out_of_range_high():
    """Note producing MIDI > 127 raises"""
    with pytest.raises(ValueError, match="outside valid range 0–127"):
        parse_note_name("G#9")  # Would be MIDI 128


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


def test_swaras_case_sensitive():
    """Swara names are case-sensitive; "sa" != "Sa" """
    with pytest.raises(ValueError, match="Unknown swara"):
        swaras_to_midi(["sa"], 60)


def test_swaras_empty_list():
    """Empty list of swaras returns empty list"""
    assert swaras_to_midi([], 60) == []


def test_swaras_sa_pushes_past_127_raises():
    """When sa_midi + swara exceeds 127, raise ValueError"""
    with pytest.raises(ValueError, match="outside valid range"):
        swaras_to_midi(["Sa", "Re"], 126)  # Re would be 128


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


# --- play_notes error handling ---

def test_play_notes_driver_error_wrapped(tmp_path):
    """Driver RuntimeError is wrapped with install hint"""
    import sys

    from raga.audio import play_notes

    mock_sf = tmp_path / "test.sf2"
    mock_sf.write_text("fake")

    mock_synth = MagicMock()
    mock_synth.start.side_effect = RuntimeError("some driver error")

    mock_fluidsynth = MagicMock()
    mock_fluidsynth.Synth.return_value = mock_synth

    with patch.dict(sys.modules, {"fluidsynth": mock_fluidsynth}):
        with pytest.raises(RuntimeError, match="FluidSynth is installed"):
            play_notes([60], 80, mock_sf)


def test_play_notes_soundfont_not_found(tmp_path):
    """Invalid soundfont path raises with guidance"""
    import sys

    from raga.audio import play_notes

    mock_sf = tmp_path / "test.sf2"
    mock_sf.write_text("fake")

    mock_synth = MagicMock()
    mock_synth.sfload.side_effect = FileNotFoundError("SoundFont not found")

    mock_fluidsynth = MagicMock()
    mock_fluidsynth.Synth.return_value = mock_synth

    with patch.dict(sys.modules, {"fluidsynth": mock_fluidsynth}):
        with pytest.raises(RuntimeError, match="Failed to load soundfont"):
            play_notes([60], 80, mock_sf)


def test_play_notes_sfload_returns_minus_one(tmp_path):
    """sfload returning -1 raises RuntimeError"""
    import sys

    from raga.audio import play_notes

    mock_sf = tmp_path / "test.sf2"
    mock_sf.write_text("fake")

    mock_synth = MagicMock()
    mock_synth.sfload.return_value = -1

    mock_fluidsynth = MagicMock()
    mock_fluidsynth.Synth.return_value = mock_synth

    with patch.dict(sys.modules, {"fluidsynth": mock_fluidsynth}):
        with pytest.raises(RuntimeError, match="Failed to load soundfont"):
            play_notes([60], 80, mock_sf)


def test_play_notes_cleanup_on_error(tmp_path):
    """fs.delete() runs even when an exception is raised (finally block)"""
    import sys

    from raga.audio import play_notes

    mock_sf = tmp_path / "test.sf2"
    mock_sf.write_text("fake")

    mock_synth = MagicMock()
    mock_synth.sfload.return_value = 0
    mock_synth.noteon.side_effect = RuntimeError("playback error")

    mock_fluidsynth = MagicMock()
    mock_fluidsynth.Synth.return_value = mock_synth

    with patch.dict(sys.modules, {"fluidsynth": mock_fluidsynth}):
        with pytest.raises(RuntimeError, match="playback error"):
            play_notes([60], 80, mock_sf)
        # delete should have been called even though an error occurred
        mock_synth.delete.assert_called_once()


def test_play_notes_tempo_zero_raises(tmp_path):
    """tempo_bpm = 0 raises ValueError"""
    from raga.audio import play_notes

    mock_sf = tmp_path / "test.sf2"
    mock_sf.write_text("fake")

    with pytest.raises(ValueError, match="tempo"):
        play_notes([60], 0, mock_sf)


def test_play_notes_tempo_negative_raises(tmp_path):
    """tempo_bpm < 0 raises ValueError"""
    from raga.audio import play_notes

    mock_sf = tmp_path / "test.sf2"
    mock_sf.write_text("fake")

    with pytest.raises(ValueError, match="tempo"):
        play_notes([60], -80, mock_sf)
