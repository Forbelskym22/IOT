const express = require('express');
const router = express.Router();

module.exports = (ledController) => {
    // Route to turn LED on
    router.get('/on', (req, res) => ledController.turnOn(req, res));
    
    // Route to turn LED off
    router.get('/off', (req, res) => ledController.turnOff(req, res));
    
    return router;
};
