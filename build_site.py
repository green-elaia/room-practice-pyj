"""예약 데이터로 예약 현황판 웹페이지(site/index.html)를 만든다."""
from pathlib import Path

from booking.store import load_rooms, load_reservations

OUT = Path(__file__).resolve().parent / "site" / "index.html"


def build():
    rooms = {r.id: r for r in load_rooms()}
    reservations = sorted(load_reservations(), key=lambda r: (r.date, r.start, r.room_id))

    rows = ""
    for r in reservations:
        room = rooms.get(r.room_id)
        room_name = room.name if room else r.room_id
        rows += f"""
        <tr>
          <td>{r.date}</td><td>{r.start}~{r.end}</td><td>{room_name}</td>
          <td>{r.title}</td><td>{r.booker} ({r.team})</td><td>{r.phone}</td><td>{r.attendees}명</td>
        </tr>"""

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>회의실 예약 현황</title>
<style>
  body {{ font-family: "Apple SD Gothic Neo", "Malgun Gothic", sans-serif; margin: 32px; color: #1a1a1a; }}
  h1 {{ font-size: 24px; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border-bottom: 1px solid #ddd; padding: 8px 10px; text-align: left; }}
  th {{ background: #f5c43d; }}
</style>
</head>
<body>
<h1>회의실 예약 현황</h1>
<p>예약 {len(reservations)}건</p>
<table>
  <tr><th>날짜</th><th>시간</th><th>회의실</th><th>회의</th><th>예약자</th><th>연락처</th><th>인원</th></tr>{rows}
</table>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"[완료] {OUT.relative_to(Path.cwd()) if OUT.is_relative_to(Path.cwd()) else OUT} 에 예약 {len(reservations)}건을 썼습니다.")


if __name__ == "__main__":
    build()
