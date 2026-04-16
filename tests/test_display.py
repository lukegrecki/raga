from rich.text import Text

from raga.display import format_scale, format_swara, format_theka, time_label


def test_format_swara_plain():
    t = format_swara("Pa")
    assert isinstance(t, Text)
    assert t.plain == "Pa"
    assert not t._spans


def test_format_swara_komal():
    t = format_swara("komal Re")
    assert t.plain == "Re"
    assert any(s.style == "yellow" for s in t._spans)


def test_format_swara_tivra():
    t = format_swara("tivra Ma")
    assert "Ma" in t.plain
    assert "♯" in t.plain
    assert any("magenta" in str(s.style) for s in t._spans)


def test_format_swara_upper_sa():
    t = format_swara("SA")
    assert t.plain == "SA"
    assert any(s.style == "bold" for s in t._spans)


def test_format_scale_joins_with_spaces():
    t = format_scale(["Sa", "Re", "Ga"])
    assert "Sa" in t.plain
    assert "Re" in t.plain
    assert "Ga" in t.plain


def test_format_scale_single():
    t = format_scale(["Sa"])
    assert t.plain == "Sa"


def test_time_label_known():
    t = time_label("evening")
    assert t.plain == "Evening"
    assert any("orange" in str(s.style) for s in t._spans)


def test_time_label_unknown_fallback():
    t = time_label("notavalidtime")
    assert t.plain == "Notavalidtime"


def test_format_theka_length():
    theka = ["Dha", "Dhin", "Dhin", "Dha"]
    vibhags = [2, 2]
    t = format_theka(theka, vibhags)
    assert isinstance(t, Text)
    for bol in ["Dha", "Dhin"]:
        assert bol in t.plain


def test_format_theka_khali_dim():
    theka = ["Dha", "~Tin"]
    vibhags = [1, 1]
    t = format_theka(theka, vibhags)
    assert "Tin" in t.plain
