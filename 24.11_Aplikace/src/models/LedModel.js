const r = require('array-gpio');

class LedModel {
    constructor(pin = 40) {
        this.led = r.out(pin);
    }

    turnOn() {
        this.led.on();
        return { status: 'LED turned ON' };
    }

    turnOff() {
        this.led.off();
        return { status: 'LED turned OFF' };
    }
}

module.exports = LedModel;
