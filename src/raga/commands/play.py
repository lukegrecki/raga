from __future__ import annotations

import os
from pathlib import Path

import typer
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from raga.audio import parse_note_name, play_notes, swaras_to_midi
from raga.completers import complete_raga_names
from raga.display import format_scale, format_scale_highlighted, render_no_match
from raga.models import load_ragas
from raga.search import find_entity

console = Console()


def play(
    name: str = typer.Argument(
        ..., help="Raga name to play", autocompletion=complete_raga_names
    ),
    sa: str = typer.Option("C4", help="Sa reference note (e.g. C4, D4)"),
    tempo: int = typer.Option(80, help="Tempo in BPM"),
    soundfont: Path | None = typer.Option(None, help="Path to SF2 soundfont file"),
) -> None:
    """Play a raga's arohana and avarohana through FluidSynth."""
    if tempo <= 0:
        raise typer.BadParameter("Tempo must be greater than 0.", param_hint="--tempo")

    sf_env = os.environ.get("RAGA_SOUNDFONT")
    resolved_sf = soundfont or (Path(sf_env) if sf_env else None)
    if resolved_sf is None:
        raise typer.BadParameter(
            "Provide --soundfont or set RAGA_SOUNDFONT. "
            "Install FluidSynth via `brew install fluid-synth` "
            "and download a SoundFont like FluidR3_GM.sf2.",
            param_hint="--soundfont",
        )

    try:
        sa_midi = parse_note_name(sa)
    except ValueError as e:
        raise typer.BadParameter(str(e), param_hint="--sa") from e

    ragas = load_ragas()
    raga, suggestions = find_entity(name, ragas)

    if raga is None:
        render_no_match(name, suggestions, "raga list")
        raise typer.Exit(1)

    all_swaras = raga.arohana + raga.avarohana
    try:
        midi_notes = swaras_to_midi(all_swaras, sa_midi)
    except ValueError as e:
        raise typer.BadParameter(str(e), param_hint="swaras") from e

    gap_indices = [len(raga.arohana) - 1]

    grid = Table.grid(padding=(0, 2))
    grid.add_column(style="bold dim", min_width=12)
    grid.add_column()
    grid.add_row("Sa", sa)
    grid.add_row("Tempo", f"{tempo} BPM")
    grid.add_row("", "")
    grid.add_row("Arohana", format_scale(raga.arohana))
    grid.add_row("Avarohana", format_scale(raga.avarohana))

    console.print(Panel(
        grid,
        title=Text(raga.name, style="bold"),
        border_style="bright_black",
        padding=(1, 2),
    ))

    arohana_len = len(raga.arohana)

    def render_playing(active: int | None) -> Text:
        if active is None:
            aro_active: int | None = None
            ava_active: int | None = None
        elif active < arohana_len:
            aro_active = active
            ava_active = None
        else:
            aro_active = None
            ava_active = active - arohana_len

        line = Text()
        line.append_text(format_scale_highlighted(raga.arohana, aro_active))
        line.append("  ·  ", style="dim")
        line.append_text(format_scale_highlighted(raga.avarohana, ava_active))
        return line

    with Live(
        render_playing(None), console=console, refresh_per_second=30, transient=False
    ) as live:
        def on_note(i: int | None) -> None:
            live.update(render_playing(i))
        play_notes(midi_notes, tempo, resolved_sf, gap_indices, on_note=on_note)
