class Attacker extends Mob {
    get _movementCost() {
        return this.kind._movementCost;
    }

    get _energyFromPrey() {
        return this.kind._energyFromPrey;
    }

    move(pos) {
        this._gameLogic.swap(this, pos)
        this.energy -= this._movementCost;
    }

    eat(pos) {
        this.kill(pos);
        this._gameLogic.replace(pos, Air);
        this._gameLogic.swap(this, pos);
        this.energy += this._energyFromPrey;
    }
}
