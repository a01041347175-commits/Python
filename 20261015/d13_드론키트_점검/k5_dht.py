# k5_dht.py — DHT11 온도·습도를 2초마다 세 번 읽고 스스로 끝난다
from machine import Pin
import time
import dht

dht11 = dht.DHT11(Pin(18))      # DHT11 신호선은 GPIO 18

for i in range(3):
    try:
        dht11.measure()
        print("온도:", dht11.temperature(), "C  습도:", dht11.humidity(), "%")
    except OSError:
        print("읽기 실패 — 이번 값은 건너뜁니다")
    time.sleep(2)

print("온습도 점검 끝")
