# Dual UART Communication System

A Node.js application with MVC architecture for controlling Raspberry Pi Pico devices via dual UART communication.

## 🎯 Features

- **MVC Architecture** - Clean separation of concerns with Models, Views, and Controllers
- **Dual UART Support** - Simultaneous communication on two UART ports
- **LED Control** - Send "on"/"off" commands to control Pico LED via UART0
- **Bidirectional Communication** - Receive status updates from Pico via UART3
- **Web Interface** - Modern UI with real-time message display
- **RESTful API** - Complete API for programmatic control

## 📁 Project Structure

```
24.11_Aplikace/
├── app.js                          # Main application entry point
├── src/
│   ├── config/
│   │   └── server.js              # Server configuration
│   ├── models/
│   │   ├── LedModel.js            # LED GPIO control
│   │   ├── UartModel.js           # Single UART operations
│   │   └── DualUartModel.js       # Dual UART operations
│   ├── controllers/
│   │   ├── LedController.js       # LED request handlers
│   │   ├── UartController.js      # UART request handlers
│   │   └── DualUartController.js  # Dual UART handlers
│   └── routes/
│       ├── ledRoutes.js           # LED endpoints
│       ├── uartRoutes.js          # UART endpoints
│       └── dualUartRoutes.js      # Dual UART endpoints
├── public/
│   ├── index.html                 # Original LED control page
│   └── dual-uart.html             # Dual UART control page
├── pico_receiver.py               # Pico #1 firmware (receives commands)
├── pico_sender.py                 # Pico #2 firmware (sends status)
├── package.json
└── UART_SETUP.md                  # Hardware setup guide
```

## 🔌 Hardware Setup

### UART 0 - OUTPUT (Raspberry Pi → Pico #1)
**Purpose:** Send LED control commands ("on"/"off")

| Raspberry Pi | Connection | Pico #1 |
|--------------|------------|---------|
| Pin 8 (GPIO 14) - TX | → | GPIO 1 (Pin 2) - RX |
| Pin 10 (GPIO 15) - RX | → | GPIO 0 (Pin 1) - TX |
| Pin 6 - GND | → | GND |

**Device:** `/dev/serial0`

### UART 3 - INPUT (Pico #2 → Raspberry Pi)
**Purpose:** Receive status updates from Pico

| Raspberry Pi | Connection | Pico #2 |
|--------------|------------|---------|
| Pin 7 (GPIO 4) - TX | → | GPIO 5 (Pin 7) - RX |
| Pin 29 (GPIO 5) - RX | → | GPIO 4 (Pin 6) - TX |
| Pin 6 - GND | → | GND |

**Device:** `/dev/ttyAMA2`

## 🚀 Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Flash Pico Firmware

**Pico #1 (LED Controller):**
1. Connect Pico #1 to computer via USB
2. Copy `pico_receiver.py` to Pico as `main.py`
3. Connect Pico to Raspberry Pi UART0 (see wiring above)

**Pico #2 (Status Sender - Optional):**
1. Connect Pico #2 to computer via USB
2. Copy `pico_sender.py` to Pico as `main.py`
3. Connect Pico to Raspberry Pi UART3 (see wiring above)

### 3. Configure UART Permissions
```bash
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/serial0 /dev/ttyAMA2
```

### 4. Start Server
```bash
npm start
# or
node app.js
```

### 5. Open Web Interface
```
http://localhost:3000              # Original LED control
http://localhost:3000/dual-uart-page  # Dual UART control
```

## 🌐 Web Interface

### Main Page (`/`)
- Direct GPIO LED control on Raspberry Pi
- Single UART configuration
- Manual UART messaging

### Dual UART Page (`/dual-uart-page`)
- UART connection status for both ports
- LED control via UART0 (sends "on"/"off" to Pico)
- Custom message sending
- Real-time message display from UART3
- Auto-refresh received messages

## 📡 API Endpoints

### Dual UART Endpoints

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/dual-uart/connect` | GET | Connect both UARTs | `curl http://localhost:3000/dual-uart/connect?baudRate=9600` |
| `/dual-uart/status` | GET | Get connection status | `curl http://localhost:3000/dual-uart/status` |
| `/dual-uart/led/on` | GET | Turn Pico LED ON | `curl http://localhost:3000/dual-uart/led/on` |
| `/dual-uart/led/off` | GET | Turn Pico LED OFF | `curl http://localhost:3000/dual-uart/led/off` |
| `/dual-uart/send` | GET | Send custom message | `curl "http://localhost:3000/dual-uart/send?message=hello"` |
| `/dual-uart/received` | GET | Get received messages | `curl http://localhost:3000/dual-uart/received?limit=50` |
| `/dual-uart/clear` | GET | Clear message buffer | `curl http://localhost:3000/dual-uart/clear` |
| `/dual-uart/close` | GET | Close connections | `curl http://localhost:3000/dual-uart/close` |

### Legacy Endpoints

| Endpoint | Description |
|----------|-------------|
| `/led/on` | Turn GPIO LED ON |
| `/led/off` | Turn GPIO LED OFF |
| `/api/ports` | List available ports |
| `/uart/send?message=XXX` | Send UART message |

## 🧪 Testing

### 1. Test UART Connections
```bash
# Connect both UARTs
curl http://localhost:3000/dual-uart/connect

# Check status
curl http://localhost:3000/dual-uart/status
```

### 2. Test LED Control
```bash
# Turn LED ON
curl http://localhost:3000/dual-uart/led/on

# Turn LED OFF
curl http://localhost:3000/dual-uart/led/off
```

### 3. Test Message Reception
```bash
# Get received messages
curl http://localhost:3000/dual-uart/received
```

## 🔧 Troubleshooting

### UART Not Detected
```bash
# Check if UART devices exist
ls -l /dev/serial0 /dev/ttyAMA2

# Check UART is enabled in boot config
grep enable_uart /boot/config.txt
```

### Permission Denied
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Set permissions (temporary)
sudo chmod 666 /dev/serial0 /dev/ttyAMA2

# Reboot
sudo reboot
```

### No Data Received
1. Verify GND is connected between devices
2. Check TX→RX and RX→TX connections
3. Verify baud rate matches (9600)
4. Check Pico is powered and running firmware
5. Use USB connection to monitor Pico debug output

### LED Not Responding
1. Verify UART0 connection
2. Check command format ("on" or "off")
3. Monitor Pico serial output via USB
4. Verify LED pin in Pico firmware (GPIO 25)

## 📝 Pico Firmware

### Receiver (Pico #1)
- Listens for "on"/"off" commands via UART
- Controls LED on GPIO 25 (built-in LED)
- Sends acknowledgment messages back

### Sender (Pico #2 - Optional)
- Sends periodic status updates
- Can send button press notifications
- Useful for sensor data transmission

## 🏗️ Architecture

This project follows **Model-View-Controller (MVC)** pattern:

- **Models** - Handle hardware communication (GPIO, UART)
- **Views** - HTML/JavaScript frontend interfaces
- **Controllers** - Process HTTP requests and coordinate models
- **Routes** - Define API endpoints and URL mappings
- **Config** - Centralized configuration management

## 📦 Dependencies

- `express` - Web server framework
- `serialport` - UART/Serial communication
- `array-gpio` - GPIO control on Raspberry Pi

## 🎓 Learn More

See `UART_SETUP.md` for detailed hardware setup instructions.

## 📄 License

MIT

## 👤 Author

IoT Application Development - 2025
