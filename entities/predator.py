class Predator extends Attacker {
    constructor() {
        super();
    }

    _nextTick() {
        if (this.isNear(Air) && this.canMultiply()) {
            let cell = random(this.findNear(Air));
            this.multiply(cell);
        }

        else if (this.isNear(Xotaker)) {
            let cell = random(this.findNear(Xotaker));
            this.eat(cell);
        }

        else if (this.isNear(Air, Grass)) {
            let cell = random(this.findNear(Air, Grass));
            this.move(cell);
        }
    }
}

Predator._defaultEnergy = 10;
Predator._multiplicationCost = 3;
Predator._energyLimit = 20;
Predator._movementCost = 0.1;
Predator._energyFromPrey = 1;
