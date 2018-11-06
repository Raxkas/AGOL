class Predator extends Attacker {
    constructor() {
        super();
    }

    _next_tick() {
        if (this.isNear(Air) && this.can_multiply()) {
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

Predator._default_energy = 100;
Predator._multiplication_cost = 9;
Predator._energy_from_prey = 3;
