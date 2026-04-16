from rich.text import Text


def format_swara(swara: str) -> Text:
    if swara.startswith("komal "):
        note = swara[6:]
        t = Text(note)
        t.stylize("yellow")
        return t
    elif swara.startswith("tivra "):
        note = swara[6:] + "\u266f"
        t = Text(note)
        t.stylize("bold magenta")
        return t
    elif swara == "SA":
        t = Text(swara)
        t.stylize("bold")
        return t
    return Text(swara)


def format_scale(swaras: list[str]) -> Text:
    result = Text()
    for i, swara in enumerate(swaras):
        if i > 0:
            result.append("  ")
        result.append_text(format_swara(swara))
    return result


TIME_LABELS = {
    "dawn": "Dawn",
    "morning": "Morning",
    "afternoon": "Afternoon",
    "evening": "Evening",
    "dusk": "Dusk",
    "night": "Night",
    "late night": "Late night",
    "midnight": "Midnight",
    "any": "Any time",
}

TIME_COLORS = {
    "dawn": "bright_yellow",
    "morning": "yellow",
    "afternoon": "bright_white",
    "evening": "orange3",
    "dusk": "dark_orange",
    "night": "blue",
    "late night": "dark_blue",
    "midnight": "medium_purple4",
    "any": "white",
}


def time_label(time: str) -> Text:
    label = TIME_LABELS.get(time, time.title())
    color = TIME_COLORS.get(time, "white")
    t = Text(label)
    t.stylize(color)
    return t
