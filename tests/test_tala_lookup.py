from raga.search import build_corpus, find_entity


def test_build_corpus_includes_name(talas):
    corpus = build_corpus(talas)
    names = [c[0] for c in corpus]
    assert "teentaal" in names


def test_build_corpus_includes_aliases(talas):
    corpus = build_corpus(talas)
    names = [c[0] for c in corpus]
    assert "tritaal" in names  # alias for Teentaal


def test_find_tala_exact(talas):
    tala, suggestions = find_entity("Teentaal", talas)
    assert tala is not None
    assert tala.name == "Teentaal"
    assert suggestions == []


def test_find_tala_case_insensitive(talas):
    tala, suggestions = find_entity("teentaal", talas)
    assert tala is not None
    assert tala.name == "Teentaal"
    assert suggestions == []


def test_find_tala_by_alias(talas):
    tala, suggestions = find_entity("Tritaal", talas)
    assert tala is not None
    assert tala.name == "Teentaal"
    assert suggestions == []


def test_find_tala_fuzzy(talas):
    tala, suggestions = find_entity("jhap", talas)
    assert tala is not None
    assert "jhap" in tala.name.lower()
    assert suggestions == []


def test_find_tala_no_match(talas):
    tala, suggestions = find_entity("xyzzzz999", talas)
    assert tala is None
    assert suggestions == []


def test_find_tala_jhaptaal(talas):
    tala, _ = find_entity("Jhaptaal", talas)
    assert tala is not None
    assert tala.name == "Jhaptaal"
    assert tala.beats == 10


def test_find_tala_fuzzy_returns_suggestions(talas):
    # "xyla" scores 40-74 against several talas — no match, but non-empty suggestions
    tala, suggestions = find_entity("xyla", talas)
    assert tala is None
    assert len(suggestions) > 0


def test_find_tala_suggestions_deduplicated(talas):
    # "triteen" hits teentaal, tritaal, teen taal, trital — all aliases of Teentaal;
    # dedup via dict.fromkeys should ensure Teentaal appears only once
    tala, suggestions = find_entity("triteen", talas)
    assert tala is None
    assert suggestions.count("Teentaal") == 1


def test_find_tala_empty_query(talas):
    tala, suggestions = find_entity("", talas)
    assert tala is None
    assert suggestions == []
