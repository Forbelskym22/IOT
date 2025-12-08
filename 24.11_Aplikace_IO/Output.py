from machine import Pin, UART
import time

# 1. Setup the LED on GP15
led = Pin(15, Pin.OUT)
led.value(0)

# 2. Setup UART0
# ID 0 corresponds to UART0.
# Baudrate must match your sender (9600 is standard for Bluetooth/GPS modules)
# tx=Pin(0) and rx=Pin(1) are the default UART0 pins
uart = UART(0, baudrate=9600, tx=Pin(0) , rx=Pin(1))

print("System Ready. Listening on UART0 (GP0/GP1)...")

# 3. Main Loop
while True:
    # Check if there is data waiting in the UART buffer
    if uart.any():
        # Read the line (returns bytes, e.g., b'on\n')
        data = uart.readline()
        
        try:
            # Convert bytes to string, strip whitespace, and lower case
            message = data.decode('utf-8').strip().lower()
            
            # Logic to handle the message
            if message == "on":
                led.value(1)
                print("Received: ON -> LED is now Lit")
                
            elif message == "off":
                led.value(0)
                print("Received: OFF -> LED is now Dark")
                
            elif message == "toggle":
                led.toggle()
                print("Received: TOGGLE -> LED state switched")
                
            else:
                # This helps debug if you are receiving hidden characters
                print(f"Ignored: {message}")
                
        except Exception as e:
            # Handles cases where garbage data cannot be decoded
            print(f"Error decoding message: {e}")
            
    # Short delay to prevent CPU overload
    time.sleep(0.01)
