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
        vibhags=vibhags if vibhags is not None else [4, 4, 4, 4],
        theka=theka if theka is not None else ["Dha"] * 16,
        feel=feel if feel is not None else ["stately", "versatile"],
        tempo=tempo if tempo is not None else ["madhya", "vilambit"],
    )


def _matches(t: Tala, beats, feel, tempo) -> bool:
    if beats is not None and t.beats != beats:
        return False
    if feel and feel.lower() not in [f.lower() for f in t.feel]:
        return False
    if tempo and tempo.lower() not in [t2.lower() for t2 in t.tempo]:
        return False
    return True


def test_matches_no_filters():
    assert _matches(_make_tala(), None, None, None)


def test_matches_beats_match():
    assert _matches(_make_tala(beats=16), 16, None, None)


def test_matches_beats_no_match():
    assert not _matches(_make_tala(beats=16), 8, None, None)


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


def test_matches_combined_filters():
    t = _make_tala(beats=16, feel=["stately"], tempo=["vilambit"])
    assert _matches(t, 16, "stately", "vilambit")
    assert not _matches(t, 16, "lively", "vilambit")


def test_suggest_filters_by_beats(talas):
    pool = [t for t in talas if t.beats == 16]
    assert len(pool) > 0
    assert all(t.beats == 16 for t in pool)


def test_suggest_filters_by_feel(talas):
    pool = [t for t in talas if "lively" in [f.lower() for f in t.feel]]
    assert len(pool) > 0


def test_suggest_all_talas_no_filters(talas):
    pool = [t for t in talas if _matches(t, None, None, None)]
    assert len(pool) == len(talas)
