from flask import Flask, render_template, jsonify, request
from collections import deque
import random
import time

app = Flask(__name__)

# Configuration for the grid
cols, rows = 20, 20

# Generate the grid with vertices
def create_grid():
    return [[{'wall': False, 'visited': False, 'prev': None} for _ in range(rows)] for _ in range(cols)]

# Get a random target point that is not a wall
def get_random_target(grid):
    while True:
        end_x = random.randint(0, cols - 1)
        end_y = random.randint(0, rows - 1)
        if not grid[end_x][end_y]['wall']:
            return end_x, end_y

# Dijkstra's Algorithm
def run_dijkstra(grid, start, end):
    queue = deque([start])
    path = []
    steps = []
    grid[start[0]][start[1]]['visited'] = True

    while queue:
        current = queue.popleft()
        steps.append(current)

        if current == end:
            while current:
                path.append(current)
                current = grid[current[0]][current[1]]['prev']
            return steps, path[::-1]  # Return steps and reversed path

        x, y = current
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

        for neighbor in neighbors:
            nx, ny = neighbor
            if 0 <= nx < cols and 0 <= ny < rows and not grid[nx][ny]['wall'] and not grid[nx][ny]['visited']:
                grid[nx][ny]['visited'] = True
                grid[nx][ny]['prev'] = current
                queue.append(neighbor)

    return steps, []  # No path found

@app.route('/')
def index():
    grid = create_grid()
    start = (0, 0)  # Fixed starting point
    end = get_random_target(grid)  # Random target
    return render_template('index.html', grid=grid, start=start, end=end, path=[], steps=[], cols=cols, rows=rows)

@app.route('/run')
def run():
    grid = create_grid()
    start = (0, 0)
    end = get_random_target(grid)

    steps, path = run_dijkstra(grid, start, end)
    
    # Store state in the session (or use a global variable)
    app.config['GRID'] = grid
    app.config['START'] = start
    app.config['END'] = end
    app.config['STEPS'] = steps
    app.config['PATH'] = path
    app.config['CURRENT_STEP'] = 0

    return jsonify({'status': 'running'})

@app.route('/next_step')
def next_step():
    current_step = app.config.get('CURRENT_STEP', 0)
    steps = app.config.get('STEPS', [])
    grid = app.config.get('GRID', [])

    if current_step < len(steps):
        current = steps[current_step]
        app.config['CURRENT_STEP'] += 1
        return jsonify({'current': current, 'grid': grid})
    else:
        return jsonify({'status': 'completed', 'path': app.config['PATH']})

if __name__ == '__main__':
    app.run(debug=True)
