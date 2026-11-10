from booking.models import Room, Reservation
from booking.rules import validate

ROOMS = [Room(id="R1", name="소회의실 A", capacity=4, floor=3)]


def make(**kw):
    base = dict(id=1, room_id="R1", title="회의", booker="김민수", team="기획팀", phone="",
                date="2026-11-10", start="10:00", end="11:00", attendees=3)
    base.update(kw)
    return Reservation(**base)


def test_정상_예약은_통과한다():
    assert validate(make(), ROOMS, []) == []


def test_없는_회의실은_막는다():
    assert "없는 회의실입니다: R9" in validate(make(room_id="R9"), ROOMS, [])


def test_끝이_시작보다_빠르면_막는다():
    errors = validate(make(start="11:00", end="10:00"), ROOMS, [])
    assert "끝나는 시간은 시작 시간보다 늦어야 합니다." in errors


def test_운영_시간_전에_시작하면_막는다():
    errors = validate(make(start="08:00", end="09:00"), ROOMS, [])
    assert "운영 시간(09:00~18:00) 밖입니다." in errors
