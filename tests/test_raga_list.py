from raga.models import Raga


def _make_raga(
    name: str = "Test",
    thaat: str = "Kalyan",
    arohana: list[str] | None = None,
    avarohana: list[str] | None = None,
    vadi: str = "Re",
    samvadi: str = "Pa",
    time: str = "evening",
    mood: list[str] | None = None,
    season: str | None = "spring",
) -> Raga:
    return Raga(
        name=name,
        thaat=thaat,
        arohana=arohana if arohana is not None else ["Sa", "Re"],
        avarohana=avarohana if avarohana is not None else ["Re", "Sa"],
        vadi=vadi,
        samvadi=samvadi,
        time=time,
        mood=mood if mood is not None else ["serene", "romantic"],
        season=season,
    )


def test_matches_no_filters():
    assert _make_raga().matches()


def test_matches_thaat_match():
    assert _make_raga(thaat="Kalyan").matches(thaat="Kalyan")


def test_matches_thaat_no_match():
    assert not _make_raga(thaat="Bhairav").matches(thaat="Kalyan")


def test_matches_thaat_case_insensitive():
    assert _make_raga(thaat="Kalyan").matches(thaat="kalyan")


def test_matches_time_match():
    assert _make_raga(time="evening").matches(time="evening")


def test_matches_time_no_match():
    assert not _make_raga(time="morning").matches(time="evening")


def test_matches_mood_match():
    assert _make_raga(mood=["serene", "romantic"]).matches(mood="romantic")


def test_matches_mood_no_match():
    assert not _make_raga(mood=["serene"]).matches(mood="devotional")


def test_matches_season_match():
    assert _make_raga(season="spring").matches(season="spring")


def test_matches_season_no_match():
    assert not _make_raga(season="winter").matches(season="spring")


def test_matches_season_none_no_match():
    assert not _make_raga(season=None).matches(season="spring")


def test_matches_include_any_time():
    assert _make_raga(time="any").matches(time="evening", include_any_time=True)
    assert not _make_raga(time="any").matches(time="evening", include_any_time=False)


def test_list_ragas_filter_thaat(ragas):
    kalyan_ragas = [r for r in ragas if r.matches(thaat="Kalyan")]
    assert len(kalyan_ragas) > 0
    assert all(r.thaat == "Kalyan" for r in kalyan_ragas)


def test_list_ragas_filter_time(ragas):
    evening_ragas = [r for r in ragas if r.matches(time="evening")]
    assert all(r.time == "evening" for r in evening_ragas)
