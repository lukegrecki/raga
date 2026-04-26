from typing import Protocol, TypeVar

from rapidfuzz import fuzz, process

FUZZY_EXACT_THRESHOLD = 75
FUZZY_SUGGESTION_THRESHOLD = 40


class EntityLike(Protocol):
    """Any entity type with name and aliases attributes."""

    name: str
    aliases: list[str]


EntityT = TypeVar("EntityT", bound=EntityLike)


def build_corpus(entities: list[EntityT]) -> list[tuple[str, EntityT]]:
    corpus: list[tuple[str, EntityT]] = []
    for entity in entities:
        corpus.append((entity.name.lower(), entity))
        for alias in entity.aliases:
            corpus.append((alias.lower(), entity))
    return corpus


def find_entity(
    query: str, entities: list[EntityT]
) -> tuple[EntityT | None, list[str]]:
    """Fuzzy search for an entity, returning best match and suggestions.

    Returns (matched_entity, suggestion_names). If high-confidence match found,
    matched_entity is set and suggestions is empty; otherwise the reverse.
    """
    corpus = build_corpus(entities)
    names = [c[0] for c in corpus]
    results = process.extract(query.lower(), names, scorer=fuzz.WRatio, limit=5)

    if not results:
        return None, []

    _, best_score, best_idx = results[0]
    if best_score >= FUZZY_EXACT_THRESHOLD:
        return corpus[best_idx][1], []

    suggestions = []
    for _, score, idx in results:
        if score >= FUZZY_SUGGESTION_THRESHOLD:
            suggestions.append(corpus[idx][1].name)
    return None, list(dict.fromkeys(suggestions))
