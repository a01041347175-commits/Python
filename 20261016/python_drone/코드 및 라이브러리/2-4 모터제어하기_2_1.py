from machine import Pin, PWM, Timer
import time

M1_motor = PWM(Pin(4), freq = 10000 ,duty=0)
M2_motor = PWM(Pin(5), freq = 10000 ,duty=0)
M3_motor = PWM(Pin(40), freq = 10000 ,duty=0)
M4_motor = PWM(Pin(41), freq = 10000 ,duty=0)

flag = False
isr_cnt = 0

duty = 0
direction = 3

last_print = time.ticks_ms()

def timer_isr(t):
    global flag
    flag = True
    
timer = Timer(0)
timer.init(period=100, mode=Timer.PERIODIC, callback=timer_isr)

try:
    while True:
        if flag == True :
            flag = False
            duty += direction
            
        if duty >= 100:
            duty = 100
            direction = -3
        elif duty <= 20 and direction == -3:
            duty = 20
            direction = 3
        
        M1_motor.duty(duty)
        M2_motor.duty(duty)
        M3_motor.duty(duty)
        M4_motor.duty(duty)
        
        now = time.ticks_ms()
        if time.ticks_diff(now, last_print) >= 1000:
            print(duty)
            last_print = now
        
        time.sleep_ms(1)
        
except KeyboardInterrupt:
    print("코드를 종료합니다.")

finally:
    timer.deinit()
    M1_motor.duty(0)
    M2_motor.duty(0)
    M3_motor.duty(0)
    M4_motor.duty(0)
    
    M1_motor.deinit()
    M2_motor.deinit()
    M3_motor.deinit()
    M4_motor.deinit()
    


