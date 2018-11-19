class Entity {
    get kind() {
        return this.constructor;
    }

    get directions () {
        let area = this._getArea(1);
        return area.filter(p => this._gameLogic.getEntityByPos(p) !== this);
    }

     _getArea(radius) {
        let [x, y] = this.pos;
        let rangePositive = [];
        for (let i = 1; i <= radius; i++) {
            rangePositive.push(i);
        }
        let rangeNegative = rangePositive.map(v => -v).reverse();
        let range = [].concat(rangeNegative, [0], rangePositive);
        let xRange = range.map(v => x + v);
        let yRange = range.map(v => y + v);
        let rows = yRange.map(y => xRange.map(x => [x, y]));
        let area = [].concat(...rows).filter(p => this._gameLogic.isPosCorrect(p));
        return area;
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
