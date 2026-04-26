import random
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console

from raga.commands.lookup_tala import _render_tala
from raga.completers import complete_beats, complete_feels, complete_tempos
from raga.models import load_talas

console = Console()


def suggest_tala(
    beats: Optional[int] = typer.Option(
        None, "--beats", "-b", help="Filter by number of beats (e.g. 16)",
        autocompletion=complete_beats,
    ),
    feel: Optional[str] = typer.Option(
        None, "--feel", "-f", help="Feel (e.g. stately, lively, versatile)",
        autocompletion=complete_feels,
    ),
    tempo: Optional[str] = typer.Option(
        None, "--tempo", "-t", help="Tempo (vilambit, madhya, drut)",
        autocompletion=complete_tempos,
    ),
    count: int = typer.Option(3, "--count", "-n", help="Number of talas to suggest"),
) -> None:
    """Suggest talas based on beats, feel, or tempo."""
    talas = load_talas()

    pool = [t for t in talas if t.matches(beats=beats, feel=feel, tempo=tempo)]

    if not pool:
        rprint("[yellow]No talas found for the given criteria.[/yellow]")
        raise typer.Exit(1)

    picks = random.sample(pool, min(count, len(pool)))

    parts = []
    if beats is not None:
        parts.append(f"[bold]{beats}[/bold] beats")
    if feel:
        parts.append(f"[italic]{feel}[/italic]")
    if tempo:
        parts.append(f"[italic]{tempo}[/italic]")

    header = "  ·  ".join(parts) if parts else "all talas"
    rprint(f"[dim]Suggesting {len(picks)} tala(s) for {header}[/dim]\n")

    for tala in picks:
        console.print(_render_tala(tala))
