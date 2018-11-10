class Mob extends Entity {
    get _defaultEnergy() {
        return this.kind._defaultEnergy;
    }

    get _multiplicationCost() {
        return this.kind._multiplicationCost;
    }

    get _energyLimit() {
        return this.kind._energyLimit;
    }

    get energy() {
        return this._energy;
    }

    set energy(value) {
        this._energy = value;
        if (this._energy > this._energyLimit) {
            this._energy = this._energyLimit;
        }
    }

    constructor() {
        super();
        this.energy = this._defaultEnergy;
    }

    spawn(kind, pos) {
        if (!(this._gameLogic.getEntityByPos(pos) instanceof Air)) {
            throw "Is not empty cell: " + pos;
        }
        this._gameLogic.replace(pos, kind);
    }

    canMultiply() {
        return this.energy >= this._defaultEnergy + this._multiplicationCost;
    }

    multiply(pos) {
        this.spawn(this.kind, pos);
        this.energy -= this._multiplicationCost;
    }

    nextTick() {
        this._nextTick();
        if (this.energy <= 0) {
            this.kill(this);
        }
    }
}
