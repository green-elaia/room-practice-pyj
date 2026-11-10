import argparse

from .report import usage_report
from .service import list_reservations, reserve
from .store import load_rooms, load_reservations


def main():
    parser = argparse.ArgumentParser(prog="python -m booking", description="회의실 예약")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="예약 목록 보기")
    p_list.add_argument("--date", help="이 날짜의 예약만 보기 (예: 2026-11-10)")

    p_add = sub.add_parser("add", help="예약하기")
    p_add.add_argument("--room", required=True, help="회의실 ID (R1~R4)")
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--date", required=True)
    p_add.add_argument("--start", required=True)
    p_add.add_argument("--end", required=True)
    p_add.add_argument("--booker", required=True)
    p_add.add_argument("--attendees", type=int, required=True)
    p_add.add_argument("--team", default="")
    p_add.add_argument("--phone", default="")

    sub.add_parser("rooms", help="회의실 목록 보기")
    sub.add_parser("report", help="회의실 이용률 보고서")

    args = parser.parse_args()

    if args.command == "list":
        for r in list_reservations(args.date):
            print(f"#{r.id} {r.date} {r.start}~{r.end} {r.room_id} {r.title} ({r.booker}, {r.attendees}명)")
    elif args.command == "add":
        new, errors = reserve(args.room, args.title, args.date, args.start, args.end,
                              args.booker, args.attendees, args.team, args.phone)
        if errors:
            print("[예약 실패]")
            for e in errors:
                print(" -", e)
        else:
            print(f"[예약 완료] #{new.id} {new.date} {new.start}~{new.end} {new.room_id} {new.title}")
    elif args.command == "rooms":
        for rm in load_rooms():
            print(f"{rm.id} {rm.name} ({rm.capacity}명, {rm.floor}층)")
    elif args.command == "report":
        for name, row in usage_report(load_reservations(), load_rooms()).items():
            print(name, row)


if __name__ == "__main__":
    main()
