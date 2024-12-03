
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.width = 700;
canvas.height = 600;

const ROWS = 6;
const COLS = 7;
const CELL_SIZE = 100;
const COLORS = {
    EMPTY: "#000",
    PLAYER1: "#FF4500",
    PLAYER2: "#FFD700",
    BACKGROUND: "#1E90FF",
    GRID: "#000"
};

// Initialize board
const board = Array.from({ length: ROWS }, () => Array(COLS).fill(0));

// Draw grid
function drawGrid() {
    ctx.fillStyle = COLORS.BACKGROUND;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            const x = col * CELL_SIZE;
            const y = row * CELL_SIZE + CELL_SIZE;
            ctx.fillStyle = COLORS.EMPTY;
            ctx.beginPath();
            ctx.arc(x + CELL_SIZE / 2, y + CELL_SIZE / 2, CELL_SIZE / 2.5, 0, Math.PI * 2);
            ctx.fill();
        }
    }
}

drawGrid();
