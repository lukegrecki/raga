import random
from datetime import datetime
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console

from raga.commands.lookup import _render_raga
from raga.completers import complete_moods, complete_times
from raga.display import TIME_COLORS
from raga.models import Raga, load_ragas

console = Console()

TIME_RANGES = [
    (4, 6, "dawn"),
    (6, 12, "morning"),
    (12, 16, "afternoon"),
    (16, 18, "evening"),
    (18, 19, "dusk"),
    (19, 22, "night"),
    (22, 24, "late night"),
    (0, 4, "midnight"),
]


def _current_time_of_day() -> str:
    hour = datetime.now().hour
    for start, end, label in TIME_RANGES:
        if start <= hour < end:
            return label
    return "any"


def suggest(
    time: Optional[str] = typer.Option(
        None,
        "--time",
        help="Time of day (e.g. morning, evening). Defaults to current time.",
        autocompletion=complete_times,
    ),
    mood: Optional[str] = typer.Option(
        None, "--mood", "-m", help="Mood (e.g. devotional, romantic)",
        autocompletion=complete_moods,
    ),
    count: int = typer.Option(3, "--count", "-n", help="Number of ragas to suggest"),
) -> None:
    """Suggest ragas suited to the current time or a given mood."""
    ragas = load_ragas()

    detected_time = time
    if not detected_time and not mood:
        detected_time = _current_time_of_day()

    def matches(r: Raga) -> bool:
        if detected_time and r.time.lower() not in (detected_time.lower(), "any"):
            return False
        if mood and mood.lower() not in [m.lower() for m in r.mood]:
            return False
        return True

    pool = [r for r in ragas if matches(r)]

    if not pool:
        rprint("[yellow]No ragas found for the given criteria.[/yellow]")
        raise typer.Exit(1)

    picks = random.sample(pool, min(count, len(pool)))

    parts = []
    if detected_time:
        color = TIME_COLORS.get(detected_time, "white")
        parts.append(f"[{color}]{detected_time}[/{color}]")
    if mood:
        parts.append(f"[italic]{mood}[/italic]")

    header = "  ·  ".join(parts) if parts else "all ragas"
    rprint(f"[dim]Suggesting {len(picks)} raga(s) for {header}[/dim]\n")

    for raga in picks:
        console.print(_render_raga(raga))
