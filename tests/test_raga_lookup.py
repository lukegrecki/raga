from raga.commands.lookup import _build_corpus, _find_raga


def test_build_corpus_includes_name(ragas):
    corpus = _build_corpus(ragas)
    names = [c[0] for c in corpus]
    assert "yaman" in names


def test_build_corpus_includes_aliases(ragas):
    corpus = _build_corpus(ragas)
    names = [c[0] for c in corpus]
    assert "kalyan" in names  # alias for Yaman


def test_find_raga_exact(ragas):
    raga, suggestions = _find_raga("Yaman", ragas)
    assert raga is not None
    assert raga.name == "Yaman"
    assert suggestions == []


def test_find_raga_case_insensitive(ragas):
    raga, suggestions = _find_raga("yaman", ragas)
    assert raga is not None
    assert raga.name == "Yaman"


def test_find_raga_by_alias(ragas):
    raga, suggestions = _find_raga("Kalyan", ragas)
    assert raga is not None
    assert raga.name == "Yaman"


def test_find_raga_fuzzy(ragas):
    raga, suggestions = _find_raga("bhair", ragas)
    assert raga is not None
    assert "bhair" in raga.name.lower()


def test_find_raga_no_match_returns_suggestions(ragas):
    raga, suggestions = _find_raga("xyzzzz999", ragas)
    assert raga is None


def test_find_raga_known_raga_bhairav(ragas):
    raga, _ = _find_raga("Bhairav", ragas)
    assert raga is not None
    assert raga.name == "Bhairav"
