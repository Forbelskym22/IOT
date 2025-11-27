"""
Raspberry Pi Pico - RECEIVER (with LED control)
Connected to Raspberry Pi UART0 (/dev/serial0)
Pins: RX = GPIO1 (Pin 2), TX = GPIO0 (Pin 1)
LED: GPIO25 (built-in LED) or use external LED on GPIO15

This Pico receives "on" or "off" commands via UART and controls an LED
"""

from machine import UART, Pin
import time

# Initialize UART0 on Pico
# RX = GPIO1 (Pin 2), TX = GPIO0 (Pin 1)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Initialize LED (built-in LED on Pico)
led = Pin(25, Pin.OUT)  # Use Pin 25 for built-in LED
# Or use external LED: led = Pin(15, Pin.OUT)

print("Pico RECEIVER ready - waiting for commands...")
print("Expecting 'on' or 'off' commands from Raspberry Pi")

while True:
    if uart.any():
        # Read incoming data
        data = uart.read()
        if data:
            message = data.decode('utf-8').strip().lower()
            print(f"Received: {message}")
            
            # Control LED based on command
            if message == 'on':
                led.on()
                print("✓ LED turned ON")
                # Optional: Send acknowledgment back
                uart.write("LED_ON\n")
                
            elif message == 'off':
                led.off()
                print("✓ LED turned OFF")
                # Optional: Send acknowledgment back
                uart.write("LED_OFF\n")
                
            else:
                print(f"Unknown command: {message}")
                uart.write(f"UNKNOWN:{message}\n")
    
    time.sleep(0.1)  # Small delay to prevent busy-waiting
