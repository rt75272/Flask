const canvas = document.getElementById('gridCanvas');
const ctx = canvas.getContext('2d');
const cols = 64, rows = 48;
const cellWidth = canvas.width / cols;
const cellHeight = canvas.height / rows;

let walls = [];
let start = { x: Math.floor(cols / 2), y: Math.floor(rows / 2) };
let end = null;

// Draw grid with outlines
function drawGrid() {
    for (let x = 0; x < cols; x++) {
        for (let y = 0; y < rows; y++) {
            ctx.fillStyle = '#2c3e50';
            ctx.fillRect(x * cellWidth, y * cellHeight, cellWidth, cellHeight);
            ctx.strokeStyle = '#34495e'; // Cell outline color
            ctx.strokeRect(x * cellWidth, y * cellHeight, cellWidth, cellHeight);
        }
    }
}

// Draw the start and end points
function drawStartEnd() {
    ctx.fillStyle = '#00ffcc'; // Start point color
    ctx.fillRect(start.x * cellWidth, start.y * cellHeight, cellWidth, cellHeight);
    ctx.strokeStyle = '#00cc99'; // Start outline color
    ctx.strokeRect(start.x * cellWidth, start.y * cellHeight, cellWidth, cellHeight);
    
    if (end) {
        ctx.fillStyle = '#007bff'; // End point color
        ctx.fillRect(end.x * cellWidth, end.y * cellHeight, cellWidth, cellHeight);
        ctx.strokeStyle = '#0056b3'; // End outline color
        ctx.strokeRect(end.x * cellWidth, end.y * cellHeight, cellWidth, cellHeight);
    }
}

// Handle mouse clicks for wall placement
canvas.addEventListener('click', (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((event.clientX - rect.left) / cellWidth);
    const y = Math.floor((event.clientY - rect.top) / cellHeight);
    
    if (walls.includes(`${x},${y}`)) {
        walls = walls.filter(wall => wall !== `${x},${y}`);
        toggleWall(x, y, false);
    } else {
        walls.push(`${x},${y}`);
        toggleWall(x, y, true);
    }
    drawGrid();
    drawStartEnd();
});

// Toggle wall state
function toggleWall(x, y, state) {
    fetch('/toggle_wall', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ x: x, y: y, state: state })
    });
}

// Run Dijkstra's algorithm
document.getElementById('runDijkstra').addEventListener('click', () => {
    fetch('/run_dijkstra', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            end = { x: data.end[0], y: data.end[1] }; // Save the endpoint coordinates
            drawPath(data.path);
            drawStartEnd();
        } else {
            alert('No path found!');
        }
    });
});

// Draw the path
function drawPath(path) {
    path.forEach(([x, y]) => {
        ctx.fillStyle = '#e74c3c'; // Color for the path
        ctx.fillRect(x * cellWidth, y * cellHeight, cellWidth, cellHeight);
    });
}

// Initial drawing
drawGrid();
drawStartEnd();
