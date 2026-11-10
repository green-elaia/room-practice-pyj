# 예전 담당자가 만든 이용률 보고서. 동작은 하지만 아무도 손대고 싶어 하지 않는다.
def usage_report(reservations, rooms):
    result = {}
    for rm in rooms:
        t = 0
        c = 0
        for r in reservations:
            if r.room_id == rm.id:
                if r.start and r.end:
                    a = int(r.start[:2]) * 60 + int(r.start[3:])
                    b = int(r.end[:2]) * 60 + int(r.end[3:])
                    if b > a:
                        t = t + (b - a)
                        c = c + 1
                    else:
                        pass
                else:
                    pass
        if c > 0:
            if t / 60 > 6:
                lv = "높음"
            else:
                if t / 60 > 2:
                    lv = "보통"
                else:
                    lv = "낮음"
        else:
            lv = "없음"
        result[rm.name] = {"건수": c, "시간": round(t / 60, 1), "이용률": lv}
    return result
