const express = require('express');
const path = require('path');
const config = require('./src/config/server');

// Import Models
const LedModel = require('./src/models/LedModel');
const UartModel = require('./src/models/UartModel');
const DualUartModel = require('./src/models/DualUartModel');

// Import Controllers
const LedController = require('./src/controllers/LedController');
const UartController = require('./src/controllers/UartController');
const DualUartController = require('./src/controllers/DualUartController');

// Import Routes
const ledRoutes = require('./src/routes/ledRoutes');
const uartRoutes = require('./src/routes/uartRoutes');
const dualUartRoutes = require('./src/routes/dualUartRoutes');

// Initialize Express app
const app = express();

// Initialize Models
const ledModel = new LedModel(config.ledPin);
const uartModel = new UartModel();
const dualUartModel = new DualUartModel();

// Initialize Controllers
const ledController = new LedController(ledModel);
const uartController = new UartController(uartModel);
const dualUartController = new DualUartController(dualUartModel);

// Initialize available ports on startup
uartModel.getAvailablePorts();

// Serve static files from 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Register Routes
app.use('/led', ledRoutes(ledController));
app.use('/api', uartRoutes(uartController));
app.use('/uart', uartRoutes(uartController));
app.use('/dual-uart', dualUartRoutes(dualUartController));

// Route for home page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Route for dual UART page
app.get('/dual-uart-page', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'dual-uart.html'));
});

// Start server
app.listen(config.port, () => {
    console.log(`Server running at http://localhost:${config.port}`);
});

module.exports = app;
