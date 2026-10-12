from machine import Pin, PWM, Timer
import time
import random

btn = Pin(0, Pin.IN, Pin.PULL_UP)               # 누르면 0
flash = PWM(Pin(4), freq=1000, duty=0)          # 플래시 (직시 금지)
red = Pin(33, Pin.OUT, value=1)                 # 0 이 켜짐

GO_DUTY = 600            # "지금!" 신호의 밝기
MIN_WAIT = 1000          # 랜덤 대기 최소(ms)
MAX_WAIT = 4000          # 랜덤 대기 최대(ms)
TOO_SLOW_MS = 3000       # 이 시간 안에 못 누르면 느림
RESULT_SHOW_MS = 1000    # 결과를 보여 주는 시간

IDLE = 0      # 대기: 버튼을 누르면 시작
READY = 1     # 준비: 빨간 LED 켜짐, 랜덤 시간 기다리는 중
GO = 2        # 플래시 켜짐: 지금 누르기
FOUL = 3      # 반칙: 빨간 LED 빠르게 깜빡
RESULT = 4    # 결과 보여 주는 중

state = IDLE
wait_ms = 0
t0 = 0                   # 상태가 시작된 시각
best = None              # 최고 기록(ms)
foul_cnt = 0
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

def start_round():
    global state, wait_ms, t0
    random.seed(time.ticks_ms())                   # 누른 시각으로 씨앗을 바꿔 매번 다르게
    wait_ms = random.randint(MIN_WAIT, MAX_WAIT)   # 1~4초 중 아무 때나
    t0 = time.ticks_ms()
    red.value(0)                                   # 준비 신호
    state = READY
    print("준비... 플래시가 켜지면 누르세요!")

def on_press():
    global state, t0, best, foul_cnt
    if state == IDLE:
        start_round()
    elif state == READY:                           # 너무 일찍 눌렀다
        flash.duty(0)
        foul_cnt = 0
        state = FOUL
        print("반칙! 너무 일찍 눌렀어요")
    elif state == GO:
        rt = time.ticks_diff(time.ticks_ms(), t0)  # 켜진 뒤 눌릴 때까지 걸린 시간
        print("반응 시간:", rt, "ms")
        if best is None or rt < best:
            best = rt
            print("★ 최고 기록 갱신!", best, "ms")
        else:
            print("최고 기록", best, "ms")
        t0 = time.ticks_ms()
        state = RESULT

def task_10ms():
    global state, t0, btn_last
    now = btn.value()
    if btn_last == 1 and now == 0:
        on_press()
    btn_last = now

    if state == READY and time.ticks_diff(time.ticks_ms(), t0) >= wait_ms:
        flash.duty(GO_DUTY)                        # 지금!
        red.value(1)
        t0 = time.ticks_ms()
        state = GO
    elif state == GO and time.ticks_diff(time.ticks_ms(), t0) >= TOO_SLOW_MS:
        flash.duty(0)
        state = IDLE
        print("너무 느려요. 다시 하려면 버튼")
    elif state == RESULT and time.ticks_diff(time.ticks_ms(), t0) >= RESULT_SHOW_MS:
        flash.duty(0)
        state = IDLE
        print("다시 하려면 버튼을 누르세요")

def task_100ms():
    global state, foul_cnt
    if state == FOUL:
        red.value(red.value() ^ 1)                 # 빠르게 깜빡
        foul_cnt += 1
        if foul_cnt >= 12:                         # 약 1.2초 깜빡이면 끝
            red.value(1)
            state = IDLE
            print("다시 하려면 버튼을 누르세요")

TASKS = [
    (10, task_10ms),
    (100, task_100ms),
]

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_isr)
print("반응속도 게임! 버튼을 누르면 시작")

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

# ⭐ 도전: 5판 평균을 내거나, 반칙을 3번 하면 게임 오버가 되게 만들어 보자.
