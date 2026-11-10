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


def test_같은_회의실과_날짜의_시간이_겹치면_막는다():
    existing = make(start="10:30", end="11:30")
    errors = validate(make(), ROOMS, [existing])
    assert "이미 예약된 시간입니다." in errors


def test_예약_시간이_기존_예약에_포함되면_막는다():
    existing = make(start="09:30", end="12:00")
    errors = validate(make(), ROOMS, [existing])
    assert "이미 예약된 시간입니다." in errors


def test_기존_예약_시간이_새_예약에_포함되면_막는다():
    existing = make(start="10:30", end="11:30")
    errors = validate(make(start="10:00", end="12:00"), ROOMS, [existing])
    assert "이미 예약된 시간입니다." in errors


def test_새_예약이_기존_예약을_완전히_감싸면_막는다():
    existing = make(start="10:00", end="11:00")
    errors = validate(make(start="09:30", end="11:30"), ROOMS, [existing])
    assert "이미 예약된 시간입니다." in errors


def test_기존_예약_종료와_새_예약_시작이_맞닿으면_허용한다():
    existing = make(start="09:00", end="10:00")
    assert validate(make(start="10:00", end="11:00"), ROOMS, [existing]) == []


def test_새_예약_종료와_기존_예약_시작이_맞닿으면_허용한다():
    existing = make(start="11:00", end="12:00")
    assert validate(make(start="10:00", end="11:00"), ROOMS, [existing]) == []


def test_다른_회의실의_예약과는_겹치지_않는다():
    other_room = Room(id="R2", name="소회의실 B", capacity=4, floor=3)
    existing = make(room_id="R2")
    assert validate(make(), ROOMS + [other_room], [existing]) == []


def test_다른_날짜의_예약과는_겹치지_않는다():
    existing = make(date="2026-11-11")
    assert validate(make(), ROOMS, [existing]) == []


def test_겹치는_기존_예약이_여러_건이어도_오류는_한_번만_추가한다():
    existing = [make(id=2), make(id=3, start="10:30", end="11:30")]
    errors = validate(make(), ROOMS, existing)
    assert errors.count("이미 예약된 시간입니다.") == 1


def test_정원을_넘으면_막는다():
    errors = validate(make(attendees=5), ROOMS, [])
    assert "정원을 넘었습니다." in errors


def test_정원과_같은_인원은_허용한다():
    assert validate(make(attendees=4), ROOMS, []) == []
