import typer
from rapidfuzz import fuzz, process
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from raga.completers import complete_tala_names
from raga.display import format_theka
from raga.models import Tala, load_talas

console = Console()


def _build_corpus(talas: list[Tala]) -> list[tuple[str, Tala]]:
    corpus: list[tuple[str, Tala]] = []
    for tala in talas:
        corpus.append((tala.name.lower(), tala))
        for alias in tala.aliases:
            corpus.append((alias.lower(), tala))
    return corpus


def _find_tala(query: str, talas: list[Tala]) -> tuple[Tala | None, list[str]]:
    corpus = _build_corpus(talas)
    names = [c[0] for c in corpus]
    results = process.extract(query.lower(), names, scorer=fuzz.WRatio, limit=5)

    if not results:
        return None, []

    if results[0][1] >= 75:
        idx = names.index(results[0][0])
        return corpus[idx][1], []

    suggestions = []
    for name, score, _ in results:
        if score >= 40:
            idx = names.index(name)
            suggestions.append(corpus[idx][1].name)
    return None, list(dict.fromkeys(suggestions))


def _render_tala(tala: Tala) -> Panel:
    from rich.table import Table

    grid = Table.grid(padding=(0, 2))
    grid.add_column(style="bold dim", min_width=12)
    grid.add_column()

    vibhag_str = " + ".join(str(v) for v in tala.vibhags)
    beats_text = Text(f"{tala.beats}   ·   {vibhag_str}", style="")
    grid.add_row("Beats / Vibhags", beats_text)

    tempo_text = " / ".join(t.title() for t in tala.tempo)
    grid.add_row("Tempo", tempo_text)

    feel_text = ", ".join(tala.feel) if tala.feel else "—"
    grid.add_row("Feel", feel_text)

    grid.add_row("", "")
    grid.add_row("Theka", format_theka(tala.theka, tala.vibhags))

    if tala.description:
        grid.add_row("", Text(tala.description, style="dim"))

    title = Text(tala.name, style="bold")
    if tala.aliases:
        title.append(f"  ·  {' / '.join(tala.aliases)}", style="dim")

    return Panel(grid, title=title, border_style="bright_black", padding=(1, 2))


def lookup_tala(
    name: str = typer.Argument(
        ..., help="Tala name to look up", autocompletion=complete_tala_names
    ),
) -> None:
    """Look up a tala by name."""
    talas = load_talas()
    tala, suggestions = _find_tala(name, talas)

    if tala:
        console.print(_render_tala(tala))
        return

    if suggestions:
        rprint(
            f"[yellow]No exact match for[/yellow] [bold]{name!r}[/bold]"
            "[yellow]. Did you mean:[/yellow]"
        )
        for s in suggestions:
            rprint(f"  [cyan]•[/cyan] {s}")
    else:
        rprint(f"[red]No tala found matching[/red] [bold]{name!r}[/bold].")
        rprint("[dim]Try[/dim] [bold]tala list[/bold] [dim]to browse all talas.[/dim]")
