from __future__ import annotations

import json
from pathlib import Path

from .models import Room, Reservation

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_rooms(data_dir: Path = DATA_DIR) -> list[Room]:
    with open(data_dir / "rooms.json", encoding="utf-8") as f:
        return [Room(**r) for r in json.load(f)]


def load_reservations(data_dir: Path = DATA_DIR) -> list[Reservation]:
    with open(data_dir / "reservations.json", encoding="utf-8") as f:
        return [Reservation(**r) for r in json.load(f)]


def save_reservations(reservations: list[Reservation], data_dir: Path = DATA_DIR) -> None:
    with open(data_dir / "reservations.json", "w", encoding="utf-8") as f:
        json.dump([r.to_dict() for r in reservations], f, ensure_ascii=False, indent=2)
        f.write("\n")


def next_id(reservations: list[Reservation]) -> int:
    return max((r.id for r in reservations), default=0) + 1
