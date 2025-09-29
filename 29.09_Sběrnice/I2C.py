from machine import Pin, I2C
import time

# I2C0, SDA=GP0, SCL=GP1
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

# tlačítko na GP14
button = Pin(14, Pin.IN, Pin.PULL_UP)

# adresa slave (musí být stejná na obou)
SLAVE_ADDR = 0x42

while True:
    if button.value() == 0:   # stisknuto
        data = b'1'
    else:
        data = b'0'
    
    try:
        i2c.writeto(SLAVE_ADDR, data)
        print("Odesláno:", data)
    except Exception as e:
        print("Chyba I2C:", e)

    time.sleep(0.1)