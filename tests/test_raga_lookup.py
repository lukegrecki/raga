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
    assert suggestions == []


def test_find_raga_by_alias(ragas):
    raga, suggestions = _find_raga("Kalyan", ragas)
    assert raga is not None
    assert raga.name == "Yaman"
    assert suggestions == []


def test_find_raga_fuzzy(ragas):
    raga, suggestions = _find_raga("bhair", ragas)
    assert raga is not None
    assert "bhair" in raga.name.lower()
    assert suggestions == []


def test_find_raga_no_match_returns_suggestions(ragas):
    raga, suggestions = _find_raga("xyzzzz999", ragas)
    assert raga is None
    assert suggestions == []


def test_find_raga_known_raga_bhairav(ragas):
    raga, _ = _find_raga("Bhairav", ragas)
    assert raga is not None
    assert raga.name == "Bhairav"


def test_find_raga_fuzzy_returns_suggestions(ragas):
    # "rag" scores 40-74 against several ragas — no match, but non-empty suggestions
    raga, suggestions = _find_raga("rag", ragas)
    assert raga is None
    assert len(suggestions) > 0


def test_find_raga_suggestions_deduplicated(ragas):
    # "xyla" hits both "kalyan" and "yaman kalyan" aliases, both pointing to Yaman;
    # dedup via dict.fromkeys should ensure Yaman appears only once
    raga, suggestions = _find_raga("xyla", ragas)
    assert raga is None
    assert suggestions.count("Yaman") == 1


def test_find_raga_empty_query(ragas):
    raga, suggestions = _find_raga("", ragas)
    assert raga is None
    assert suggestions == []
