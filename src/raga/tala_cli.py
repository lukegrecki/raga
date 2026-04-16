import typer

from raga.commands.list_talas import list_talas
from raga.commands.lookup_tala import lookup_tala
from raga.commands.suggest_tala import suggest_tala

app = typer.Typer(
    help="Hindustani tala reference — look up talas, browse by beats, feel, and tempo.",
    no_args_is_help=True,
)

app.command("lookup")(lookup_tala)
app.command("list")(list_talas)
app.command("suggest")(suggest_tala)

if __name__ == "__main__":
    app()
