const r = require('array-gpio');
const express = require('express');
const path = require('path');
const { SerialPort } = require('serialport');
const app = express();
const port = 3000;

// Create LED output object
let led = r.out(40);

// UART/Serial port configuration
let uartPort = null;
let availablePorts = [];
let uartMessages = []; // Store messages for testing

// Function to get available serial ports
async function getAvailablePorts() {
    try {
        const ports = await SerialPort.list();
        availablePorts = ports.map(p => p.path);
        console.log('Available ports:', availablePorts);
        
        // If no ports found, add demo port for testing
        if (availablePorts.length === 0) {
            console.log('No real ports found. Available for demo: /dev/ttyDEMO');
            availablePorts = ['/dev/ttyDEMO'];
        }
        
        return availablePorts;
    } catch (err) {
        console.log('Error listing ports:', err.message);
        return ['/dev/ttyDEMO'];
    }
}

// Function to connect to UART port
function connectToUART(portPath, baudRate = 9600) {
    try {
        if (uartPort && uartPort.isOpen) {
            uartPort.close();
        }
        
        // Demo mode for testing
        if (portPath === '/dev/ttyDEMO') {
            uartPort = {
                path: portPath,
                isOpen: true,
                write: (data, callback) => {
                    console.log(`[DEMO UART ${portPath}] Sent: ${data}`);
                    uartMessages.push(data);
                    if (callback) callback(null);
                }
            };
            console.log('Connected to DEMO UART port:', portPath);
            return true;
        }
        
        uartPort = new SerialPort({ path: portPath, baudRate: baudRate });
        
        uartPort.on('open', () => {
            console.log('UART port opened:', portPath);
        });
        
        uartPort.on('error', (err) => {
            console.log('UART Error:', err.message);
        });
        
        return true;
    } catch (err) {
        console.log('Connection error:', err.message);
        return false;
    }
}

// Initialize available ports on startup
getAvailablePorts();

// Serve static files from 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Route for home page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API endpoints to control LED
app.get('/led/on', (req, res) => {
    led.on();
    res.json({ status: 'LED turned ON' });
});

app.get('/led/off', (req, res) => {
    led.off();
    res.json({ status: 'LED turned OFF' });
});

// API endpoint to get available serial ports
app.get('/api/ports', async (req, res) => {
    const ports = await getAvailablePorts();
    res.json({ 
        ports: ports, 
        currentPort: uartPort ? uartPort.path : null,
        isConnected: uartPort && uartPort.isOpen 
    });
});

// API endpoint to connect to a specific port
app.get('/api/connect', (req, res) => {
    const portPath = req.query.port;
    const baudRate = req.query.baudRate || 9600;
    
    if (!portPath) {
        return res.json({ status: 'Error', message: 'Port path required' });
    }
    
    const success = connectToUART(portPath, parseInt(baudRate));
    res.json({ 
        status: success ? 'Connected' : 'Failed',
        port: portPath,
        baudRate: baudRate
    });
});

// API endpoint to get sent messages (for testing)
app.get('/api/messages', (req, res) => {
    res.json({ 
        messages: uartMessages,
        count: uartMessages.length
    });
});

// API endpoint to send message via UART
app.get('/uart/send', (req, res) => {
    const message = req.query.message || 'Hello from Raspberry Pi';
    
    if (!uartPort || !uartPort.isOpen) {
        return res.json({ status: 'Error', error: 'UART port not connected. Please connect to a port first.' });
    }

    uartPort.write(message + '\r\n', (err) => {
        if (err) {
            return res.json({ status: 'Error sending message', error: err.message });
        }
        res.json({ status: 'Message sent via UART', message: message });
    });
});

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});