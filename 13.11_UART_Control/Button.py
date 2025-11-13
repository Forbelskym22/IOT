from machine import Pin, UART
import time


class ButtonUART:
    def __init__(self, pin_number, uart_id=0, baud=9600):
        # UART setup
        self.uart = UART(uart_id, baudrate=baud)

        # Button setup with internal pull-up
        self.button = Pin(pin_number, Pin.IN, Pin.PULL_UP)

        # Track state (1 = released, 0 = pressed)
        self.state = self.button.value()

    def read(self):
        """Read and update the button state."""
        current = self.button.value()

        pressed = False

        # Detect press edge
        if self.state == 1 and current == 0:
            self.uart.write("Pressed")
            print("klik")
            pressed = True

        self.state = current
        return pressed


# --- SETUP ---
btn = ButtonUART(pin_number=15)      # Button on GP15
led = Pin("LED", Pin.OUT)            # LED controlled outside the class

# --- MAIN LOOP ---
while True:
    if btn.read():                   # True only on button press event
        led.toggle()                 # LED toggles here
    
    time.sleep(0.02)
