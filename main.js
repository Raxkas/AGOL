// GAME SETTINGS
const WIDTH = 50;
const HEIGHT = 50;
// [4, 3, 2, 1, 1, 1]
const SPAWN_CHANCES = [90, 10, 10, 1, 1, 1];
const KINDS = [Air, Grass, Xotaker, Predator, Creeper, Monorem];

// OUTPUT SETTINGS
const CELL_SIDE_PX = 20; //7
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
            let kind_name = entity.kind.name;
            let opacity = _compute_opacity(entity);
            let color = COLORS[kind_name] + opacity.toString(16);
            _set_color(pos, color);
        }
    }
    logic.next_tick();
}


function _set_color(pos, new_color) {
    let [x, y] = pos;
    fill(new_color);
    rect(x*CELL_SIDE_PX, y*CELL_SIDE_PX, CELL_SIDE_PX, CELL_SIDE_PX);
}


function _compute_opacity(entity) {
    let opacity = 255;
    if (!(entity instanceof Mob)) {
        return opacity;
    }
    const energy = entity.energy;
    const def_energy = entity._default_energy;
    const mult_cost = entity._multiplication_cost;
    if (energy < def_energy+mult_cost) {
        opacity = 64 + 32*energy/(def_energy+mult_cost);
    }
    else {
        opacity = 128 + 5*(energy-def_energy-mult_cost);
    }
    if (opacity >= 255) {
        opacity = 255;
    }
    opacity = Math.floor(opacity);
    return opacity;
}
