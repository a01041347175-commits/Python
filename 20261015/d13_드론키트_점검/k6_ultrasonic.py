# k6_ultrasonic.py — 초음파 센서로 거리를 다섯 번 재고 스스로 끝난다
import machine
import time
from machine import Pin

trigger = Pin(17, mode=Pin.OUT, pull=None)   # 소리를 쏘라는 신호
echo = Pin(1, mode=Pin.IN, pull=None)        # 돌아온 소리 신호
trigger.value(0)

for i in range(5):
    trigger.value(0)
    time.sleep_us(5)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)
    pulse_time = machine.time_pulse_us(echo, 1, 30000)
    distance_cm = (pulse_time / 2) / 29.1
    if 2 <= distance_cm <= 200:
        print(round(distance_cm, 1), "cm")
    else:
        print("범위 밖 — 센서 앞에 손을 20cm 쯤 두세요")
    time.sleep(0.5)

print("초음파 점검 끝")
