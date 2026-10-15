# k3_buzzer.py — 부저로 도·미·솔 세 음을 한 번씩 내고 스스로 끝난다
from machine import Pin, PWM
import time

buzzer = PWM(Pin(6), freq=440, duty=0)   # 부저는 GPIO 6, 소리 없이 시작

try:
    for name, freq in (("도", 523), ("미", 659), ("솔", 784)):
        buzzer.freq(freq)        # 소리 높이
        buzzer.duty(100)         # 소리 크기(작게)
        print("삐 —", name, freq, "Hz")
        time.sleep_ms(400)
        buzzer.duty(0)
        time.sleep_ms(150)
finally:
    buzzer.duty(0)
    buzzer.deinit()
    print("부저 점검 끝")
