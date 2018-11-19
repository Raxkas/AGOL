class Grass extends Mob {
    constructor() {
        super();
    }

    _nextTick() {
        this.energy++;
        if (this.isNear(Air) && this.canMultiply()) {
            let cell = random(this.findNear(Air));
            this.multiply(cell);
        }
    }
}

Grass._defaultEnergy = 1;
Grass._multiplicationCost = 4;
Grass._energyLimit = 10;
