import typer
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from raga.search import find_entity
from raga.completers import complete_raga_names
from raga.display import format_scale, format_swara, time_label
from raga.models import Raga, load_ragas

console = Console()


def _render_raga(raga: Raga) -> Panel:
    grid = Table.grid(padding=(0, 2))
    grid.add_column(style="bold dim", min_width=12)
    grid.add_column()

    grid.add_row("Thaat", raga.thaat)
    grid.add_row("Time", time_label(raga.time))
    vadi_text = Text()
    vadi_text.append_text(format_swara(raga.vadi))
    vadi_text.append("  /  ")
    vadi_text.append_text(format_swara(raga.samvadi))
    grid.add_row("Vadi / Samvadi", vadi_text)

    mood_text = ", ".join(raga.mood) if raga.mood else "—"
    grid.add_row("Mood", mood_text)

    if raga.season:
        grid.add_row("Season", raga.season.title())

    grid.add_row("", "")
    grid.add_row("Arohana", format_scale(raga.arohana))
    grid.add_row("Avarohana", format_scale(raga.avarohana))

    if raga.pakad:
        grid.add_row("", "")
        grid.add_row("Pakad", Text(raga.pakad, style="italic"))

    if raga.description:
        grid.add_row("", "")
        grid.add_row("", Text(raga.description, style="dim"))

    title = Text(raga.name, style="bold")
    if raga.aliases:
        title.append(f"  ·  {' / '.join(raga.aliases)}", style="dim")

    return Panel(grid, title=title, border_style="bright_black", padding=(1, 2))


def lookup(
    name: str = typer.Argument(
        ..., help="Raga name to look up", autocompletion=complete_raga_names
    ),
) -> None:
    """Look up a raga by name."""
    ragas = load_ragas()
    raga, suggestions = find_entity(name, ragas)

    if raga:
        console.print(_render_raga(raga))
        return

    if suggestions:
        rprint(
            f"[yellow]No exact match for[/yellow] [bold]{name!r}[/bold]"
            "[yellow]. Did you mean:[/yellow]"
        )
        for s in suggestions:
            rprint(f"  [cyan]•[/cyan] {s}")
    else:
        rprint(f"[red]No raga found matching[/red] [bold]{name!r}[/bold].")
        rprint("[dim]Try[/dim] [bold]raga list[/bold] [dim]to browse all ragas.[/dim]")
