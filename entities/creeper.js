class Creeper extends Attacker {
    constructor() {
        super();
    }

    get _bangCost() {
        return this.kind._bangCost;
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

    bang() {
        if (this.energy < this._bangCost) {
            throw "Not enough energy";
        }
        let damaged = this.directions.concat([this.pos]);
        damaged.map(p => this.kill(p));
    }
}

Creeper._defaultEnergy = 10;
Creeper._multiplicationCost = +Infinity;
Creeper._energyLimit = +Infinity;
Creeper._energyFromPrey = 2;
Creeper._bangCost = 20;
