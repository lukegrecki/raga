from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, model_validator


class Raga(BaseModel):
    name: str
    aliases: list[str] = []
    thaat: str
    arohana: list[str]
    avarohana: list[str]
    vadi: str
    samvadi: str
    time: str
    mood: list[str] = []
    season: Optional[str] = None
    pakad: Optional[str] = None
    description: Optional[str] = None


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
