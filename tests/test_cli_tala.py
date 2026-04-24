from typer.testing import CliRunner

from raga.tala_cli import app

runner = CliRunner()


class TestTalaLookup:
    def test_lookup_exact_match(self):
        result = runner.invoke(app, ["lookup", "Teentaal"])
        assert result.exit_code == 0
        assert "Teentaal" in result.output

    def test_lookup_alias(self):
        result = runner.invoke(app, ["lookup", "Tritaal"])
        assert result.exit_code == 0
        assert "Teentaal" in result.output

    def test_lookup_case_insensitive(self):
        result = runner.invoke(app, ["lookup", "teentaal"])
        assert result.exit_code == 0
        assert "Teentaal" in result.output

    def test_lookup_no_match_no_suggestions(self):
        result = runner.invoke(app, ["lookup", "xyzzzz999"])
        assert result.exit_code == 0
        assert "No tala found" in result.output

    def test_lookup_fuzzy_match(self):
        result = runner.invoke(app, ["lookup", "teen"])
        assert result.exit_code == 0
        assert "Teentaal" in result.output

    def test_lookup_missing_argument(self):
        result = runner.invoke(app, ["lookup"])
        assert result.exit_code == 2


class TestTalaList:
    def test_list_all(self):
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "Tala" in result.output

    def test_list_filter_by_beats(self):
        result = runner.invoke(app, ["list", "--beats", "16"])
        assert result.exit_code == 0
        assert "Teentaal" in result.output

    def test_list_filter_by_feel(self):
        result = runner.invoke(app, ["list", "--feel", "versatile"])
        assert result.exit_code == 0

    def test_list_filter_by_tempo(self):
        result = runner.invoke(app, ["list", "--tempo", "madhya"])
        assert result.exit_code == 0

    def test_list_no_match(self):
        result = runner.invoke(app, ["list", "--beats", "999"])
        assert result.exit_code == 0
        assert "No talas match" in result.output

    def test_list_plain_output(self):
        result = runner.invoke(app, ["list", "--plain"])
        assert result.exit_code == 0
        assert "Teentaal" in result.output

    def test_list_combined_filters(self):
        result = runner.invoke(app, ["list", "--beats", "16", "--feel", "versatile"])
        assert result.exit_code == 0


class TestTalaSuggest:
    def test_suggest_with_beats(self):
        result = runner.invoke(app, ["suggest", "--beats", "16", "--count", "1"])
        assert result.exit_code == 0

    def test_suggest_with_feel(self):
        result = runner.invoke(app, ["suggest", "--feel", "lively", "--count", "1"])
        assert result.exit_code == 0

    def test_suggest_with_tempo(self):
        result = runner.invoke(app, ["suggest", "--tempo", "madhya", "--count", "1"])
        assert result.exit_code == 0

    def test_suggest_invalid_beats(self):
        result = runner.invoke(app, ["suggest", "--beats", "999"])
        assert result.exit_code == 1
        assert "No talas found" in result.output

    def test_suggest_invalid_feel(self):
        result = runner.invoke(app, ["suggest", "--feel", "fakefeel"])
        assert result.exit_code == 1
        assert "No talas found" in result.output

    def test_suggest_invalid_tempo(self):
        result = runner.invoke(app, ["suggest", "--tempo", "faketempo"])
        assert result.exit_code == 1
        assert "No talas found" in result.output
