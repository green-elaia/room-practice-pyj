from __future__ import annotations

from datetime import datetime

from .models import Room, Reservation

OPEN_TIME = "09:00"
CLOSE_TIME = "18:00"


def to_minutes(hhmm: str) -> int:
    t = datetime.strptime(hhmm, "%H:%M")
    return t.hour * 60 + t.minute


def validate(new: Reservation, rooms: list[Room], existing: list[Reservation]) -> list[str]:
    """새 예약에 문제가 있으면 오류 메시지 목록을 돌려준다. 문제가 없으면 빈 목록."""
    errors = []

    room_ids = [r.id for r in rooms]
    if new.room_id not in room_ids:
        errors.append(f"없는 회의실입니다: {new.room_id}")

    start = to_minutes(new.start)
    end = to_minutes(new.end)
    if start >= end:
        errors.append("끝나는 시간은 시작 시간보다 늦어야 합니다.")

    if start < to_minutes(OPEN_TIME) or end >= to_minutes(CLOSE_TIME):
        errors.append(f"운영 시간({OPEN_TIME}~{CLOSE_TIME}) 밖입니다.")

    if start % 30 != 0 or end % 30 != 0:
        errors.append("예약은 30분 단위로만 할 수 있습니다.")

    # TODO: 같은 회의실, 같은 날짜에 시간이 겹치는 예약은 막아야 한다 (현업 요청 1번)

    return errors
