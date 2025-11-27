const { SerialPort } = require('serialport');

class DualUartModel {
    constructor() {
        this.uart0 = null;  // /dev/serial0 - Output UART (send to Pico)
        this.uart3 = null;  // /dev/ttyAMA2 - Input UART (receive from Pico)
        this.availablePorts = [];
        this.receivedMessages = []; // Store messages received from UART3
    }

    async getAvailablePorts() {
        try {
            const ports = await SerialPort.list();
            let detectedPaths = ports.map(p => p.path);
            
            const knownPiPorts = [
                '/dev/serial0',   // UART 0
                '/dev/ttyAMA2'    // UART 3
            ];

            this.availablePorts = [...new Set([...detectedPaths, ...knownPiPorts])];
            console.log('Available ports:', this.availablePorts);
            return this.availablePorts;

        } catch (err) {
            console.log('Error listing ports:', err.message);
            return ['/dev/serial0', '/dev/ttyAMA2'];
        }
    }

    // Connect UART 0 for OUTPUT (sending commands to Pico)
    connectOutputUART(baudRate = 9600) {
        try {
            const portPath = '/dev/serial0';
            
            // Close existing port if open
            if (this.uart0 && this.uart0.isOpen) {
                console.log('Closing previous UART0 connection');
                this.uart0.close();
            }
            
            console.log(`Connecting OUTPUT UART0: ${portPath} at ${baudRate} baud`);
            this.uart0 = new SerialPort({ path: portPath, baudRate: baudRate });
            
            this.uart0.on('open', () => {
                console.log('✓ UART0 (OUTPUT) opened:', portPath);
            });

            this.uart0.on('error', (err) => {
                console.log('UART0 Error:', err.message);
            });
            
            return true;
        } catch (err) {
            console.log('UART0 connection error:', err.message);
            return false;
        }
    }

    // Connect UART 3 for INPUT (receiving data from Pico)
    connectInputUART(baudRate = 9600) {
        try {
            const portPath = '/dev/ttyAMA2';
            
            // Close existing port if open
            if (this.uart3 && this.uart3.isOpen) {
                console.log('Closing previous UART3 connection');
                this.uart3.close();
            }
            
            console.log(`Connecting INPUT UART3: ${portPath} at ${baudRate} baud`);
            this.uart3 = new SerialPort({ path: portPath, baudRate: baudRate });
            
            this.uart3.on('open', () => {
                console.log('✓ UART3 (INPUT) opened:', portPath);
            });

            // Listen for incoming data from the second Pico
            this.uart3.on('data', (data) => {
                const message = data.toString().trim();
                console.log('📨 Received from Pico (UART3):', message);
                this.receivedMessages.push({
                    timestamp: new Date().toISOString(),
                    message: message
                });
                
                // Keep only last 100 messages
                if (this.receivedMessages.length > 100) {
                    this.receivedMessages.shift();
                }
            });

            this.uart3.on('error', (err) => {
                console.log('UART3 Error:', err.message);
            });
            
            return true;
        } catch (err) {
            console.log('UART3 connection error:', err.message);
            return false;
        }
    }

    // Connect both UARTs at once
    connectBothUARTs(baudRate = 9600) {
        const uart0Success = this.connectOutputUART(baudRate);
        const uart3Success = this.connectInputUART(baudRate);
        return uart0Success && uart3Success;
    }

    // Send LED control command via UART0
    sendLEDCommand(command) {
        return new Promise((resolve, reject) => {
            if (!this.uart0 || !this.uart0.isOpen) {
                reject(new Error('UART0 (OUTPUT) not connected. Please connect first.'));
                return;
            }

            const validCommands = ['on', 'off'];
            const cmd = command.toLowerCase();

            if (!validCommands.includes(cmd)) {
                reject(new Error(`Invalid command. Use 'on' or 'off'`));
                return;
            }

            this.uart0.write(cmd + '\n', (err) => {
                if (err) {
                    reject(err);
                } else {
                    console.log(`📤 Sent to Pico: ${cmd}`);
                    resolve(cmd);
                }
            });
        });
    }

    // Send custom message via UART0
    sendMessage(message) {
        return new Promise((resolve, reject) => {
            if (!this.uart0 || !this.uart0.isOpen) {
                reject(new Error('UART0 (OUTPUT) not connected. Please connect first.'));
                return;
            }

            this.uart0.write(message + '\n', (err) => {
                if (err) {
                    reject(err);
                } else {
                    console.log(`📤 Sent to Pico: ${message}`);
                    resolve(message);
                }
            });
        });
    }

    // Get status of both UARTs
    getStatus() {
        return {
            uart0: {
                path: '/dev/serial0',
                connected: this.uart0 && this.uart0.isOpen,
                description: 'OUTPUT - Send commands to Pico (Pin 8 TX, Pin 10 RX)'
            },
            uart3: {
                path: '/dev/ttyAMA2',
                connected: this.uart3 && this.uart3.isOpen,
                description: 'INPUT - Receive data from Pico (Pin 7 TX, Pin 29 RX)'
            }
        };
    }

    // Get received messages
    getReceivedMessages(limit = 50) {
        return this.receivedMessages.slice(-limit).reverse();
    }

    // Clear received messages
    clearReceivedMessages() {
        this.receivedMessages = [];
    }

    // Close connections
    closeConnections() {
        if (this.uart0 && this.uart0.isOpen) {
            this.uart0.close();
            console.log('UART0 closed');
        }
        if (this.uart3 && this.uart3.isOpen) {
            this.uart3.close();
            console.log('UART3 closed');
        }
    }
}

module.exports = DualUartModel;
