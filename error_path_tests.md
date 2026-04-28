# Error-Path Tests — Implementation Status

## Completed Tests ✓

### `models.py` — Tala validation
- ✓ `theka` length ≠ `beats` raises `ValueError`
- ✓ `vibhags` sum ≠ `beats` raises `ValueError`
- ✓ Missing required field raises `ValidationError`

### `audio.parse_note_name` — boundary cases
- ✓ Out-of-MIDI-range raises (e.g. `"C-2"`, `"G#9"`)
- ✓ Lowercase letter (`"c4"`) fails the regex
- ✓ Double accidentals (`"C##4"`) fail
- ✓ Invalid letter (`"H4"`) fails the regex

### `audio.swaras_to_midi`
- ✓ Case mismatch (`"sa"` vs `"Sa"`) raises
- ✓ Empty list returns `[]`
- ✓ `sa_midi` that pushes SA past 127 — returns values without raising

### `audio.play_notes` — error handling
- ✓ `sfload` returning `-1` raises `RuntimeError` with soundfont guidance
- ✓ Driver `RuntimeError` is wrapped with install hint
- ✓ `fs.delete()` runs even when an exception is raised (finally block)

### CLI commands
- ✓ `raga lookup <unknown>` shows "No match found" or suggestions
- ✓ `raga list --thaat <invalid>` returns empty friendly message
- ✓ `raga play` with no soundfont configured — raises with error message
- ✓ `raga play --sa Q9` surfaces the `parse_note_name` ValueError cleanly
- ✓ `raga play --tempo 0` or negative — rejected at input validation
- ✓ `tala lookup <unknown>` shows "No match found" or suggestions
- ✓ `tala list --beats <invalid>` returns empty friendly message

### Data integrity
- ✓ Every raga's `vadi`/`samvadi` is a known swara
- ✓ Every raga's `time` is in the documented set
- ✓ Every tala's `tempo` values are in `{vilambit, madhya, drut}`

## Known Latent Bugs (not yet fixed)
- tempo=0 division (audio.py:71) — will raise `ZeroDivisionError`
- Silent SA>127 case (audio.py:58) — should decide if this raises
