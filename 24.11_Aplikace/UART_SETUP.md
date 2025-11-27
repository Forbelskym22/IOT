# Dual UART Setup Guide

## Hardware Connections

### UART 0 - OUTPUT (Raspberry Pi → Pico #1)
**Raspberry Pi Pins:**
- TX (Pin 8, GPIO 14) → Pico RX (GPIO 1, Pin 2)
- RX (Pin 10, GPIO 15) → Pico TX (GPIO 0, Pin 1)
- GND (Pin 6) → Pico GND

**Device:** `/dev/serial0`
**Purpose:** Send "on"/"off" commands to control Pico LED

### UART 3 - INPUT (Pico #2 → Raspberry Pi)
**Raspberry Pi Pins:**
- TX (Pin 7, GPIO 4) → Pico RX (GPIO 5, Pin 7)
- RX (Pin 29, GPIO 5) → Pico TX (GPIO 4, Pin 6)
- GND (Pin 6) → Pico GND

**Device:** `/dev/ttyAMA2`
**Purpose:** Receive status updates from Pico

## Software Setup

### 1. Flash Pico Firmware

**Pico #1 (Receiver):**
```bash
# Copy pico_receiver.py to Pico as main.py
# This Pico will receive commands and control LED
```

**Pico #2 (Sender - Optional):**
```bash
# Copy pico_sender.py to Pico as main.py
# This Pico will send status updates back
```

### 2. Start Node.js Server

```bash
npm start
# or
node app.js
```

### 3. Connect to UARTs

Open browser: `http://localhost:3000`

Or use API:
```bash
# Connect both UARTs
curl http://localhost:3000/dual-uart/connect?baudRate=9600

# Check status
curl http://localhost:3000/dual-uart/status

# Turn LED ON
curl http://localhost:3000/dual-uart/led/on

# Turn LED OFF
curl http://localhost:3000/dual-uart/led/off

# Get received messages
curl http://localhost:3000/dual-uart/received
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dual-uart/connect` | GET | Connect both UARTs |
| `/dual-uart/status` | GET | Get connection status |
| `/dual-uart/led/on` | GET | Send "on" command to Pico |
| `/dual-uart/led/off` | GET | Send "off" command to Pico |
| `/dual-uart/send?message=XXX` | GET | Send custom message |
| `/dual-uart/received` | GET | Get messages from Pico #2 |
| `/dual-uart/clear` | GET | Clear received messages |
| `/dual-uart/close` | GET | Close all connections |

## Testing

1. **Test UART0 (Output):**
   ```bash
   curl http://localhost:3000/dual-uart/led/on
   # LED on Pico #1 should turn ON
   
   curl http://localhost:3000/dual-uart/led/off
   # LED on Pico #1 should turn OFF
   ```

2. **Test UART3 (Input):**
   ```bash
   curl http://localhost:3000/dual-uart/received
   # Should show messages from Pico #2
   ```

## Troubleshooting

1. **Check UART permissions:**
   ```bash
   sudo usermod -a -G dialout $USER
   sudo chmod 666 /dev/serial0 /dev/ttyAMA2
   ```

2. **Verify UART is enabled:**
   ```bash
   ls -l /dev/serial0 /dev/ttyAMA2
   ```

3. **Check connections:**
   - Verify GND is connected
   - TX goes to RX, RX goes to TX
   - Check baud rate matches (9600)

4. **Monitor Pico output:**
   - Connect Pico to USB and use Thonny IDE to see debug messages
