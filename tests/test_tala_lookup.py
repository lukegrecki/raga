from raga.commands.lookup_tala import _build_corpus, _find_tala


def test_build_corpus_includes_name(talas):
    corpus = _build_corpus(talas)
    names = [c[0] for c in corpus]
    assert "teentaal" in names


def test_build_corpus_includes_aliases(talas):
    corpus = _build_corpus(talas)
    names = [c[0] for c in corpus]
    assert "tritaal" in names  # alias for Teentaal


def test_find_tala_exact(talas):
    tala, suggestions = _find_tala("Teentaal", talas)
    assert tala is not None
    assert tala.name == "Teentaal"
    assert suggestions == []


def test_find_tala_case_insensitive(talas):
    tala, suggestions = _find_tala("teentaal", talas)
    assert tala is not None
    assert tala.name == "Teentaal"
    assert suggestions == []


def test_find_tala_by_alias(talas):
    tala, suggestions = _find_tala("Tritaal", talas)
    assert tala is not None
    assert tala.name == "Teentaal"
    assert suggestions == []


def test_find_tala_fuzzy(talas):
    tala, suggestions = _find_tala("jhap", talas)
    assert tala is not None
    assert "jhap" in tala.name.lower()
    assert suggestions == []


def test_find_tala_no_match(talas):
    tala, suggestions = _find_tala("xyzzzz999", talas)
    assert tala is None
    assert suggestions == []


def test_find_tala_jhaptaal(talas):
    tala, _ = _find_tala("Jhaptaal", talas)
    assert tala is not None
    assert tala.name == "Jhaptaal"
    assert tala.beats == 10


def test_find_tala_fuzzy_returns_suggestions(talas):
    # "xyla" scores 40-74 against several talas — no match, but non-empty suggestions
    tala, suggestions = _find_tala("xyla", talas)
    assert tala is None
    assert len(suggestions) > 0


def test_find_tala_suggestions_deduplicated(talas):
    # "triteen" hits teentaal, tritaal, teen taal, trital — all aliases of Teentaal;
    # dedup via dict.fromkeys should ensure Teentaal appears only once
    tala, suggestions = _find_tala("triteen", talas)
    assert tala is None
    assert suggestions.count("Teentaal") == 1


def test_find_tala_empty_query(talas):
    tala, suggestions = _find_tala("", talas)
    assert tala is None
    assert suggestions == []
