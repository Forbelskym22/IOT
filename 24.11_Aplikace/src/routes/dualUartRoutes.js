const express = require('express');
const router = express.Router();

module.exports = (dualUartController) => {
    // Get available ports and status
    router.get('/ports', (req, res) => dualUartController.getPorts(req, res));
    
    // Connect both UARTs
    router.get('/connect', (req, res) => dualUartController.connectBoth(req, res));
    
    // Send LED command (on/off)
    router.get('/led/:command', (req, res) => dualUartController.sendLEDCommand(req, res));
    
    // Send custom message
    router.get('/send', (req, res) => dualUartController.sendCustomMessage(req, res));
    
    // Get received messages from UART3
    router.get('/received', (req, res) => dualUartController.getReceivedMessages(req, res));
    
    // Clear received messages
    router.get('/clear', (req, res) => dualUartController.clearMessages(req, res));
    
    // Get UART status
    router.get('/status', (req, res) => dualUartController.getStatus(req, res));
    
    // Close connections
    router.get('/close', (req, res) => dualUartController.closeConnections(req, res));
    
    return router;
};
