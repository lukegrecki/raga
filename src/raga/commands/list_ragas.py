from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.text import Text

from raga.completers import complete_moods, complete_seasons, complete_thaats, complete_times
from raga.display import TIME_COLORS, format_swara, time_label
from raga.models import Raga, load_ragas

console = Console()


def _matches(raga: Raga, thaat: Optional[str], time: Optional[str], mood: Optional[str], season: Optional[str]) -> bool:
    if thaat and raga.thaat.lower() != thaat.lower():
        return False
    if time and raga.time.lower() != time.lower():
        return False
    if mood and mood.lower() not in [m.lower() for m in raga.mood]:
        return False
    if season:
        if raga.season is None or raga.season.lower() != season.lower():
            return False
    return True


def list_ragas(
    thaat: Optional[str] = typer.Option(None, "--thaat", "-t", help="Filter by thaat (e.g. Kalyan, Bhairav)", autocompletion=complete_thaats),
    time: Optional[str] = typer.Option(None, "--time", help="Filter by time (e.g. morning, evening, night)", autocompletion=complete_times),
    mood: Optional[str] = typer.Option(None, "--mood", "-m", help="Filter by mood (e.g. devotional, romantic)", autocompletion=complete_moods),
    season: Optional[str] = typer.Option(None, "--season", "-s", help="Filter by season (e.g. spring, winter)", autocompletion=complete_seasons),
) -> None:
    """List all ragas, with optional filters."""
    ragas = load_ragas()
    filtered = [r for r in ragas if _matches(r, thaat, time, mood, season)]

    if not filtered:
        rprint("[yellow]No ragas match the given filters.[/yellow]")
        return

    table = Table(
        show_header=True,
        header_style="bold",
        border_style="bright_black",
        row_styles=["", "dim"],
        expand=False,
        padding=(0, 1),
    )
    table.add_column("Raga", min_width=18)
    table.add_column("Thaat", min_width=12)
    table.add_column("Time", min_width=12)
    table.add_column("Vadi", min_width=8)
    table.add_column("Mood")

    for raga in sorted(filtered, key=lambda r: r.name):
        mood_text = ", ".join(raga.mood[:2]) if raga.mood else "—"
        if len(raga.mood) > 2:
            mood_text += f" +{len(raga.mood) - 2}"
        table.add_row(
            raga.name,
            raga.thaat,
            time_label(raga.time),
            format_swara(raga.vadi),
            mood_text,
        )

    if any([thaat, time, mood, season]):
        parts = []
        if thaat:
            parts.append(f"thaat=[bold]{thaat}[/bold]")
        if time:
            parts.append(f"time=[bold]{time}[/bold]")
        if mood:
            parts.append(f"mood=[bold]{mood}[/bold]")
        if season:
            parts.append(f"season=[bold]{season}[/bold]")
        rprint(f"[dim]Showing {len(filtered)} raga(s) · {', '.join(parts)}[/dim]")

    console.print(table)
