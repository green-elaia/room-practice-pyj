from __future__ import annotations

from .models import Reservation
from .rules import validate
from .store import load_rooms, load_reservations, save_reservations, next_id


def reserve(room_id, title, date, start, end, booker, attendees, team="", phone=""):
    rooms = load_rooms()
    reservations = load_reservations()
    new = Reservation(
        id=next_id(reservations), room_id=room_id, title=title, booker=booker, team=team,
        phone=phone, date=date, start=start, end=end, attendees=attendees,
    )
    errors = validate(new, rooms, reservations)
    if errors:
        return None, errors
    reservations.append(new)
    save_reservations(reservations)
    return new, []


def list_reservations(date=None):
    reservations = load_reservations()
    if date:
        reservations = [r for r in reservations if r.date == date]
    return sorted(reservations, key=lambda r: (r.date, r.start, r.room_id))
