from machine import Pin, PWM, Timer

btn = Pin(0, Pin.IN, Pin.PULL_UP)               # 누르면 0
flash = PWM(Pin(4), freq=1000, duty=0)          # 플래시 밝기 0~1023 (직시 금지)
red = Pin(33, Pin.OUT, value=1)                 # 빨간 LED: 0 이 켜짐

LEVELS = [0, 60, 250, 700]                      # 꺼짐, 약, 중, 강
NAMES = ["꺼짐", "약", "중", "강"]
state = 0                                       # 지금 몇 번째 단계인지
btn_last = 1                                    # 직전 버튼 값

# 인터럽트가 세우는 깃발
flag_10ms = False
isr_cnt = 0                                     # 인터럽트가 세는 ms

def timer_isr(t):
    global isr_cnt, flag_10ms
    isr_cnt += 1
    if isr_cnt % 10 == 0:
        flag_10ms = True
    if isr_cnt >= 1000:
        isr_cnt = 0
    # 깃발만 세우고 바로 빠져나간다

def task_10ms():
    global state, btn_last
    now = btn.value()
    if btn_last == 1 and now == 0:              # 눌린 순간만 잡는다
        state = (state + 1) % len(LEVELS)       # 0→1→2→3→0
        flash.duty(LEVELS[state])
        red.value(0 if state > 0 else 1)        # 켜져 있으면 빨간 LED 도 켠다
        print("단계", state, NAMES[state], "duty", LEVELS[state])
    btn_last = now

TASKS = [
    (10, task_10ms),
]

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_isr)

try:
    while True:
        # 메인은 깃발을 내리고 나서 일을 한다
        if flag_10ms:
            flag_10ms = False
            task_10ms()
except KeyboardInterrupt:
    tmr.deinit()
    flash.duty(0)
    flash.deinit()
    red.value(1)
    print("정지")

# ⭐ 도전: LEVELS 에 단계를 더 넣거나, 눈에 더 자연스러운 곡선(0, 15, 60, 250, 1023)으로 바꿔 보자.
