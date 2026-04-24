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

✅ **Duplicated search/list logic** — Fixed in commit a8e62b1

---

## Testing Gaps

✅ **End-to-end CLI tests via Typer's test runner** — Fixed in commit d785b69

- `completers.py` has zero test coverage.
- No error-path tests: missing JSON file, soundfont file not found.

---

## UX

- When `raga list --mood <invalid>` returns nothing, the error doesn't hint at valid mood values.
- The soundfont error message doesn't mention the `RAGA_SOUNDFONT` env var prominently enough.
- When fuzzy lookup finds no match and score < 40, there's no recovery hint — could fall back to showing the 3 closest names anyway.

---

## Priority Order

1. ✅ Fix Pilu `vadi` data bug
2. ✅ Add MIDI bounds validation
3. ✅ Add FluidSynth init error handling
4. ✅ Deduplicate search logic into `search.py`
5. 🟨 Fill testing gaps: ✅ CLI integration, 🔲 completers coverage, 🔲 error-path tests
