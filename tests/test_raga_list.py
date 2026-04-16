from raga.commands.list_ragas import _matches
from raga.models import Raga


def _make_raga(**kwargs) -> Raga:
    defaults = dict(
        name="Test",
        thaat="Kalyan",
        arohana=["Sa", "Re"],
        avarohana=["Re", "Sa"],
        vadi="Re",
        samvadi="Pa",
        time="evening",
        mood=["serene", "romantic"],
        season="spring",
    )
    defaults.update(kwargs)
    return Raga(**defaults)


def test_matches_no_filters():
    assert _matches(_make_raga(), None, None, None, None)


def test_matches_thaat_match():
    assert _matches(_make_raga(thaat="Kalyan"), "Kalyan", None, None, None)


def test_matches_thaat_no_match():
    assert not _matches(_make_raga(thaat="Bhairav"), "Kalyan", None, None, None)


def test_matches_thaat_case_insensitive():
    assert _matches(_make_raga(thaat="Kalyan"), "kalyan", None, None, None)


def test_matches_time_match():
    assert _matches(_make_raga(time="evening"), None, "evening", None, None)


def test_matches_time_no_match():
    assert not _matches(_make_raga(time="morning"), None, "evening", None, None)


def test_matches_mood_match():
    assert _matches(_make_raga(mood=["serene", "romantic"]), None, None, "romantic", None)


def test_matches_mood_no_match():
    assert not _matches(_make_raga(mood=["serene"]), None, None, "devotional", None)


def test_matches_season_match():
    assert _matches(_make_raga(season="spring"), None, None, None, "spring")


def test_matches_season_no_match():
    assert not _matches(_make_raga(season="winter"), None, None, None, "spring")


def test_matches_season_none_no_match():
    assert not _matches(_make_raga(season=None), None, None, None, "spring")


def test_list_ragas_filter_thaat(ragas):
    from raga.commands.list_ragas import _matches as m
    kalyan_ragas = [r for r in ragas if m(r, "Kalyan", None, None, None)]
    assert len(kalyan_ragas) > 0
    assert all(r.thaat == "Kalyan" for r in kalyan_ragas)


def test_list_ragas_filter_time(ragas):
    from raga.commands.list_ragas import _matches as m
    evening_ragas = [r for r in ragas if m(r, None, "evening", None, None)]
    assert all(r.time == "evening" for r in evening_ragas)
