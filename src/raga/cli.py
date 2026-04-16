import typer

from raga.commands.list_ragas import list_ragas
from raga.commands.lookup import lookup
from raga.commands.suggest import suggest

app = typer.Typer(
    help="Hindustani raga reference — look up ragas, browse by thaat, time, and mood.",
    no_args_is_help=True,
)

app.command("lookup")(lookup)
app.command("list")(list_ragas)
app.command("suggest")(suggest)

if __name__ == "__main__":
    app()
