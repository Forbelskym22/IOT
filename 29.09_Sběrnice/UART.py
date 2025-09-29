from machine import Pin, UART
import time

class Button:
    def __init__(self, pin_num, pull=Pin.PULL_UP, debounce_ms=50):
        self.pin = Pin(pin_num, Pin.IN, pull)
        self.debounce_ms = debounce_ms
        self.last_state = self.pin.value()
        self.last_time = time.ticks_ms()

    def is_pressed(self):
        """Vrací True pouze jednou při každém stisku (přechod HIGH->LOW)."""
        current = self.pin.value()
        now = time.ticks_ms()

        # Debounce
        if time.ticks_diff(now, self.last_time) > self.debounce_ms:
            if self.last_state == 1 and current == 0:  # PULL_UP => 1=neaktivní, 0=stisk
                self.last_state = current
                self.last_time = now
                return True
            self.last_state = current
            self.last_time = now
        return False


# --- Inicializace ---
button = Button(14)                  # Tlačítko na GP14
led = Pin("LED", Pin.OUT)            # Vestavěná LED
led_state = 0                         # Aktuální stav LED

# UART1 na pinech GP16 (TX) a GP17 (RX) s rychlostí 9600 baud
uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))


# --- Hlavní smyčka ---
while True:
    if button.is_pressed():
        led_state = not led_state       # Přepnutí 0/1
        led.value(led_state)

        # Odeslat hodnotu po UART (jako text + nový řádek)
        uart.write(f"{int(led_state)}\n")

        print("LED přepnuta na:", led_state)

    time.sleep(0.01)  # malé zpoždění pro šetření CPU
