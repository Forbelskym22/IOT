from machine import Pin
import sys
import select

# 1. Setup the LED on GP15
# We initialize it to 0 (OFF) to start
led = Pin(15, Pin.OUT)
led.value(0)

# 2. Setup the listener (Poller)
# This allows us to check if data is waiting without stopping the code
poll_object = select.poll()
poll_object.register(sys.stdin, select.POLLIN)

print("System Ready.")
print("Type 'on', 'off', or 'toggle' and press Enter.")

# 3. Main Loop
while True:
    # Check if there is data waiting on the USB connection (timeout=0 means check instantly)
    if poll_object.poll(0):
        # Read the line, strip whitespace/newlines, and convert to lowercase
        message = sys.stdin.readline().strip().lower()
        
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
            print(f"Ignored unknown message: {message}")