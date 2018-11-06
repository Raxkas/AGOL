class Predator extends Attacker {
    constructor() {
        super();
    }

    _nextTick() {
        if (this.isNear(Air) && this.canMultiply()) {
            let cell = random(this.findNear(Air));
            this.multiply(cell);
        }

        else if (this.isNear(Xotaker, Monorem)) {
            let cell = random(this.findNear(Xotaker, Monorem));
            this.eat(cell);
        }

        else if (this.isNear(Air, Grass)) {
            let cell = random(this.findNear(Air, Grass));
            this.move(cell);
        }
    }
}

Predator._defaultEnergy = 100;
Predator._multiplicationCost = 9;
Predator._energyLimit = 145;
Predator._energyFromPrey = 3;
