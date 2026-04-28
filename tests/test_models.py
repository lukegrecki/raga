import pytest

from raga.audio import SWARA_SEMITONES
from raga.models import VALID_TEMPOS, VALID_TIMES, Raga, Tala, load_ragas, load_talas


def test_load_ragas_nonempty(ragas):
    assert len(ragas) > 0


def test_load_talas_nonempty(talas):
    assert len(talas) > 0


def test_ragas_are_raga_instances(ragas):
    assert all(isinstance(r, Raga) for r in ragas)


def test_talas_are_tala_instances(talas):
    assert all(isinstance(t, Tala) for t in talas)


def test_raga_required_fields(ragas):
    for r in ragas:
        assert r.name
        assert r.arohana
        assert r.avarohana
        assert r.vadi
        assert r.samvadi
        assert r.time


def test_load_ragas_is_cached():
    assert load_ragas() is load_ragas()


def test_load_talas_is_cached():
    assert load_talas() is load_talas()


# --- Tala validation ---

def test_tala_theka_length_mismatch_raises():
    """theka length must match beats"""
    with pytest.raises(ValueError, match="theka has 4 bols but beats=5"):
        Tala(
            name="BadTala",
            beats=5,
            vibhags=[5],
            theka=["Dha", "Dha", "Jha", "Nu"],
        )


def test_tala_vibhags_sum_mismatch_raises():
    """vibhags sum must match beats"""
    with pytest.raises(ValueError, match="vibhags sum to 3 but beats=4"):
        Tala(
            name="BadTala",
            beats=4,
            vibhags=[2, 1],
            theka=["Dha", "Dha", "Jha", "Nu"],
        )


def test_tala_valid_structure():
    """Valid Tala with matching beats, vibhags, and theka"""
    tala = Tala(
        name="TestTala",
        beats=4,
        vibhags=[2, 2],
        theka=["Dha", "Dha", "Jha", "Nu"],
    )
    assert tala.name == "TestTala"
    assert tala.beats == 4
    assert len(tala.theka) == 4
    assert sum(tala.vibhags) == 4


# --- Data integrity ---

def test_raga_vadi_is_valid_swara(ragas):
    """Every raga's vadi must be a known swara"""
    for raga in ragas:
        assert raga.vadi in SWARA_SEMITONES, (
            f"Raga '{raga.name}' has invalid vadi '{raga.vadi}'"
        )


def test_raga_samvadi_is_valid_swara(ragas):
    """Every raga's samvadi must be a known swara"""
    for raga in ragas:
        assert raga.samvadi in SWARA_SEMITONES, (
            f"Raga '{raga.name}' has invalid samvadi '{raga.samvadi}'"
        )


def test_raga_time_is_valid(ragas):
    """Every raga's time must be in the documented set"""
    for raga in ragas:
        assert raga.time in VALID_TIMES, (
            f"Raga '{raga.name}' has invalid time '{raga.time}'"
        )


def test_tala_tempo_values_are_valid(talas):
    """Every tala's tempo values must be in {vilambit, madhya, drut}"""
    for tala in talas:
        for tempo in tala.tempo:
            assert tempo.lower() in VALID_TEMPOS, (
                f"Tala '{tala.name}' has invalid tempo '{tempo}'"
            )
