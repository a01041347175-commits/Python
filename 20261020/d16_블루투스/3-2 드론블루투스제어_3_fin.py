import bluetooth
import time
from machine import Pin, PWM
from ble_simple_peripheral import BLESimplePeripheral

M1 = PWM(Pin(4), freq=10000, duty=0)
M2 = PWM(Pin(5), freq=10000, duty=0)
M3 = PWM(Pin(40), freq=10000, duty=0)
M4 = PWM(Pin(41), freq=10000, duty=0)
 
def motor(power):
    duty = power                  
    M1.duty(duty)
    M2.duty(duty)
    M3.duty(duty)
    M4.duty(duty)

ble = bluetooth.BLE()
p = BLESimplePeripheral(ble, name='pyD_pjh')

command = ""                        

def on_rx(data):
    global command
    command = data.decode().strip()

p.on_write(on_rx)

running = False     
power = 20          
step = 3            
      
try:
    while True:
        
        if command == "1":
            running = True
            motor(80)
            print("모터 시작")
            command = ""
        elif command == "2":
            running = False
            motor(0)
            print("모터 정지")
            command = ""
            
        if running:
            power += step
            if power >= 100:
                power = 100
                step = -3
            if power <= 20:
                power = 20
                step = 3
            motor(power)
            print(power)

        time.sleep(0.1)             

except KeyboardInterrupt:
    motor(0)                        
    print("코드를 종료합니다.")
