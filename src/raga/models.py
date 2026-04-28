from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, model_validator

VALID_TIMES = {
    "dawn",
    "morning",
    "afternoon",
    "evening",
    "dusk",
    "night",
    "late night",
    "midnight",
    "any",
}
VALID_TEMPOS = {"vilambit", "madhya", "drut"}


class Raga(BaseModel):
    name: str
    aliases: list[str] = []
    thaat: Optional[str] = None
    arohana: list[str]
    avarohana: list[str]
    vadi: str
    samvadi: str
    time: str
    mood: list[str] = []
    season: Optional[str] = None
    pakad: Optional[str] = None
    description: Optional[str] = None

    def matches(
        self,
        thaat: Optional[str] = None,
        time: Optional[str] = None,
        mood: Optional[str] = None,
        season: Optional[str] = None,
        include_any_time: bool = False,
    ) -> bool:
        if thaat and (self.thaat is None or self.thaat.lower() != thaat.lower()):
            return False
        if time:
            allowed = (time.lower(), "any") if include_any_time else (time.lower(),)
            if self.time.lower() not in allowed:
                return False
        if mood and mood.lower() not in [m.lower() for m in self.mood]:
            return False
        if season and (self.season is None or self.season.lower() != season.lower()):
            return False
        return True


@lru_cache(maxsize=1)
def load_ragas() -> list[Raga]:
    data_path = Path(__file__).parent / "data" / "ragas.json"
    with open(data_path) as f:
        data = json.load(f)
    return [Raga(**r) for r in data]


class Tala(BaseModel):
    name: str
    aliases: list[str] = []
    beats: int
    vibhags: list[int]
    theka: list[str]
    feel: list[str] = []
    tempo: list[str] = []
    description: Optional[str] = None

    def matches(
        self,
        beats: Optional[int] = None,
        feel: Optional[str] = None,
        tempo: Optional[str] = None,
    ) -> bool:
        if beats is not None and self.beats != beats:
            return False
        if feel and feel.lower() not in [f.lower() for f in self.feel]:
            return False
        if tempo and tempo.lower() not in [t.lower() for t in self.tempo]:
            return False
        return True

    @model_validator(mode='after')
    def check_beats_invariant(self) -> 'Tala':
        if len(self.theka) != self.beats:
            raise ValueError(
                f"theka has {len(self.theka)} bols but beats={self.beats}"
            )
        if sum(self.vibhags) != self.beats:
            raise ValueError(
                f"vibhags sum to {sum(self.vibhags)} but beats={self.beats}"
            )
        return self


@lru_cache(maxsize=1)
def load_talas() -> list[Tala]:
    data_path = Path(__file__).parent / "data" / "talas.json"
    with open(data_path) as f:
        data = json.load(f)
    return [Tala(**t) for t in data]
