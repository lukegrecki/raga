from raga.commands.list_talas import _matches
from raga.models import Tala


def _make_tala(
    name: str = "Test",
    beats: int = 16,
    vibhags: list[int] | None = None,
    theka: list[str] | None = None,
    feel: list[str] | None = None,
    tempo: list[str] | None = None,
) -> Tala:
    return Tala(
        name=name,
        beats=beats,
        vibhags=vibhags if vibhags is not None else [beats],
        theka=theka if theka is not None else ["Dha"] * beats,
        feel=feel if feel is not None else ["stately", "versatile"],
        tempo=tempo if tempo is not None else ["vilambit", "madhya"],
    )


def test_matches_no_filters():
    assert _matches(_make_tala(), None, None, None)


def test_matches_beats_match():
    assert _matches(_make_tala(beats=16), 16, None, None)


def test_matches_beats_no_match():
    assert not _matches(_make_tala(beats=10), 16, None, None)


def test_matches_feel_match():
    assert _matches(_make_tala(feel=["stately"]), None, "stately", None)


def test_matches_feel_no_match():
    assert not _matches(_make_tala(feel=["lively"]), None, "stately", None)


def test_matches_feel_case_insensitive():
    assert _matches(_make_tala(feel=["Stately"]), None, "stately", None)


def test_matches_tempo_match():
    assert _matches(_make_tala(tempo=["madhya"]), None, None, "madhya")


def test_matches_tempo_no_match():
    assert not _matches(_make_tala(tempo=["drut"]), None, None, "vilambit")


def test_list_talas_filter_beats(talas):
    filtered = [t for t in talas if _matches(t, 16, None, None)]
    assert len(filtered) > 0
    assert all(t.beats == 16 for t in filtered)


def test_list_talas_filter_feel(talas):
    filtered = [t for t in talas if _matches(t, None, "stately", None)]
    assert all("stately" in [f.lower() for f in t.feel] for t in filtered)
