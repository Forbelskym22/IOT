class UartController {
    constructor(uartModel) {
        this.uartModel = uartModel;
    }

    async getPorts(req, res) {
        try {
            const ports = await this.uartModel.getAvailablePorts();
            res.json({ 
                ports: ports, 
                currentPort: this.uartModel.getCurrentPort(),
                isConnected: this.uartModel.isConnected()
            });
        } catch (error) {
            res.status(500).json({ 
                status: 'Error', 
                message: error.message 
            });
        }
    }

    connect(req, res) {
        const portPath = req.query.port;
        const baudRate = req.query.baudRate || 9600;
        
        if (!portPath) {
            return res.json({ status: 'Error', message: 'Port path required' });
        }
        
        const success = this.uartModel.connectToUART(portPath, parseInt(baudRate));
        res.json({ 
            status: success ? 'Connected' : 'Failed',
            port: portPath,
            baudRate: baudRate
        });
    }

    getMessages(req, res) {
        const messages = this.uartModel.getMessages();
        res.json({ 
            messages: messages,
            count: messages.length
        });
    }

    async sendMessage(req, res) {
        const message = req.query.message || 'Hello from Raspberry Pi';
        
        try {
            await this.uartModel.sendMessage(message);
            res.json({ 
                status: 'Message sent via UART', 
                message: message 
            });
        } catch (error) {
            res.json({ 
                status: 'Error sending message', 
                error: error.message 
            });
        }
    }
}

module.exports = UartController;
