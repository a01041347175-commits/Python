# k1_led.py — 42번 핀의 LED 를 세 번 깜빡이고 스스로 끝난다
from machine import Pin
import time

led = Pin(42, Pin.OUT)      # 42번 핀을 '내보내기' 로 쓴다

for i in range(3):
    led.value(1)
    print("LED 켬", i + 1, "/ 3")
    time.sleep(0.5)
    led.value(0)
    print("LED 끔")
    time.sleep(0.5)

print("LED 점검 끝")
