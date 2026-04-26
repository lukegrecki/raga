from typing import Callable, TypeVar

from rich import print as rprint
from rich.text import Text

Entity = TypeVar("Entity")


def format_swara(swara: str) -> Text:
    if swara.startswith("komal "):
        note = swara[6:]
        t = Text(note)
        t.stylize("yellow")
        return t
    elif swara.startswith("tivra "):
        note = swara[6:] + "\u266f"
        t = Text(note)
        t.stylize("bold magenta")
        return t
    elif swara == "SA":
        t = Text(swara)
        t.stylize("bold")
        return t
    return Text(swara)


def format_scale(swaras: list[str]) -> Text:
    result = Text()
    for i, swara in enumerate(swaras):
        if i > 0:
            result.append("  ")
        result.append_text(format_swara(swara))
    return result


def format_scale_highlighted(swaras: list[str], active: int | None) -> Text:
    result = Text()
    for i, swara in enumerate(swaras):
        if i > 0:
            result.append("  ")
        start = len(result)
        result.append_text(format_swara(swara))
        if i == active:
            result.stylize("reverse bold", start, len(result))
    return result


TIME_LABELS = {
    "dawn": "Dawn",
    "morning": "Morning",
    "afternoon": "Afternoon",
    "evening": "Evening",
    "dusk": "Dusk",
    "night": "Night",
    "late night": "Late night",
    "midnight": "Midnight",
    "any": "Any time",
}

TIME_COLORS = {
    "dawn": "bright_yellow",
    "morning": "yellow",
    "afternoon": "bright_white",
    "evening": "orange3",
    "dusk": "dark_orange",
    "night": "blue",
    "late night": "dark_blue",
    "midnight": "medium_purple4",
    "any": "white",
}


def format_theka(theka: list[str], vibhags: list[int]) -> Text:
    result = Text()
    bol_idx = 0
    beat = 1
    for v_size in vibhags:
        result.append(f"  {beat:>2}  ", style="dim")
        for i in range(v_size):
            if i > 0:
                result.append("  ")
            bol = theka[bol_idx]
            if bol.startswith("~"):
                result.append(bol[1:], style="dim italic")
            elif bol == "—":
                result.append("—", style="dim")
            elif bol_idx == 0:
                result.append(bol, style="bold cyan")
            else:
                result.append(bol)
            bol_idx += 1
        result.append("\n")
        beat += v_size
    return result


def time_label(time: str) -> Text:
    label = TIME_LABELS.get(time, time.title())
    color = TIME_COLORS.get(time, "white")
    t = Text(label)
    t.stylize(color)
    return t


def render_no_match(name: str, suggestions: list[str], list_cmd: str) -> None:
    if suggestions:
        rprint(
            f"[yellow]No exact match for[/yellow] [bold]{name!r}[/bold]"
            "[yellow]. Did you mean:[/yellow]"
        )
        for s in suggestions:
            rprint(f"  [cyan]•[/cyan] {s}")
    else:
        rprint(f"[red]No match found for[/red] [bold]{name!r}[/bold].")
        rprint(f"[dim]Try[/dim] [bold]{list_cmd}[/bold] [dim]to browse all.[/dim]")


def to_plain_text(
    entities: list[Entity],
    headers: list[str],
    row_builder: Callable[[Entity], list[str]],
    noun_plural: str,
    filter_info: str = "",
) -> str:
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
        parts.append(f"Showing {len(entities)} {noun_plural} · {filter_info}")
        parts.append("")

    parts += [header_line, separator] + data_lines
    return "\n".join(parts)
