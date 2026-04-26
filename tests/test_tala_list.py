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
    assert _make_tala().matches()


def test_matches_beats_match():
    assert _make_tala(beats=16).matches(beats=16)


def test_matches_beats_no_match():
    assert not _make_tala(beats=10).matches(beats=16)


def test_matches_feel_match():
    assert _make_tala(feel=["stately"]).matches(feel="stately")


def test_matches_feel_no_match():
    assert not _make_tala(feel=["lively"]).matches(feel="stately")


def test_matches_feel_case_insensitive():
    assert _make_tala(feel=["Stately"]).matches(feel="stately")


def test_matches_tempo_match():
    assert _make_tala(tempo=["madhya"]).matches(tempo="madhya")


def test_matches_tempo_no_match():
    assert not _make_tala(tempo=["drut"]).matches(tempo="vilambit")


def test_list_talas_filter_beats(talas):
    filtered = [t for t in talas if t.matches(beats=16)]
    assert len(filtered) > 0
    assert all(t.beats == 16 for t in filtered)


def test_list_talas_filter_feel(talas):
    filtered = [t for t in talas if t.matches(feel="stately")]
    assert all("stately" in [f.lower() for f in t.feel] for t in filtered)
