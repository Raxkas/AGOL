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
        return directions.filter(p => this._gameLogic.isPosCorrect(p));
    }

    isNear() {
        return this.findNear(...arguments).length > 0;
    }

    findNear() {
        if (arguments.length == 1) {
            let kind = arguments[0];
            return this.directions.filter(pos => this._gameLogic.getEntityByPos(pos) instanceof kind);
        }
        let kinds = Array.from(arguments);
        let found = kinds.map(kind => this.findNear.apply(this, [kind])).reduce((a, b) => a.concat(b));
        return found;
    }
}
