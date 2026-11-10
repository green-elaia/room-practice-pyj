# 회의실 예약 서비스

사내 회의실을 예약하고, 예약 현황판을 웹페이지로 보여 주는 서비스입니다.

## 실행

```bash
python -m booking list
python -m booking add --room R1 --title "주간 회의" --date 2026-11-10 --start 10:00 --end 11:00 --booker 김민수 --attendees 3
python build_site.py
```

## 테스트

```bash
python -m pytest
```
