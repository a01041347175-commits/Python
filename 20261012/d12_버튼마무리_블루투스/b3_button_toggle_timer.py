from machine import Pin, Timer

btn = Pin(0, Pin.IN, Pin.PULL_UP)
flash = Pin(4, Pin.OUT, value=0)     # 플래시: 매우 밝다, 직시 금지
red = Pin(33, Pin.OUT, value=1)

time_cnt = 0
ms_flag = False
btn_last = 1
red_start = 0

def timer_callback(t): # ISR
    global ms_flag
    ms_flag = True

def task_10ms():
    global btn_last, red_start
    now = btn.value()
    if btn_last == 1 and now == 0:   # 뗀 상태에서 누른 상태로 바뀐 순간
        red_start = 1
        flash.value(flash.value() ^ 1)
        print("버튼 눌림 → 플래시 토글")
    btn_last = now

def task_500ms():
    if red_start == 1:
        red.value(red.value() ^ 1)       # 버튼과 상관없이 계속 깜빡

TASKS = [
    (10, task_10ms),
    (500, task_500ms),
]
CYCLE = 1000

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            for period, task in TASKS:
                if time_cnt % period == 0:
                    task()

            if time_cnt >= CYCLE:
                time_cnt = 0
except KeyboardInterrupt:
    tmr.deinit()
    flash.value(0)
    red.value(1)
    print("타이머 정지")
