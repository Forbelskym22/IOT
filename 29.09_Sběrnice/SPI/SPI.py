from machine import Pin, SPI
import time

# SPI Master Configuration
# SCK  - GP2
# MOSI - GP3
# MISO - GP4
# CS   - GP5

# Initialize SPI
spi = SPI(0, 
          baudrate=100000,  # 100 kHz - pomalé pro bit-banging slave
          polarity=0,
          phase=0,
          bits=8,
          firstbit=SPI.MSB,
          sck=Pin(2),
          mosi=Pin(3),
          miso=Pin(4))

# CS pin
cs = Pin(5, Pin.OUT)
cs.value(1)  # CS high (inactive)

print("MicroPython SPI Master Ready")
print("Sending messages to bit-banging slave...")

def send_message(msg):
    """Send a message to the slave"""
    # Convert string to bytes and pad to 16 bytes
    data = msg.encode('utf-8')
    data = data + b'\x00' * (16 - len(data))
    
    # Pull CS low (activate slave)
    cs.value(0)
    time.sleep_ms(10)  # Delay for slave to detect CS
    
    # Send data byte by byte with delays
    for byte_val in data:
        spi.write(bytes([byte_val]))
        time.sleep_ms(1)  # Small delay between bytes
    
    # Pull CS high (deactivate slave)
    time.sleep_ms(10)
    cs.value(1)
    
    print(f"Sent: {msg}")

# Main loop
message_count = 0

while True:
    message_count += 1
    send_message(f"Hello #{message_count}")
    time.sleep(2)  # Wait 2 seconds between messages