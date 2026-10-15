# k2_battery.py — 배터리 전압을 1초마다 다섯 번 읽고 스스로 끝난다
from machine import Pin, ADC
import time

adc = ADC(Pin(2))            # 2번 핀의 전압을 숫자로 읽는다

for i in range(5):
    raw = adc.read()                                  # 0 ~ 4095
    voltage = raw / 4095 * 5.02 * 0.96                # 전압(V)
    percent = (voltage - 3.0) / (4.25 - 3.0) * 100    # 잔량(%)
    print("raw", raw, "| 전압", round(voltage, 2), "V | 잔량", round(percent), "%")
    time.sleep(1.0)

print("배터리 점검 끝")
