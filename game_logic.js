function _getRandomOf(kinds, spawnChances) {
    const chancesSum = spawnChances.reduce((a, b) => a+b);
    const seed = Math.random() * chancesSum;
    let passedChancesSum = 0;
    for (var id in spawnChances) {
        passedChancesSum += spawnChances[id];
        if (passedChancesSum > seed) {
            return kinds[id];
        }
    }
    throw "Something went wrong. Arguments: " + [kinds, spawnChances];
}


class AGOLLogic {
    constructor(width, height, kinds, spawnChances) {
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
        this._generateEntities(spawnChances);
        this.tickNumber = 0;
    }
    
    _generateEntities(spawnChances) {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                let kind = _getRandomOf(this._KINDS, spawnChances);
                this.replace([x,y], kind);
            }
        }
    }
    
    nextTick() {
        let entities = [].concat(...this._ARRAYS);
        for (let entity of entities) {
            if (entity.alive) {
                entity.nextTick();
            }
        }
        this.tickNumber += 1;
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
        let oldEntity = this._getEntityBy(value);
        
        if (value === oldEntity) {
            var pos = oldEntity.pos;
        }
        else {
            var pos = value;
        }
        let [x, y] = pos;
        
        if (oldEntity !== null) {
            this._matrix[y][x] = null;
            let oldEntityArray = this.getArrayBy(oldEntity);
            let i = oldEntityArray.indexOf(oldEntity);
            if (i < 0) {
                throw "Entity not in array";
            }
            oldEntityArray.splice(i, 1);
            oldEntity.alive = false;
        }
        
        let newEntity = new kind();
        this.getArrayBy(newEntity).push(newEntity);
        this._matrix[y][x] = newEntity;
        newEntity.pos = pos;
        newEntity._gameLogic = this;
        newEntity.alive = true;
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
            if (!value.alive) {
                throw "Dead entity";
            }
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
