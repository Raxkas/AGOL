class Attacker extends Mob {
    get _movement_cost() {
        return this.kind._movement_cost;
    }

    get _energy_from_prey() {
        return this.kind._energy_from_prey;
    }

    move(pos) {
        this._game_logic.swap(this, pos)
        this.energy -= this._movement_cost;
    }

    eat(pos) {
        this.kill(pos);
        this._game_logic.replace(pos, Air);
        this._game_logic.swap(this, pos);
        this.energy += this._energy_from_prey;
    }
}

Attacker._movement_cost = 1;
