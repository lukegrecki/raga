from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from raga.completers import complete_beats, complete_feels, complete_tempos
from raga.display import to_plain_text
from raga.models import Tala, load_talas

console = Console()


def _matches(
    tala: Tala, beats: Optional[int], feel: Optional[str], tempo: Optional[str]
) -> bool:
    if beats is not None and tala.beats != beats:
        return False
    if feel and feel.lower() not in [f.lower() for f in tala.feel]:
        return False
    if tempo and tempo.lower() not in [t.lower() for t in tala.tempo]:
        return False
    return True


def list_talas(
    beats: Optional[int] = typer.Option(
        None, "--beats", "-b", help="Filter by number of beats (e.g. 16)",
        autocompletion=complete_beats,
    ),
    feel: Optional[str] = typer.Option(
        None, "--feel", "-f", help="Filter by feel (e.g. lively, stately)",
        autocompletion=complete_feels,
    ),
    tempo: Optional[str] = typer.Option(
        None, "--tempo", "-t", help="Filter by tempo (vilambit, madhya, drut)",
        autocompletion=complete_tempos,
    ),
    plain: bool = typer.Option(
        False, "--plain", help="Output plain text, suitable for piping or redirection",
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Write plain text output to a file",
    ),
) -> None:
    """List all talas, with optional filters."""
    talas = load_talas()
    filtered = [t for t in talas if _matches(t, beats, feel, tempo)]

    if not filtered:
        rprint("[yellow]No talas match the given filters.[/yellow]")
        return

    if plain or output:
        sorted_filtered = sorted(filtered, key=lambda t: t.name)
        headers = ["Tala", "Beats", "Vibhags", "Tempo", "Feel"]
        filter_parts = []
        if beats is not None:
            filter_parts.append(f"beats={beats}")
        if feel:
            filter_parts.append(f"feel={feel}")
        if tempo:
            filter_parts.append(f"tempo={tempo}")
        filter_info = ", ".join(filter_parts) if filter_parts else ""
        text = to_plain_text(
            sorted_filtered,
            headers,
            lambda t: [
                t.name,
                str(t.beats),
                "+".join(str(v) for v in t.vibhags),
                " / ".join(x.title() for x in t.tempo),
                ", ".join(t.feel) if t.feel else "-",
            ],
            noun_plural="talas",
            filter_info=filter_info,
        )
        if output:
            output.write_text(text)
            typer.echo(f"Wrote {len(filtered)} tala(s) to {output}")
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
    table.add_column("Tala", min_width=16)
    table.add_column("Beats", min_width=6, justify="right")
    table.add_column("Vibhags", min_width=14)
    table.add_column("Tempo", min_width=20)
    table.add_column("Feel")

    for tala in sorted(filtered, key=lambda t: t.name):
        vibhag_str = "+".join(str(v) for v in tala.vibhags)
        tempo_str = " / ".join(t.title() for t in tala.tempo)
        feel_str = ", ".join(tala.feel[:2]) if tala.feel else "—"
        if len(tala.feel) > 2:
            feel_str += f" +{len(tala.feel) - 2}"
        table.add_row(tala.name, str(tala.beats), vibhag_str, tempo_str, feel_str)

    if any(v is not None for v in [beats, feel, tempo]):
        parts = []
        if beats is not None:
            parts.append(f"beats=[bold]{beats}[/bold]")
        if feel:
            parts.append(f"feel=[bold]{feel}[/bold]")
        if tempo:
            parts.append(f"tempo=[bold]{tempo}[/bold]")
        rprint(f"[dim]Showing {len(filtered)} tala(s) · {', '.join(parts)}[/dim]")

    console.print(table)
