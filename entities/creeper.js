class Creeper extends Attacker {
    constructor() {
        super();
    }

    _next_tick() {
        if (this.energy >= this._bang_cost) {
            this.bang()
        }

        else if (this.isNear(Xotaker, Predator)) {
            let prey_kind = Xotaker;
            if (!this.isNear(Xotaker)) {
                prey_kind = Predator;
            }
            let cell = random(this.findNear(prey_kind));
            this.eat(cell)
        }

        else if (this.isNear(Air, Grass)) {
            let cell = random(this.findNear(Air, Grass));
            this.move(cell);
        }
    }

    bang() {
        if (this.energy < 20) {
            throw "not enough power";
        }
        let damaged = this.directions.concat(this.pos);
        damaged.map(this.kill);
    }
}

Creeper._default_energy = 10;
Creeper._multiplication_cost = +Infinity;
Creeper._energy_from_prey = 2;
Creeper._bang_cost = 20;
