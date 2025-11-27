"""
Raspberry Pi Pico - SENDER (optional - sends status updates)
Connected to Raspberry Pi UART3 (/dev/ttyAMA2)
Pins: RX = GPIO5 (Pin 7), TX = GPIO4 (Pin 6)

This Pico can send status updates, sensor data, or button presses back to Raspberry Pi
"""

from machine import UART, Pin
import time

# Initialize UART1 on Pico
# TX = GPIO4 (Pin 6), RX = GPIO5 (Pin 7)
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Optional: Button to send messages
button = Pin(16, Pin.IN, Pin.PULL_UP)  # Button on GPIO16

# Optional: Status LED
status_led = Pin(25, Pin.OUT)

print("Pico SENDER ready - sending status updates...")

counter = 0
button_pressed_last = False

while True:
    # Send periodic status updates
    counter += 1
    message = f"STATUS:{counter}\n"
    uart.write(message)
    print(f"Sent: {message.strip()}")
    
    # Check button state (if button is connected)
    button_pressed = not button.value()  # Active LOW
    if button_pressed and not button_pressed_last:
        uart.write("BUTTON_PRESSED\n")
        print("Button pressed - sent notification")
        status_led.toggle()
    
    button_pressed_last = button_pressed
    
    # Send status every 5 seconds
    time.sleep(5)
