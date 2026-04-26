from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from raga.completers import (
    complete_moods,
    complete_seasons,
    complete_thaats,
    complete_times,
)
from raga.display import format_swara, time_label, to_plain_text
from raga.models import load_ragas

console = Console()



def list_ragas(
    thaat: Optional[str] = typer.Option(
        None, "--thaat", "-t", help="Filter by thaat (e.g. Kalyan, Bhairav)",
        autocompletion=complete_thaats,
    ),
    time: Optional[str] = typer.Option(
        None, "--time", help="Filter by time (e.g. morning, evening, night)",
        autocompletion=complete_times,
    ),
    mood: Optional[str] = typer.Option(
        None, "--mood", "-m", help="Filter by mood (e.g. devotional, romantic)",
        autocompletion=complete_moods,
    ),
    season: Optional[str] = typer.Option(
        None, "--season", "-s", help="Filter by season (e.g. spring, winter)",
        autocompletion=complete_seasons,
    ),
    plain: bool = typer.Option(
        False, "--plain", help="Output plain text, suitable for piping or redirection",
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Write plain text output to a file",
    ),
) -> None:
    """List all ragas, with optional filters."""
    ragas = load_ragas()
    filtered = [
        r for r in ragas if r.matches(thaat=thaat, time=time, mood=mood, season=season)
    ]

    if not filtered:
        rprint("[yellow]No ragas match the given filters.[/yellow]")
        return

    if plain or output:
        sorted_filtered = sorted(filtered, key=lambda r: r.name)
        headers = ["Raga", "Thaat", "Time", "Vadi", "Samvadi", "Mood"]
        filter_parts = []
        if thaat:
            filter_parts.append(f"thaat={thaat}")
        if time:
            filter_parts.append(f"time={time}")
        if mood:
            filter_parts.append(f"mood={mood}")
        if season:
            filter_parts.append(f"season={season}")
        filter_info = ", ".join(filter_parts) if filter_parts else ""
        text = to_plain_text(
            sorted_filtered,
            headers,
            lambda r: [
                r.name,
                r.thaat or "—",
                r.time.title(),
                r.vadi,
                r.samvadi,
                ", ".join(r.mood) if r.mood else "-",
            ],
            noun_plural="ragas",
            filter_info=filter_info,
        )
        if output:
            output.write_text(text)
            typer.echo(f"Wrote {len(filtered)} raga(s) to {output}")
        else:
            typer.echo(text)
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
            raga.thaat or "—",
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
