# k4_oled.py — OLED 화면에 KIT OK 를 띄운다 (ssd1306.py 는 보드 안에 이미 있다)
from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C

i2c = SoftI2C(sda=Pin(43), scl=Pin(44))      # 화면과 말하는 선 두 개
print("I2C 주소 :", i2c.scan())              # 화면이 있으면 목록에 숫자가 나온다

oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)                                  # 화면 지우기
oled.text("KIT OK", 40, 28)                   # (x=40, y=28) 에 글자
oled.show()                                   # 지금까지 그린 것을 보여 준다
print("OLED 점검 끝")
