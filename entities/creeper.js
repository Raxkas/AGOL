class Creeper extends Attacker {
    constructor() {
        super();
    }

    get _bangCost() {
        return this.kind._bangCost;
    }

    get _bangRadius() {
        return this.kind._bangRadius;
    }

    _nextTick() {
        if (this.energy >= this._bangCost) {
            this.bang()
        }

        else if (this.isNear(Xotaker, Predator)) {
            let preyKind = Xotaker;
            if (!this.isNear(Xotaker)) {
                preyKind = Predator;
            }
            let cell = random(this.findNear(preyKind));
            this.eat(cell)
        }

        else if (this.isNear(Air, Grass)) {
            let cell = random(this.findNear(Air, Grass));
            this.move(cell);
        }
    }

    _getArea(radius) {
        let [x, y] = this.pos;
        let rangePositive = [];
        for (let i = 1; i <= radius; i++) {
            rangePositive.push(i);
        }
        let rangeNegative = rangePositive.map(v => -v).reverse();
        let range = [].concat(rangeNegative, [0], rangePositive);
        let xRange = range.map(v => x + v);
        let yRange = range.map(v => y + v);
        let rows = yRange.map(y => xRange.map(x => [x, y]));
        let area = [].concat(...rows).filter(p => this._gameLogic.isPosCorrect(p));
        return area;
    }

    bang() {
        if (this.energy < this._bangCost) {
            throw "Not enough energy";
        }
        let damaged = this._getArea(this._bangRadius);
        damaged.map(p => this.kill(p));
    }
}

Creeper._defaultEnergy = 10;
Creeper._multiplicationCost = +Infinity;
Creeper._energyLimit = +Infinity;
Creeper._energyFromPrey = 2;
Creeper._bangCost = 20;
Creeper._bangRadius = 5;
