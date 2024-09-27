let layers = [4, 5, 3];  // Define the number of nodes in each layer
let nodes = [];  // Array to store node positions and velocities

function setup() {
  let canvas = createCanvas(windowWidth, windowHeight);  // Full window size
  canvas.position(0, 0);
  canvas.style('z-index', '-1');  // Ensure the canvas is in the background
  frameRate(30);  // Set the frame rate for the animation

  // Initialize node positions and random velocities for each node
  for (let i = 0; i < layers.length; i++) {
    nodes[i] = [];
    let layerSpacing = width / (layers.length + 1);  // Calculate spacing between layers

    for (let j = 0; j < layers[i]; j++) {
      let x = (i + 1) * layerSpacing + random(-20, 20);  // Randomize the X position slightly
      let y = random(50, height - 50);  // Randomize Y position within the canvas bounds

      nodes[i][j] = {
        x: x,
        y: y,
        xVel: random(-1, 1),  // Random velocity in X direction
        yVel: random(-1, 1),  // Random velocity in Y direction
      };
    }
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);  // Adjust canvas size when the window is resized
}

function draw() {
  background(0, 0, 0, 85);  // Black background
  let nodeDiameter = 5;
  let darkGray = 500; // animation color/opacity. 

  // Draw and animate the nodes
  for (let i = 0; i < layers.length; i++) {
    for (let j = 0; j < layers[i]; j++) {
      // Update node positions based on velocity
      nodes[i][j].x += nodes[i][j].xVel;
      nodes[i][j].y += nodes[i][j].yVel;

      // Keep nodes within the canvas boundaries
      if (nodes[i][j].x < 0 || nodes[i][j].x > width) nodes[i][j].xVel *= -1;
      if (nodes[i][j].y < 0 || nodes[i][j].y > height) nodes[i][j].yVel *= -1;

      // Draw nodes (dark gray circles)
      fill(darkGray);  // Dark gray color for nodes
      noStroke();
      ellipse(nodes[i][j].x, nodes[i][j].y, nodeDiameter, nodeDiameter);

      // Animate connections between layers
      if (i > 0) {
        for (let k = 0; k < layers[i - 1]; k++) {
          // Draw lines between nodes of consecutive layers (dark gray lines)
          stroke(darkGray);  // Dark gray color for lines
          strokeWeight(0.25);
          line(nodes[i - 1][k].x, nodes[i - 1][k].y, nodes[i][j].x, nodes[i][j].y);

        //   // Draw an animated pulse along the lines (dark gray pulse)
        //   let pulseLength = (frameCount % 100) / 100;
        //   let pulseX = lerp(nodes[i - 1][k].x, nodes[i][j].x, pulseLength);
        //   let pulseY = lerp(nodes[i - 1][k].y, nodes[i][j].y, pulseLength);
        //   noStroke();
        //   fill(darkGray);  // Dark gray color for the pulse
        //   ellipse(pulseX, pulseY, 5, 5);
        }
      }
    }
  }
}
