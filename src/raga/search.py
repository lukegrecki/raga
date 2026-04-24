from rapidfuzz import fuzz, process
from typing import TypeVar, Callable, Protocol

FUZZY_EXACT_THRESHOLD = 75
FUZZY_SUGGESTION_THRESHOLD = 40

Entity = TypeVar("Entity")


class EntityLike(Protocol):
    """Any entity type with name and aliases attributes."""

    name: str
    aliases: list[str]


def build_corpus(entities: list[EntityLike]) -> list[tuple[str, EntityLike]]:
    """Build a searchable corpus from entities and their aliases."""
    corpus: list[tuple[str, EntityLike]] = []
    for entity in entities:
        corpus.append((entity.name.lower(), entity))
        for alias in entity.aliases:
            corpus.append((alias.lower(), entity))
    return corpus


def find_entity(
    query: str, entities: list[EntityLike]
) -> tuple[EntityLike | None, list[str]]:
    """Fuzzy search for an entity, returning best match and suggestions.

    Returns a tuple of (matched_entity, suggestion_names).
    If a high-confidence match is found, matched_entity is set and suggestions is empty.
    Otherwise, matched_entity is None and suggestions contains candidates above the threshold.
    """
    corpus = build_corpus(entities)
    names = [c[0] for c in corpus]
    results = process.extract(query.lower(), names, scorer=fuzz.WRatio, limit=5)

    if not results:
        return None, []

    best_score = results[0][1]
    if best_score >= FUZZY_EXACT_THRESHOLD:
        idx = names.index(results[0][0])
        return corpus[idx][1], []

    suggestions = []
    for name, score, _ in results:
        if score >= FUZZY_SUGGESTION_THRESHOLD:
            idx = names.index(name)
            suggestions.append(corpus[idx][1].name)
    return None, list(dict.fromkeys(suggestions))


def to_plain_text(
    entities: list[Entity],
    headers: list[str],
    row_builder: Callable[[Entity], list[str]],
    filter_info: str = "",
) -> str:
    """Generate plain text table output for a list of entities.

    Args:
        entities: List of entities to display
        headers: Column headers
        row_builder: Function that takes an entity and returns a list of cell strings
        filter_info: Optional description of applied filters (e.g. "thaat=Kalyan")

    Returns:
        Formatted plain text table
    """
    rows = [row_builder(entity) for entity in entities]
    widths = [
        max(len(h), max((len(row[i]) for row in rows), default=0))
        for i, h in enumerate(headers)
    ]
    header_line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers)).rstrip()
    separator = "-" * (sum(widths) + 2 * (len(widths) - 1))
    data_lines = [
        "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip()
        for row in rows
    ]

    parts = []
    if filter_info:
        parts.append(f"Showing {len(entities)} entity/entities · {filter_info}")
        parts.append("")

    parts += [header_line, separator] + data_lines
    return "\n".join(parts)
