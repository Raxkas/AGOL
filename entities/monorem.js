let _monoremsJointEnergy = 150;


class Monorem extends Attacker {
    constructor() {
        super();
    }

    _nextTick() {
        if (this.isNear(Air) && this.canMultiply()) {
            let cell = random(this.findNear(Air));
            this.multiply(cell);
        }

        else if (this.isNear(Xotaker, Predator, Creeper)) {
            let cell = random(this.findNear(Xotaker, Predator, Creeper));
            this.eat(cell);
        }

        else if (this.isNear(Air, Grass)) {
            let cell = random(this.findNear(Air, Grass));
            this.move(cell);
        }
    }

    get energy() {
        if ("_gameLogic" in this) {
            return _monoremsJointEnergy/this._gameLogic.count(this.kind);
        }
        return this._defaultEnergy;
    }

    set energy(value) {
        _monoremsJointEnergy -= this.energy;
        _monoremsJointEnergy += value;
        if (this.energy > this._energyLimit) {
            _monoremsJointEnergy = this._energyLimit*this._gameLogic.count(this.kind);
        }
    }
}

Monorem._defaultEnergy = 5;
Monorem._multiplicationCost = 9;
Monorem._energyLimit = 20;
Monorem._energyFromPrey = 3;
