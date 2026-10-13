# 보드에 쌓인 인지능력 검사 기록을 읽어 보여 준다 (보드를 PC 에 연결한 뒤 실행)
LOG_FILE = "cog_log.txt"
BEST_FILE = "best.txt"

try:
    with open(LOG_FILE) as f:
        rows = [int(line) for line in f.read().split()]
except OSError:
    rows = []

passed = [ms for ms in rows if ms >= 0]      # 통과한 것은 반응 시간(ms)
failed = len(rows) - len(passed)             # 실패는 -1

if len(rows) == 0:
    print("아직 저장된 기록이 없습니다. g4 를 main.py 로 저장하고 몇 번 검사해 보세요.")
else:
    print("검사 횟수 :", len(rows), "번  (통과", len(passed), "· 실패", failed, ")")
    if len(passed) > 0:
        print("가장 빠름 :", min(passed), "ms")
        print("평균      :", sum(passed) // len(passed), "ms")
    print("최근 10번 :", rows[-10:], "  (-1 은 실패)")

try:
    with open(BEST_FILE) as f:
        print("best.txt  :", f.read(), "ms")
except OSError:
    print("best.txt  : 없음")
