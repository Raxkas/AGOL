let _monoremsJointEnergy = 0;


class Monorem extends Attacker {
    constructor() {
        super();
    }

    _nextTick() {
        this.energy += 1;

        if (this.isNear(Air) && this.canMultiply()) {
            let cell = random(this.findNear(Air));
            this.multiply(cell);
        }

        else if (this.isNear(Grass) && this.canMultiply() && this.energy >= this._defaultEnergy + this._multiplicationCost + 1) {
            let cell = random(this.findNear(Grass));
            this.kill(cell);
            this.multiply(cell);
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
        if ("_gameLogic" in this) {
            if (this.energy > this._energyLimit) {
                _monoremsJointEnergy = this._energyLimit*this._gameLogic.count(this.kind);
            }
        }
    }
}

Monorem._defaultEnergy = 10;
Monorem._multiplicationCost = 5;
Monorem._energyLimit = 20;
Monorem._movementCost = 0;
Monorem._energyFromPrey = undefined;
