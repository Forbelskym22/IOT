import time
from machine import Pin, PWM
 
# Vytvoříme PWM objekty pro piny 15, 14 a 13
pwm15 = PWM(Pin(15))
pwm14 = PWM(Pin(14))
pwm13 = PWM(Pin(13))
 
# Nastavíme stejnou frekvenci pro všechny
for pwm in (pwm15, pwm14, pwm13):
    pwm.freq(1000)
 
def blik(pwms):
    duty = 0
    direction = 1
    for _ in range(8 * 256):
        duty += direction
        if duty > 255:
            duty = 255
            direction = -1
        elif duty < 0:
            duty = 0
            direction = 1
        # Nastavíme stejný duty pro všechny PWM
        for pwm in pwms:
            pwm.duty_u16(duty * duty)
        time.sleep(0.001)
 
# Zavoláme funkci s listem PWM objektů
blik([pwm15, pwm14, pwm13])