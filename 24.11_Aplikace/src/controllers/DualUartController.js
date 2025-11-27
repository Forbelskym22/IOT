class DualUartController {
    constructor(dualUartModel) {
        this.dualUartModel = dualUartModel;
    }

    async getPorts(req, res) {
        try {
            const ports = await this.dualUartModel.getAvailablePorts();
            const status = this.dualUartModel.getStatus();
            res.json({ 
                ports: ports,
                status: status
            });
        } catch (error) {
            res.status(500).json({ 
                status: 'Error', 
                message: error.message 
            });
        }
    }

    connectBoth(req, res) {
        const baudRate = req.query.baudRate || 9600;
        
        const success = this.dualUartModel.connectBothUARTs(parseInt(baudRate));
        const status = this.dualUartModel.getStatus();
        
        res.json({ 
            status: success ? 'Both UARTs Connected' : 'Connection Failed',
            baudRate: baudRate,
            uarts: status
        });
    }

    async sendLEDCommand(req, res) {
        const command = req.query.command || req.params.command;
        
        if (!command) {
            return res.json({ 
                status: 'Error', 
                message: 'Command required (on/off)' 
            });
        }

        try {
            const sentCommand = await this.dualUartModel.sendLEDCommand(command);
            res.json({ 
                status: 'Command sent successfully', 
                command: sentCommand,
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            res.json({ 
                status: 'Error sending command', 
                error: error.message 
            });
        }
    }

    async sendCustomMessage(req, res) {
        const message = req.query.message;
        
        if (!message) {
            return res.json({ 
                status: 'Error', 
                message: 'Message required' 
            });
        }

        try {
            await this.dualUartModel.sendMessage(message);
            res.json({ 
                status: 'Message sent via UART0', 
                message: message,
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            res.json({ 
                status: 'Error sending message', 
                error: error.message 
            });
        }
    }

    getReceivedMessages(req, res) {
        const limit = req.query.limit || 50;
        const messages = this.dualUartModel.getReceivedMessages(parseInt(limit));
        res.json({ 
            messages: messages,
            count: messages.length
        });
    }

    clearMessages(req, res) {
        this.dualUartModel.clearReceivedMessages();
        res.json({ 
            status: 'Messages cleared' 
        });
    }

    getStatus(req, res) {
        const status = this.dualUartModel.getStatus();
        res.json(status);
    }

    closeConnections(req, res) {
        this.dualUartModel.closeConnections();
        res.json({ 
            status: 'All UART connections closed' 
        });
    }
}

module.exports = DualUartController;
