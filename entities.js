class Entity {
    get kind() {
        return this.constructor;
    }

    get directions () {
        let [x, y] = this.pos;
        let directions = [
            [x - 1, y - 1],
            [x    , y - 1],
            [x + 1, y - 1],
            [x - 1, y    ],
            [x + 1, y    ],
            [x - 1, y + 1],
            [x    , y + 1],
            [x + 1, y + 1]
        ];
        return directions.filter(p => this._game_logic.isPosCorrect(p));
    }

    isNear() {
        return this.findNear(...arguments).length > 0;
    }

    findNear() {
        if (arguments.length == 1) {
            let kind = arguments[0];
            return this.directions.filter(pos => this._game_logic.getEntityByPos(pos) instanceof kind);
        }
        let kinds = Array.from(arguments);
        let found = kinds.map(kind => this.findNear.apply(this, [kind])).reduce((a, b) => a.concat(b));
        return found;
    }
}



class Air extends Entity {
    constructor () {
        super();
    }

    next_tick() {
        null;
    }
}



class Mob extends Entity {
    get _default_energy() {
        return this.kind._default_energy;
    }

    get _multiplication_cost() {
        return this.kind._multiplication_cost;
    }

    get _energy_limit() {
        return this.kind._energy_limit;
    }

    get energy() {
        return this._energy;
    }

    set energy(value) {
        this._energy = value;
        if (this._energy > this._energy_limit) {
            this._energy = this._energy_limit;
        }
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
Xotaker._energy_limit = 40;
Xotaker._energy_from_prey = 2;



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
Predator._energy_limit = 145;
Predator._energy_from_prey = 3;


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
Creeper._energy_limit = +Infinity;
Creeper._energy_from_prey = 2;
Creeper._bang_cost = 20;


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
        if (this.energy > this._energy_limit) {
            _monoremsJointEnergy = this._energy_limit*this._game_logic.count(this.kind);
        }
    }
}

Monorem._default_energy = 5;
Monorem._multiplication_cost = 9;
Monorem._energy_limit = 20;
Monorem._energy_from_prey = 3;
