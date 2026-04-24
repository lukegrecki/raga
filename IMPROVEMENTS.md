# Codebase Improvement Suggestions

## Bug / Data Issues

✅ **Pilu raga vadi mismatch** — Fixed in commit fa06e8b

✅ **MIDI bounds validation** — Fixed in commit fa06e8b

---

## Code Quality

✅ **Unhandled errors during FluidSynth init** — Fixed in commit c4f9e0c

✅ **Magic numbers in fuzzy search** — Fixed in commit 3e04c77

---

## Architecture

**Duplicated search/list logic**
- `lookup.py` and `lookup_tala.py` share nearly identical `_build_corpus()` and `_find_*()` structures. Same duplication exists between `list_ragas.py` and `list_talas.py`. A shared `search.py` utility would eliminate this and make adding future entity types cheap.

---

## Testing Gaps

- No end-to-end CLI tests via Typer's test runner — commands are unit-tested but not as a user would invoke them.
- `completers.py` has zero test coverage.
- No error-path tests: missing JSON file, invalid `--sa` note, soundfont not found, negative tempo.

---

## UX

- When `raga list --mood <invalid>` returns nothing, the error doesn't hint at valid mood values.
- The soundfont error message doesn't mention the `RAGA_SOUNDFONT` env var prominently enough.
- When fuzzy lookup finds no match and score < 40, there's no recovery hint — could fall back to showing the 3 closest names anyway.

---

## Priority Order

1. ✅ Fix Pilu `vadi` data bug
2. ✅ Add MIDI bounds validation
3. Add FluidSynth init error handling
4. Deduplicate search logic into `search.py`
5. Fill testing gaps (completers, CLI integration, error paths)
