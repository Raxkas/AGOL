// GAME SETTINGS
const WIDTH = 50;
const HEIGHT = 50;
const SPAWN_CHANCES = [90, 10, 10, 1, 1, 1];
const KINDS = [Air, Grass, Xotaker, Predator, Creeper, Monorem];

// OUTPUT SETTINGS
const CELL_SIDE_PX = 16;
const BACKGROUND_COLOR = '#acacacff';
const COLORS = {
    "Air": "#acacac",
    "Grass": "#007f00",
    "Xotaker": "#ffff00",
    "Predator": "#ff0000",
    "Creeper": "#003399",
    "Monorem": "#ffffff"
}
const FPS = 5;


var logic = null;


function setup() {
    logic = new AGOLLogic(WIDTH, HEIGHT, KINDS, SPAWN_CHANCES);
    frameRate(FPS);
    createCanvas(logic.width * CELL_SIDE_PX, logic.height * CELL_SIDE_PX);
    background(BACKGROUND_COLOR);
}


function draw() {
    background(BACKGROUND_COLOR);
    for (let y = 0; y < logic.height; y++) {
        for (let x = 0; x < logic.width; x++) {
            let pos = [x, y];
            let entity = logic.getEntityByPos(pos);
            let kindName = entity.kind.name;
            let opacity = _computeOpacity(entity);
            let color = COLORS[kindName] + opacity.toString(16);
            _setColor(pos, color);
        }
    }
    logic.nextTick();
}


function _setColor(pos, newColor) {
    let [x, y] = pos;
    fill(newColor);
    rect(x*CELL_SIDE_PX, y*CELL_SIDE_PX, CELL_SIDE_PX, CELL_SIDE_PX);
}


function _computeOpacity(entity) {
    let opacity = 255;
    if (!(entity instanceof Mob)) {
        return opacity;
    }
    const energy = entity.energy;
    const defEnergy = entity._defaultEnergy;
    const multCost = entity._multiplicationCost;
    if (energy < defEnergy+multCost) {
        opacity = 64 + 32*energy/(defEnergy+multCost);
    }
    else {
        opacity = 128 + 5*(energy-defEnergy-multCost);
    }
    if (opacity >= 255) {
        opacity = 255;
    }
    opacity = Math.floor(opacity);
    return opacity;
}
