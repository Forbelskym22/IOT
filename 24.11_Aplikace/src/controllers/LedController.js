class LedController {
    constructor(ledModel) {
        this.ledModel = ledModel;
    }

    turnOn(req, res) {
        const result = this.ledModel.turnOn();
        res.json(result);
    }

    turnOff(req, res) {
        const result = this.ledModel.turnOff();
        res.json(result);
    }
}

module.exports = LedController;
