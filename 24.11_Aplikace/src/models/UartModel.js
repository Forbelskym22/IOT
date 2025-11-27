const { SerialPort } = require('serialport');

class UartModel {
    constructor() {
        this.uartPort = null;
        this.availablePorts = [];
        this.uartMessages = []; // Store messages for testing
    }

    async getAvailablePorts() {
        try {
            // 1. Ask the OS what it sees
            const ports = await SerialPort.list();
            let detectedPaths = ports.map(p => p.path);
            
            // 2. FORCE ADD the Raspberry Pi specific UARTs
            // Even if SerialPort.list() misses them, we know they exist because of your config.
            const knownPiPorts = [
                '/dev/serial0',  // The default (Pins 8 & 10)
                '/dev/ttyAMA1',  // Likely UART 2 (Pins 27 & 28)
                '/dev/ttyAMA2',  // Likely UART 3 (Pins 7 & 29)
                '/dev/ttyAMA3'   // Just in case
            ];

            // 3. Merge lists and remove duplicates
            this.availablePorts = [...new Set([...detectedPaths, ...knownPiPorts])];
            
            console.log('Available ports:', this.availablePorts);
            return this.availablePorts;

        } catch (err) {
            console.log('Error listing ports:', err.message);
            // Fallback
            return ['/dev/serial0', '/dev/ttyAMA1', '/dev/ttyAMA2'];
        }
    }

    connectToUART(portPath, baudRate = 9600) {
        try {
            // Close existing port if open
            if (this.uartPort && this.uartPort.isOpen) {
                console.log(`Closing previous port: ${this.uartPort.path}`);
                this.uartPort.close();
            }
            
            // Demo mode for testing
            if (portPath === '/dev/ttyDEMO') {
                this.uartPort = {
                    path: portPath,
                    isOpen: true,
                    write: (data, callback) => {
                        console.log(`[DEMO] Sent: ${data}`);
                        this.uartMessages.push(data);
                        if (callback) callback(null);
                    }
                };
                return true;
            }
            
            // Create new connection
            console.log(`Attempting to connect to ${portPath} at ${baudRate}...`);
            this.uartPort = new SerialPort({ path: portPath, baudRate: baudRate });
            
            this.uartPort.on('open', () => {
                console.log('SUCCESS: UART port opened:', portPath);
            });
            
            // Added: Listen for incoming data from Pico
            this.uartPort.on('data', (data) => {
                console.log('Data from Pico:', data.toString());
            });

            this.uartPort.on('error', (err) => {
                console.log('UART Error:', err.message);
            });
            
            return true;
        } catch (err) {
            console.log('Connection error:', err.message);
            return false;
        }
    }

    sendMessage(message) {
        return new Promise((resolve, reject) => {
            if (!this.uartPort || !this.uartPort.isOpen) {
                reject(new Error('UART port not connected. Please connect to a port first.'));
                return;
            }

            this.uartPort.write(message + '\r\n', (err) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(message);
                }
            });
        });
    }

    getCurrentPort() {
        return this.uartPort ? this.uartPort.path : null;
    }

    isConnected() {
        return this.uartPort && this.uartPort.isOpen;
    }

    getMessages() {
        return this.uartMessages;
    }
}

module.exports = UartModel;
