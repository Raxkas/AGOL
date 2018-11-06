class Mob extends Entity {
    get _default_energy() {
        return this.kind._default_energy;
    }

    get _multiplication_cost() {
        return this.kind._multiplication_cost;
    }

    constructor() {
        super();
        this.energy = this._default_energy;
    }

    spawn(kind, pos) {
        if (!(this._game_logic.getEntityByPos(pos) instanceof Air)) {
            throw "Is not empty cell: " + pos;
        }
        this._game_logic.replace(pos, kind);
    }

    kill(value) {
        this._game_logic.replace(value, Air);
    }

    can_multiply() {
        return this.energy >= this._default_energy + this._multiplication_cost;
    }

    multiply(pos) {
        this.spawn(this.kind, pos);
        this.energy -= this._multiplication_cost;
    }

    next_tick() {
        this._next_tick();
        if (this.energy <= 0) {
            this.kill(this);
        }
    }
}
