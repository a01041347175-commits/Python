from machine import Pin, Timer

btn = Pin(0, Pin.IN, Pin.PULL_UP)       # 누르면 0
flash = Pin(4, Pin.OUT, value=0)        # 플래시: 매우 밝다, 직시 금지

DEBOUNCE_MS = 70    # 값(0 이든 1 이든)이 이 시간 동안 안 바뀌어야 "진짜 바뀜" 으로 인정 (10 의 배수로 바꿔 보자)
CHECK_MS = 10       # 버튼을 확인하는 간격
MAX_HOLD_MS = 5000      # 심화 : 0 (눌림) 이 이 시간 이상 이어지면 무효 (눌린 채 걸림 · 고장 방어)

raw_last = 1        # 직전에 읽은 값 (떨림 포함)
stable = 1          # 인정된 값: 1 = 뗌, 0 = 눌림 (0 도 1 도 70ms 안정돼야 바뀐다)
same_ms = 0         # 값이 바뀌지 않고 이어진 시간 (ms)
raw_changes = 0     # 값이 바뀐 횟수 (떨림도 센다)
presses = 0         # 인정된 눌림 횟수 (1 → 0 → 1 한 바퀴가 끝났을 때 센다)
held_ms = 0         # 심화 : 눌림이 확정된 뒤 0 이 이어진 시간 (ms)
invalid = 0         # 심화 : 너무 오래 눌러서 무효로 만든 횟수

# 인터럽트가 세우는 깃발
flag_10ms = False
isr_cnt = 0

def timer_isr(t):
    global isr_cnt, flag_10ms
    isr_cnt += 1
    if isr_cnt % CHECK_MS == 0:
        flag_10ms = True
    if isr_cnt >= 1000:
        isr_cnt = 0
    # 깃발만 세우고 바로 빠져나간다

def task_10ms():
    global raw_last, stable, same_ms, raw_changes, presses, held_ms, invalid
    now = btn.value()
    if now != raw_last:                 # 값이 바뀌었다 → 떨림일 수 있으니 시간을 처음부터 잰다
        raw_changes += 1
        raw_last = now
        same_ms = 0
        return
    same_ms += CHECK_MS                 # 같은 값이 이어지면 안정된 시간이 쌓인다
    if stable == 0:                     # 심화 : 눌림이 확정된 뒤로 0 이 이어진 시간을 센다
        held_ms += CHECK_MS
    if same_ms >= DEBOUNCE_MS and now != stable:   # 충분히 안정됐고 인정된 값과 다르면
        stable = now                    # 이제야 인정한다 (0 도 1 도 똑같이 기다린다)
        if stable == 0:                 # 1 → 0 : 눌림이 확정됐다. 아직 한 바퀴가 안 끝났다
            held_ms = 0
            print("누름 확정 (뗄 때까지 기다린다)")
        elif held_ms >= MAX_HOLD_MS:        # 0 → 1 이지만 너무 오래 눌렀다 → 무효
            invalid += 1
            print("너무 오래 눌러서 무효", held_ms, "ms")
        else:                           # 0 → 1 : 뗌까지 확정 → 1 → 0 → 1 한 바퀴 완성
            presses += 1
            flash.value(flash.value() ^ 1)
            print("눌림 인정", presses, "번 / 값이 바뀐 횟수", raw_changes)

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
    flash.value(0)
    print("정지. 인정된 눌림", presses, "번 / 무효", invalid, "번 / 값이 바뀐 횟수", raw_changes)

# 심화 정답 : 5초(5000ms) 이상 누르고 있다 떼면 플래시를 토글하지 않고 '무효' 로 센다.
