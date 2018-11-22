// GAME SETTINGS
const WIDTH = 64;
const HEIGHT = 64;
const SPAWN_CHANCES = [128, 1, 1, 1, 1, 1];
const KINDS = [Air, Grass, Xotaker, Predator, Creeper, Monorem];

// OUTPUT SETTINGS
const CELL_SIDE_PX = 15;
const BACKGROUND_COLOR = '#000000';
const COLORS = {
    "Air": "#ffffff00",
    "Grass": "#007f00",
    "Xotaker": "#ffff00",
    "Predator": "#ff0000",
    "Creeper": "#0044bb",
    "Monorem": "#ffffff"
}
const FPS = 5;


const LOGIC = new AGOLLogic(WIDTH, HEIGHT, KINDS, SPAWN_CHANCES);


function setup() {
    frameRate(FPS);
    createCanvas(LOGIC.width * CELL_SIDE_PX, LOGIC.height * CELL_SIDE_PX);
    background(BACKGROUND_COLOR);
    strokeWeight(0.0625);
}


function draw() {
    showField(LOGIC);
    logGameInfo();
    LOGIC.nextTick();
}


function showField(logic) {
    background(BACKGROUND_COLOR);
    for (let y = 0; y < logic.height; y++) {
        for (let x = 0; x < logic.width; x++) {
            let pos = [x, y];
            let entity = logic.getEntityByPos(pos);
            let kindName = entity.kind.name;
            let color = COLORS[kindName]
            if (color.length == 1+6) {
                let opacity = _computeOpacity(entity);
                opacity = opacity.toString(16);
                if (opacity.length == 1) {
                    opacity = '0' + opacity;
                }
                color += opacity;
            }
            _setColor(pos, color);
        }
    }
}


function _setColor(pos, newColor) {
    let [x, y] = pos;
    fill(newColor);
    rect(x*CELL_SIDE_PX, y*CELL_SIDE_PX, CELL_SIDE_PX, CELL_SIDE_PX);
}


function _computeOpacity(entity) {
    const minOpacity = 64;
    const maxOpacity = 255
    let opacity = maxOpacity;
    if (!(entity instanceof Mob)) {
        return opacity;
    }
    const energy = entity.energy;
    const energyLimit = entity._energyLimit;
    let k = energy/energyLimit;
    opacity = minOpacity + k*(maxOpacity - minOpacity);
    opacity = Math.floor(opacity);
    if (opacity >= 255) {
        opacity = 255;
    }
    return opacity;
}


function logGameInfo() {
    console.log(LOGIC.tickNumber);
    for (let kind of KINDS) {
        let kindCount = LOGIC.count(kind);
        console.log(kind.name, kindCount);
    }
}
