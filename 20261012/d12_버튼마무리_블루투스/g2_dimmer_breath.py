from machine import Pin, PWM, Timer
import time

btn = Pin(0, Pin.IN, Pin.PULL_UP)               # 누르면 0
flash = PWM(Pin(4), freq=1000, duty=0)          # 플래시 (직시 금지)
red = Pin(33, Pin.OUT, value=1)                 # 켜져 있으면 빨간 LED 도 켠다

LONG_MS = 500          # 이 시간 이상 누르면 "길게 누름"
MIN_DUTY = 20          # 가장 어두운 값
MAX_DUTY = 700         # 가장 밝은 값
FADE_STEP = 8          # 10ms 마다 바뀌는 크기

level = 300            # 켜졌을 때의 밝기
is_on = False          # 켜짐/꺼짐
fade_dir = 1           # +1 밝아짐, -1 어두워짐
long_started = False   # 이번 누름이 길게 누름으로 넘어갔는지
press_start = 0        # 누르기 시작한 시각
btn_last = 1

flag_10ms = False
isr_cnt = 0

def timer_isr(t):
    global isr_cnt, flag_10ms
    isr_cnt += 1
    if isr_cnt % 10 == 0:
        flag_10ms = True
    if isr_cnt >= 1000:
        isr_cnt = 0

def apply():
    flash.duty(level if is_on else 0)
    red.value(0 if is_on else 1)

def task_10ms():
    global btn_last, press_start, long_started, is_on, level, fade_dir
    now = btn.value()
    if btn_last == 1 and now == 0:                       # 막 눌렀다
        press_start = time.ticks_ms()
        long_started = False
    elif now == 0:                                       # 계속 누르는 중
        held = time.ticks_diff(time.ticks_ms(), press_start)
        if held >= LONG_MS:
            if not long_started:                         # 길게 누름이 시작되는 순간
                long_started = True
                is_on = True
                print("길게 누름 시작, 방향", fade_dir)
            level += FADE_STEP * fade_dir
            if level >= MAX_DUTY:                        # 끝에 닿으면 방향을 뒤집는다
                level = MAX_DUTY
                fade_dir = -1
            if level <= MIN_DUTY:
                level = MIN_DUTY
                fade_dir = 1
            apply()
    elif btn_last == 0 and now == 1:                     # 막 뗐다
        held = time.ticks_diff(time.ticks_ms(), press_start)
        if long_started:                                 # 길게 눌렀다 뗌: 지금 밝기로 고정
            fade_dir = -fade_dir                         # 다음 번엔 반대 방향
            print("고정 level", level)
        else:                                            # 짧게 누름: 토글
            is_on = not is_on
            apply()
            print("짧게", held, "ms → ", "켜짐" if is_on else "꺼짐", "level", level)
    btn_last = now

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_isr)

try:
    while True:
        if flag_10ms:
            flag_10ms = False
            task_10ms()
except KeyboardInterrupt:
    tmr.deinit()
    flash.duty(0)
    flash.deinit()
    red.value(1)
    print("정지")

# ⭐ 도전: 오래 누를수록 FADE_STEP 이 점점 커지게(가속) 만들어 보자.
