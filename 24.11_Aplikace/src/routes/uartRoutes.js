const express = require('express');
const router = express.Router();

module.exports = (uartController) => {
    // Route to get available serial ports
    router.get('/ports', (req, res) => uartController.getPorts(req, res));
    
    // Route to connect to a specific port
    router.get('/connect', (req, res) => uartController.connect(req, res));
    
    // Route to get sent messages (for testing)
    router.get('/messages', (req, res) => uartController.getMessages(req, res));
    
    // Route to send message via UART
    router.get('/send', (req, res) => uartController.sendMessage(req, res));
    
    return router;
};
