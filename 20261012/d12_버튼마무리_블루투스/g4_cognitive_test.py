from machine import Pin, PWM, Timer
import time
import random

btn = Pin(0, Pin.IN, Pin.PULL_UP)               # 누르면 0
flash = PWM(Pin(4), freq=1000, duty=0)          # 플래시 (직시 금지)
red = Pin(33, Pin.OUT, value=1)                 # 0 이 켜짐

# ───── ★ 고쳐 쓰는 값: 이 칸의 숫자만 바꾸면 된다 ─────
LIMIT_MS = 500           # 이 시간(0.5초) 안에 눌러야 통과
GO_DUTY = 600            # "지금!" 신호의 밝기 (0~1023)
PASS_DUTY = 80           # 통과 때 불의 밝기: 어둡게
FAIL_DUTY = 600          # 실패 때 불의 밝기: 밝게

# 깜빡임 모양: 한 칸 = 100ms, 1 = 켜짐, 0 = 꺼짐. 끝까지 읽으면 처음으로 돌아가 계속 반복
PASS_PATTERN = [1, 1, 0, 0,   1, 1, 0, 0,   0, 0, 0, 0]                       # 두 번 깜빡 · 쉬고
FAIL_PATTERN = [1, 1, 1, 1, 1, 1,   0, 0,   1, 0, 1, 0, 1, 0,   0, 0, 0, 0]   # 길게 한 번 · 짧게 세 번 · 쉬고

MIN_WAIT = 1000          # 랜덤 대기 최소(ms)
MAX_WAIT = 4000          # 랜덤 대기 최대(ms)
# ───── 여기까지 ─────

PRESS_LOCK_MS = 100      # 버튼을 누른 뒤 이 시간 동안은 또 눌린 것으로 치지 않는다 (떨림 방지)
BEST_FILE = "best.txt"           # 통과한 것 중 가장 빠른 기록 (플래시 메모리)
LOG_FILE = "cog_log.txt"         # 검사 결과를 한 줄씩 쌓는 파일 (통과 ms, 실패 -1)

IDLE = 0      # 키 입력 대기: 버튼을 누르면 검사 시작
READY = 1     # 준비: 빨간 LED 켜짐, 랜덤 시간 기다리는 중
GO = 2        # 플래시 켜짐: LIMIT_MS 안에 누르기
FOUL = 3      # 반칙: 빨간 LED 빠르게 깜빡
PASS = 4      # 통과: PASS_PATTERN 대로 PASS_DUTY 로 계속 깜빡 (버튼을 누를 때까지)
FAIL = 5      # 실패: FAIL_PATTERN 대로 FAIL_DUTY 로 계속 깜빡 (버튼을 누를 때까지)

state = IDLE
wait_ms = 0
t0 = 0                   # 상태가 시작된 시각
best = None              # 통과 기록 중 가장 빠른 것(ms)
blink_cnt = 0            # 깜빡임 단계 세기
foul_cnt = 0             # 반칙 깜빡임 횟수
last_press = 0           # 마지막으로 인정한 버튼 누름 시각
btn_last = 1

flag_10ms = False
flag_100ms = False
isr_cnt = 0

def timer_isr(t):
    global isr_cnt, flag_10ms, flag_100ms
    isr_cnt += 1
    if isr_cnt % 10 == 0:
        flag_10ms = True
    if isr_cnt % 100 == 0:
        flag_100ms = True
    if isr_cnt >= 1000:
        isr_cnt = 0

def load_best():
    try:
        with open(BEST_FILE) as f:         # 파일이 있으면 읽어서
            return int(f.read())
    except (OSError, ValueError):          # 처음이라 파일이 없거나 내용이 이상하면
        return None                        # 기록 없음

def save_best(ms):
    with open(BEST_FILE, "w") as f:        # "w": 새로 쓰기 (옛 내용은 지워짐)
        f.write(str(ms))

def log_result(ms):
    with open(LOG_FILE, "a") as f:         # "a": 맨 끝에 덧붙이기
        f.write(str(ms) + "\n")

best = load_best()                         # 전원을 켤 때마다 지난 기록을 불러온다

def start_round():
    global state, wait_ms, t0
    random.seed(time.ticks_ms())                   # 누른 시각으로 씨앗을 바꿔 매번 다르게
    wait_ms = random.randint(MIN_WAIT, MAX_WAIT)   # 1~4초 중 아무 때나
    t0 = time.ticks_ms()
    red.value(0)                                   # 준비 신호
    state = READY
    print("준비... 플래시가 켜지면", LIMIT_MS, "ms 안에 누르세요!")

def finish_pass(rt):
    global state, best, blink_cnt
    print("통과! 반응 시간:", rt, "ms")
    log_result(rt)                                 # 통과 기록을 파일 끝에 한 줄
    if best is None or rt < best:
        best = rt
        save_best(best)                            # 최고 기록일 때만 다시 쓴다
        print("★ 최고 기록 갱신!", best, "ms")
    flash.duty(0)
    blink_cnt = 0
    state = PASS

def finish_fail():
    global state, blink_cnt
    print("실패!", LIMIT_MS, "ms 안에 못 눌렀어요")
    log_result(-1)                                 # 실패는 -1 로 적는다
    flash.duty(0)
    blink_cnt = 0
    state = FAIL

def on_press():
    global state, foul_cnt
    if state == IDLE or state == PASS or state == FAIL:   # 대기·통과·실패 어디서든 누르면 새로 도전
        flash.duty(0)
        red.value(1)
        start_round()
    elif state == READY:                           # 너무 일찍 눌렀다
        flash.duty(0)
        foul_cnt = 0
        state = FOUL
        print("반칙! 너무 일찍 눌렀어요")
    elif state == GO:
        rt = time.ticks_diff(time.ticks_ms(), t0)  # 켜진 뒤 눌릴 때까지 걸린 시간
        if rt < LIMIT_MS:
            finish_pass(rt)
        else:
            finish_fail()

def task_10ms():
    global state, t0, btn_last, last_press
    now = btn.value()
    if btn_last == 1 and now == 0:
        if time.ticks_diff(time.ticks_ms(), last_press) >= PRESS_LOCK_MS:
            last_press = time.ticks_ms()
            on_press()
    btn_last = now

    if state == READY and time.ticks_diff(time.ticks_ms(), t0) >= wait_ms:
        flash.duty(GO_DUTY)                        # 지금!
        red.value(1)
        t0 = time.ticks_ms()
        state = GO
    elif state == GO and time.ticks_diff(time.ticks_ms(), t0) >= LIMIT_MS:
        finish_fail()                              # 0.5초가 지났다

def task_100ms():
    global state, foul_cnt, blink_cnt
    if state == FOUL:
        red.value(red.value() ^ 1)                 # 빠르게 깜빡
        foul_cnt += 1
        if foul_cnt >= 12:                         # 약 1.2초 깜빡이면 끝
            red.value(1)
            state = IDLE
            print("다시 하려면 버튼을 누르세요")
    elif state == PASS:                            # 어두운 불: 두 번 깜빡 · 쉬고 · 계속
        on = PASS_PATTERN[blink_cnt % len(PASS_PATTERN)]
        flash.duty(PASS_DUTY if on else 0)
        blink_cnt += 1                             # 버튼을 누를 때까지 계속 반복
    elif state == FAIL:                            # 밝은 불: 길게 한 번 · 짧게 세 번 · 계속
        on = FAIL_PATTERN[blink_cnt % len(FAIL_PATTERN)]
        flash.duty(FAIL_DUTY if on else 0)
        blink_cnt += 1                             # 버튼을 누를 때까지 계속 반복

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_isr)
print("인지능력 검사기! 저장된 최고 기록:", best)
print("버튼을 누르면 시작")

try:
    while True:
        if flag_10ms:
            flag_10ms = False
            task_10ms()
        if flag_100ms:
            flag_100ms = False
            task_100ms()
except KeyboardInterrupt:
    tmr.deinit()
    flash.duty(0)
    flash.deinit()
    red.value(1)
    print("정지. 최고 기록:", best)

# ⭐ 도전: LIMIT_MS 를 300 으로 줄여 보자. 실패 횟수가 세 번이 되면 검사 종료로 만들어 보자.
