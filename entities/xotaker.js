class Xotaker extends Attacker {
    constructor() {
        super();
    }

    _next_tick() {
        if (this.isNear(Air) && this.can_multiply()) {
            let cell = random(this.findNear(Air));
            this.multiply(cell);
        }

        else if (this.isNear(Grass)) {
            let cell = random(this.findNear(Grass))
            this.eat(cell);
        }

        else if (this.isNear(Air)) {
            let cell = random(this.findNear(Air));
            this.move(cell)
        }
    }
}

Xotaker._default_energy = 5;
Xotaker._multiplication_cost = 20;
Xotaker._energy_from_prey = 2;
