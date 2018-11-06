class Grass extends Mob {
    constructor() {
        super();
    }

    _next_tick() {
        this.energy++;
        if (this.isNear(Air) && this.can_multiply()) {
            let cell = random(this.findNear(Air));
            this.multiply(cell);
        }
    }
}

Grass._default_energy = 1;
Grass._multiplication_cost = 4;
Grass._energy_limit = 10;
