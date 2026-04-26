from typer.testing import CliRunner

from raga.cli import app

runner = CliRunner()


class TestRagaLookup:
    def test_lookup_exact_match(self):
        result = runner.invoke(app, ["lookup", "Yaman"])
        assert result.exit_code == 0
        assert "Yaman" in result.output

    def test_lookup_alias(self):
        result = runner.invoke(app, ["lookup", "Kalyan"])
        assert result.exit_code == 0
        assert "Yaman" in result.output

    def test_lookup_case_insensitive(self):
        result = runner.invoke(app, ["lookup", "yaman"])
        assert result.exit_code == 0
        assert "Yaman" in result.output

    def test_lookup_fuzzy_match(self):
        result = runner.invoke(app, ["lookup", "bhair"])
        assert result.exit_code == 0
        assert "Bhairav" in result.output

    def test_lookup_no_match_no_suggestions(self):
        result = runner.invoke(app, ["lookup", "xyzzzz999"])
        assert result.exit_code == 0
        assert "No match found" in result.output

    def test_lookup_partial_match_with_suggestions(self):
        result = runner.invoke(app, ["lookup", "rag"])
        assert result.exit_code == 0
        assert "Did you mean" in result.output

    def test_lookup_missing_argument(self):
        result = runner.invoke(app, ["lookup"])
        assert result.exit_code == 2


class TestRagaList:
    def test_list_all(self):
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "Raga" in result.output

    def test_list_filter_by_thaat(self):
        result = runner.invoke(app, ["list", "--thaat", "Kalyan"])
        assert result.exit_code == 0
        assert "Yaman" in result.output

    def test_list_filter_by_mood(self):
        result = runner.invoke(app, ["list", "--mood", "devotional"])
        assert result.exit_code == 0

    def test_list_filter_by_time(self):
        result = runner.invoke(app, ["list", "--time", "evening"])
        assert result.exit_code == 0

    def test_list_filter_by_season(self):
        result = runner.invoke(app, ["list", "--season", "spring"])
        assert result.exit_code == 0

    def test_list_no_match(self):
        result = runner.invoke(app, ["list", "--thaat", "Nonexistent"])
        assert result.exit_code == 0
        assert "No ragas match" in result.output

    def test_list_plain_output(self):
        result = runner.invoke(app, ["list", "--plain"])
        assert result.exit_code == 0
        assert "Yaman" in result.output

    def test_list_combined_filters(self):
        result = runner.invoke(app, ["list", "--thaat", "Kalyan", "--mood", "romantic"])
        assert result.exit_code == 0


class TestRagaSuggest:
    def test_suggest_with_explicit_time(self):
        result = runner.invoke(app, ["suggest", "--time", "evening"])
        assert result.exit_code == 0

    def test_suggest_with_mood(self):
        result = runner.invoke(app, ["suggest", "--mood", "devotional"])
        assert result.exit_code == 0

    def test_suggest_with_count(self):
        result = runner.invoke(app, ["suggest", "--count", "1"])
        assert result.exit_code == 0

    def test_suggest_no_match_invalid_mood(self):
        result = runner.invoke(app, ["suggest", "--mood", "fakemood"])
        assert result.exit_code == 1
        assert "No ragas found" in result.output

    def test_suggest_no_match_combined_filters(self):
        result = runner.invoke(
            app, ["suggest", "--time", "faketime", "--mood", "fakemood"]
        )
        assert result.exit_code == 1
        assert "No ragas found" in result.output


class TestRagaPlay:
    def test_play_tempo_zero(self):
        result = runner.invoke(
            app, ["play", "Yaman", "--tempo", "0", "--soundfont", "fake.sf2"]
        )
        assert result.exit_code == 2
        assert "Tempo" in result.output

    def test_play_tempo_negative(self):
        result = runner.invoke(
            app, ["play", "Yaman", "--tempo", "-1", "--soundfont", "fake.sf2"]
        )
        assert result.exit_code == 2
        assert "Tempo" in result.output

    def test_play_no_soundfont_no_env(self, monkeypatch):
        monkeypatch.delenv("RAGA_SOUNDFONT", raising=False)
        result = runner.invoke(app, ["play", "Yaman"])
        assert result.exit_code == 2
        assert "soundfont" in result.output.lower()

    def test_play_invalid_sa_note(self):
        result = runner.invoke(
            app, ["play", "Yaman", "--sa", "Z99", "--soundfont", "fake.sf2"]
        )
        assert result.exit_code == 2
        assert "--sa" in result.output or "invalid" in result.output.lower()

    def test_play_raga_not_found(self):
        result = runner.invoke(
            app, ["play", "xyzzzz999", "--soundfont", "fake.sf2"]
        )
        assert result.exit_code == 1
        assert "No match found" in result.output
