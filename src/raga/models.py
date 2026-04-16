from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


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
