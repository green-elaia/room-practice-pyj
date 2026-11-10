from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class Room:
    id: str
    name: str
    capacity: int
    floor: int


@dataclass
class Reservation:
    id: int
    room_id: str
    title: str
    booker: str
    team: str
    phone: str
    date: str  # "2026-11-10"
    start: str  # "10:00"
    end: str  # "11:00"
    attendees: int

    def to_dict(self) -> dict:
        return asdict(self)
