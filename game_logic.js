function _get_random_of(kinds, spawn_chances) {
    const chances_sum = spawn_chances.reduce((a, b) => a+b);
    const seed = random() * chances_sum;
    let passed_chances_sum = 0;
    for (var id in spawn_chances) {
        passed_chances_sum += spawn_chances[id];
        if (passed_chances_sum > seed) {
            return kinds[id];
        }
    }
    throw "Something went wrong. Arguments: " + [kinds, spawn_chances];
}


class AGOLLogic {
    constructor(width, height, kinds, spawn_chances) {
        this.width = width;
        this.height = height;
        this._KINDS = Array.from(kinds);
        this._ARRAYS = [];
        for (let i in this._KINDS) {
            this._ARRAYS.push([]);
        }
        this._matrix = [];
        for (let y = 0; y < this.height; y++) {
            this._matrix.push([]);
            for (let x = 0; x < this.width; x++) {
                this._matrix[y].push(null);
            }
        }
        this._generate_entities(spawn_chances);
    }
    
    _generate_entities(spawn_chances) {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                let kind = _get_random_of(this._KINDS, spawn_chances);
                this.replace([x,y], kind);
            }
        }
    }
    
    next_tick() {
        let entities = [].concat(...this._ARRAYS);
        for (let entity of entities) {
            if (entity.alive) {
                entity.next_tick();
            }
        }
    }
    
    isPosCorrect(pos) {
        let [x, y] = pos;
        return (0 <= x && x < this.width && 0 <= y && y < this.height);
    }
    
    getEntityByPos(pos) {
        if (!this.isPosCorrect(pos)) {
            throw "Incorrect pos: " + pos;
        }
        let [x, y] = pos;
        let entity = this._matrix[y][x];
        return entity;
    }
    
    replace(value, kind) {
        let old_entity = this._getEntityBy(value);
        
        if (value === old_entity) {
            var pos = old_entity.pos;
        }
        else {
            var pos = value;
        }
        let [x, y] = pos;
        
        if (old_entity !== null) {
            this._matrix[y][x] = null;
            let old_entity_array = this.getArrayBy(old_entity);
            let i = old_entity_array.indexOf(old_entity);
            old_entity_array.splice(i, 1);
            old_entity.alive = false;
        }
        
        let new_entity = new kind();
        this.getArrayBy(new_entity).push(new_entity);
        this._matrix[y][x] = new_entity;
        new_entity.pos = pos;
        new_entity._game_logic = this;
        new_entity.alive = true;
    }
    
    swap(value1, value2) {
        let [entity1, entity2] = [value1, value2].map(v => this._getEntityBy(v));
        let [pos1, pos2] = [entity1.pos, entity2.pos];
        [entity1.pos, entity2.pos] = [pos2, pos1];
        let [[x1, y1], [x2, y2]] = [pos1, pos2];
        [this._matrix[y1][x1], this._matrix[y2][x2]] = [entity2, entity1];
    }
    
    getArrayBy(value) {
        let id = this._getId(value);
        return this._ARRAYS[id];
    }
    
    _getId(value) {
        if (this._ARRAYS.includes(value)) {
            return this._ARRAYS.indexOf(value);
        }
        else if (value instanceof Array && value.length == 2) {
            return this.getEntityByPos(value)
        }
        else if (this._KINDS.includes(value)) {
            return this._KINDS.indexOf(value);
        }
        else if (this._KINDS.includes(value.constructor)) {
            return this._getId(value.constructor);
        }
        else {
            throw "Incorrect value: " + value;
        }
    }
    
    _getEntityBy(value) {
        if (this._KINDS.includes(value.constructor)) {
            return value;
        }
        else {
            return this.getEntityByPos(value);
        }
    }
    
    count(kind) {
        return this.getArrayBy(kind).length;
    }
}
