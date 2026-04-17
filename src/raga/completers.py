from raga.models import load_ragas, load_talas


def complete_raga_names(incomplete: str) -> list[str]:
    ragas = load_ragas()
    names = [r.name for r in ragas] + [a for r in ragas for a in r.aliases]
    return sorted(n for n in names if n.lower().startswith(incomplete.lower()))


def complete_tala_names(incomplete: str) -> list[str]:
    talas = load_talas()
    names = [t.name for t in talas] + [a for t in talas for a in t.aliases]
    return sorted(n for n in names if n.lower().startswith(incomplete.lower()))


def complete_thaats(incomplete: str) -> list[str]:
    ragas = load_ragas()
    thaats = sorted({r.thaat for r in ragas})
    return [t for t in thaats if t.lower().startswith(incomplete.lower())]


def complete_times(incomplete: str) -> list[str]:
    times = [
        "dawn", "morning", "afternoon", "evening", "dusk",
        "night", "late night", "midnight", "any",
    ]
    return [t for t in times if t.startswith(incomplete.lower())]


def complete_moods(incomplete: str) -> list[str]:
    ragas = load_ragas()
    moods = sorted({m for r in ragas for m in r.mood})
    return [m for m in moods if m.startswith(incomplete.lower())]


def complete_seasons(incomplete: str) -> list[str]:
    ragas = load_ragas()
    seasons = sorted({r.season for r in ragas if r.season})
    return [s for s in seasons if s.startswith(incomplete.lower())]


def complete_feels(incomplete: str) -> list[str]:
    talas = load_talas()
    feels = sorted({f for t in talas for f in t.feel})
    return [f for f in feels if f.startswith(incomplete.lower())]


def complete_tempos(incomplete: str) -> list[str]:
    options = ["vilambit", "madhya", "drut"]
    return [o for o in options if o.startswith(incomplete.lower())]


def complete_beats(incomplete: str) -> list[str]:
    talas = load_talas()
    beats = sorted({str(t.beats) for t in talas})
    return [b for b in beats if b.startswith(incomplete)]
