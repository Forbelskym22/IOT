const express = require('express');
const path = require('path');
const config = require('./src/config/server');

// Import Models
const LedModel = require('./src/models/LedModel');
const UartModel = require('./src/models/UartModel');

// Import Controllers
const LedController = require('./src/controllers/LedController');
const UartController = require('./src/controllers/UartController');

// Import Routes
const ledRoutes = require('./src/routes/ledRoutes');
const uartRoutes = require('./src/routes/uartRoutes');

// Initialize Express app
const app = express();

// Initialize Models
const ledModel = new LedModel(config.ledPin);
const uartModel = new UartModel();

// Initialize Controllers
const ledController = new LedController(ledModel);
const uartController = new UartController(uartModel);

// Initialize available ports on startup
uartModel.getAvailablePorts();

// Serve static files from 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Register Routes
app.use('/led', ledRoutes(ledController));
app.use('/api', uartRoutes(uartController));
app.use('/uart', uartRoutes(uartController));

// Route for home page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
app.listen(config.port, () => {
    console.log(`Server running at http://localhost:${config.port}`);
});

module.exports = app;
