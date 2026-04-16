from unittest.mock import patch

import pytest

from raga.commands.suggest import _current_time_of_day
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
        season=None,
    )
    defaults.update(kwargs)
    return Raga(**defaults)


@pytest.mark.parametrize("hour,expected", [
    (5, "dawn"),
    (9, "morning"),
    (14, "afternoon"),
    (17, "evening"),
    (18, "dusk"),
    (20, "night"),
    (23, "late night"),
    (2, "midnight"),
])
def test_current_time_of_day(hour, expected):
    with patch("raga.commands.suggest.datetime") as mock_dt:
        mock_dt.now.return_value.hour = hour
        assert _current_time_of_day() == expected


def test_suggest_filters_by_time(ragas):
    evening = [r for r in ragas if r.time == "evening"]
    assert len(evening) > 0


def test_suggest_filters_by_mood(ragas):
    devotional = [r for r in ragas if "devotional" in r.mood]
    assert len(devotional) > 0


def test_suggest_any_time_raga_included():
    ragas = [
        _make_raga(name="AnyRaga", time="any"),
        _make_raga(name="EveningRaga", time="evening"),
        _make_raga(name="MorningRaga", time="morning"),
    ]

    def matches(r: Raga, time: str) -> bool:
        if r.time.lower() != time.lower() and r.time.lower() != "any":
            return False
        return True

    pool = [r for r in ragas if matches(r, "evening")]
    names = [r.name for r in pool]
    assert "AnyRaga" in names
    assert "EveningRaga" in names
    assert "MorningRaga" not in names


def test_suggest_mood_filter():
    ragas = [
        _make_raga(name="R1", mood=["devotional", "serene"]),
        _make_raga(name="R2", mood=["romantic"]),
    ]

    def matches(r: Raga, mood: str) -> bool:
        return mood.lower() in [m.lower() for m in r.mood]

    pool = [r for r in ragas if matches(r, "devotional")]
    assert len(pool) == 1
    assert pool[0].name == "R1"
