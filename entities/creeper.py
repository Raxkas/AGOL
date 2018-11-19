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

        else if (this.isNear(Monorem)) {
            let cell = random(this.findNear(Monorem));
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

Creeper._defaultEnergy = 20;
Creeper._multiplicationCost = 3;
Creeper._energyLimit = 27;
Creeper._movementCost = 0.1;
Creeper._energyFromPrey = 1;
Creeper._bangRadius = 5;
Creeper._childrenPerMultiplication = 6;
