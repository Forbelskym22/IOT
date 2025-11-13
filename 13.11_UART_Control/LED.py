from machine import UART, Pin
import time

# ---- UART SETUP ----
# UART0: TX = GP0, RX = GP1
uart = UART(0, baudrate=9600)

# ---- LED SETUP ----
led = Pin(15, Pin.OUT)   # Built-in onboard LED

buffer = b""  # incoming data buffer

while True:
    if uart.any():                               # data available?
        buffer += uart.read()                    # accumulate received bytes

        # check for newline-terminated command
        if b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)
            cmd = line.decode().strip()

            # ---- COMMAND HANDLING ----
            if cmd == "ON":
                led.value(1)
            elif cmd == "OFF":
                led.value(0)

    time.sleep(0.01)
