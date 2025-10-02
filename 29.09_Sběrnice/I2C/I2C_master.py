from machine import Pin, I2C
import time

class Button:
    def __init__(self, pin_num, pull=Pin.PULL_UP, debounce_ms=50):
        self.pin = Pin(pin_num, Pin.IN, pull)
        self.debounce_ms = debounce_ms
        self.last_state = self.pin.value()
        self.last_time = time.ticks_ms()

    def is_pressed(self):
        """Vrátí True jen při stisku (detekce změny)"""
        current_state = self.pin.value()
        now = time.ticks_ms()

        # debounce kontrola
        if current_state != self.last_state:
            if time.ticks_diff(now, self.last_time) > self.debounce_ms:
                self.last_state = current_state
                self.last_time = now
                if current_state == 0:
                    return True
        return False

# I2C0, SDA=GP0, SCL=GP1
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

#LED on board
onboard_led = Pin("LED", Pin.OUT)
led = False #led state

# tlačítko na GP14 jako objekt
button = Button(14)

# adresa slave
SLAVE_ADDR = 0x42
while True:
    if button.is_pressed():
        data = b'1'
        led = not led
        try:
            i2c.writeto(SLAVE_ADDR, data)
            print("Odesláno:", data)
        except Exception as e:
            print("Chyba I2C:", e, data)
    
    if led:
        onboard_led.value(1)
    else:
        onboard_led.value(0)
    time.sleep(0.01)  # krátký delay
