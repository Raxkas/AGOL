class Creeper extends Attacker {
    constructor() {
        super();
    }

    get _bangRadius() {
        return this.kind._bangRadius;
    }

    get _childrenPerMultiplication() {
        return this.kind._childrenPerMultiplication;
    }

    _nextTick() {
        if (this.canMultiply()) {
            this.bang();
            let availableCells = this._getArea(this._bangRadius);
            for (let i = 0; i < this._childrenPerMultiplication; i++) {
                let cell = random(availableCells);
                this.spawn(Creeper, cell);
                availableCells = availableCells.filter(x => x !== cell);
            }
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
        let damaged = this._getArea(this._bangRadius);
        damaged.map(p => this.kill(p));
    }
}

Creeper._defaultEnergy = 10;
Creeper._multiplicationCost = 20;
Creeper._energyLimit = 40;
Creeper._energyFromPrey = 2;
Creeper._bangRadius = 5;
Creeper._childrenPerMultiplication = 8;
