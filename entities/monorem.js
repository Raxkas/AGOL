let _monoremsJointEnergy = 150;


class Monorem extends Attacker {
    constructor() {
        super();
    }

    _next_tick() {
        if (this.isNear(Air) && this.can_multiply()) {
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
        if ("_game_logic" in this) {
            return _monoremsJointEnergy/this._game_logic.count(this.kind);
        }
        return this._default_energy;
    }

    set energy(value) {
        _monoremsJointEnergy -= this.energy;
        _monoremsJointEnergy += value;
    }
}

Monorem._default_energy = 5;
Monorem._multiplication_cost = 9;
Monorem._energy_from_prey = 3;
