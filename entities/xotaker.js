class Xotaker extends Attacker {
    constructor() {
        super();
    }

    _nextTick() {
        if (this.isNear(Air) && this.canMultiply()) {
            let cell = random(this.findNear(Air));
            this.multiply(cell);
        }

        else if (this.isNear(Grass) && this.canMultiply() && this.energy == this._energyLimit) {
            let cell = random(this.findNear(Grass));
            let oldPos = this.pos;
            this.eat(cell);
            this.multiply(oldPos);
        }

        else if (this.isNear(Grass)) {
            let cell = random(this.findNear(Grass))
            this.eat(cell);
        }

        else if (this.isNear(Air)) {
            let cell = random(this.findNear(Air));
            this.move(cell)
        }
    }
}

Xotaker._defaultEnergy = 5;
Xotaker._multiplicationCost = 20;
Xotaker._energyLimit = 40;
Xotaker._energyFromPrey = 2;
