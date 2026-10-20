import bluetooth
import time
from machine import Pin, PWM, Timer
from ble_simple_peripheral import BLESimplePeripheral   # 보드에 업로드돼 있어야 하는 파일

# ---------------- 하드웨어 ----------------
motors = [PWM(Pin(n), freq=10000, duty=0) for n in (4, 5, 40, 41)]
btn = Pin(0, Pin.IN, Pin.PULL_UP)        # 보드 BOOT 버튼 (보드에 맞게 핀 번호 확인)

def set_all(pct):
    """0~100(%) 를 ESP32 PWM 범위 0~1023 으로 바꿔서 4개 모터에 적용"""
    d = int(pct * 1023 / 100)
    for m in motors:
        m.duty(d)

# ---------------- BLE ----------------
ble = bluetooth.BLE()
p = BLESimplePeripheral(ble, name='pyD_pjh')   # 서비스 등록·광고·재연결은 이 클래스가 처리

command = ""            # 폰이 보낸 글자를 적어 두는 포스트잇

def on_rx(data):
    global command
    command = data.decode().strip()

p.on_write(on_rx)

def send(msg):
    print(msg)
    if p.is_connected():
        p.send(msg.encode())   # 기본 MTU 에서는 20바이트까지만 전송됨 (한글 1자 = 3바이트)

# ---------------- 타이머 ----------------
flag = False
isr_cnt = 0

def timer_isr(t):
    global isr_cnt, flag
    isr_cnt += 1
    if isr_cnt % 10 == 0:      # 100ms x 10 = 1초마다
        flag = True
    if isr_cnt >= 1000:
        isr_cnt = 0

tim = Timer(0)
tim.init(period=100, mode=Timer.PERIODIC, callback=timer_isr)

# ---------------- 상태 ----------------
running = False
duty = 20
direction = 3
last_print = time.ticks_ms()
btn_last = 1

def task():
    global command, running, duty, direction, last_print

    if command:                         # 폰에서 온 명령 처리
        if command == "1":
            running = True
            send("motor start")
        elif command == "2":
            running = False
            set_all(0)
            send("motor stop")
        command = ""

    if running:                         # 20% <-> 100% 왕복 램프
        duty += direction
        if duty >= 100:
            duty = 100
            direction = -3
        elif duty <= 20:
            duty = 20
            direction = 3
        set_all(duty)

        now = time.ticks_ms()
        if time.ticks_diff(now, last_print) >= 1000:
            print(duty)
            last_print = now

# ---------------- 메인 루프 ----------------
try:
    while True:
        if flag:
            flag = False
            task()

        now = btn.value()               # 버튼은 매 루프마다 확인해야 눌림을 놓치지 않음
        if btn_last == 1 and now == 0:
            send("btn pressed")
        btn_last = now

        time.sleep_ms(10)
except KeyboardInterrupt:
    print("코드를 종료합니다.")
finally:
    tim.deinit()
    set_all(0)
    for m in motors:
        m.deinit()