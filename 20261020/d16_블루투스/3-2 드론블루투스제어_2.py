import bluetooth
import time
from machine import Pin, PWM
from ble_simple_peripheral import BLESimplePeripheral

# ===== 1. 모터 4개, 버튼 1개 =====
M1 = PWM(Pin(4), freq=10000, duty=0)
M2 = PWM(Pin(5), freq=10000, duty=0)
M3 = PWM(Pin(40), freq=10000, duty=0)
M4 = PWM(Pin(41), freq=10000, duty=0)

btn = Pin(0, Pin.IN, Pin.PULL_UP)   # 안 누르면 1, 누르면 0


# 모터 4개 세기를 한 번에 바꾸는 함수 (power: 0~100)
def motor(power):
    d = power * 10                  # duty 는 0~1023 이라서 10 을 곱한다
    M1.duty(d)
    M2.duty(d)
    M3.duty(d)
    M4.duty(d)


# ===== 2. 블루투스 =====
ble = bluetooth.BLE()
p = BLESimplePeripheral(ble, name='pyD_pjh')

command = ""                        # 폰이 보낸 글자를 적어 두는 곳

# 폰이 글자를 보내면 자동으로 실행되는 함수
def on_rx(data):
    global command
    command = data.decode().strip()

p.on_write(on_rx)


# ===== 3. 변수 =====
running = False     # 모터가 돌고 있나?
power = 20          # 지금 모터 세기
step = 3            # 한 번에 바뀌는 양 (+면 올라감, -면 내려감)
btn_last = 1        # 바로 전에 버튼 상태


# ===== 4. 반복 =====
try:
    while True:

        # (1) 폰 명령 확인
        if command == "1":
            running = True
            print("모터 시작")
            command = ""
        elif command == "2":
            running = False
            motor(0)
            print("모터 정지")
            command = ""

        # (2) 모터 세기 올렸다 내렸다
        if running:
            power = power + step
            if power >= 100:
                power = 100
                step = -3
            if power <= 20:
                power = 20
                step = 3
            motor(power)
            print(power)

        # (3) 버튼 누르면 폰에 알림
        now = btn.value()
        if btn_last == 1 and now == 0:
            print("버튼 눌림")
            if p.is_connected():
                p.send(b"btn pressed")
        btn_last = now

        time.sleep(0.1)             # 0.1초 쉬고 다시 처음부터

except KeyboardInterrupt:
    motor(0)                        # 멈출 때 모터도 끈다
    print("코드를 종료합니다.")