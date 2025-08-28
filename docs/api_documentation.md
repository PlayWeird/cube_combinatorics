# Cube Combinatorics API Documentation

## Overview
This document provides detailed API documentation for the Rubik's Cube Combinatorics library.

## Modules

### cube_model
Core cube representation and operations.

#### Classes
- `Cube`: Main cube class for operations and transformations
- `CubeState`: Data class representing a cube state

#### Key Methods
- `from_json(json_path)`: Load cube state from JSON file
- `to_json(json_path)`: Save cube state to JSON file
- `apply_move(move)`: Apply a move to the cube
- `is_solved()`: Check if the cube is solved
- `validate_state()`: Validate cube state legality

### visualizer
Cube visualization module for generating images.

#### Classes
- `CubeVisualizer`: Handles all visualization operations

#### Key Methods
- `create_net_visualization(cube_state, output_path)`: Create 2D net visualization
- `create_numbered_visualization(cube_state, output_path)`: Create numbered position visualization
- `export_as_png(figure, output_path)`: Export as PNG
- `export_as_svg(figure, output_path)`: Export as SVG

### solver
Solving algorithms implementation.

#### Classes
- `CubeSolver`: Main solver class
- `LayerByLayerSolver`: Layer-by-layer solving implementation
- `Solution`: Data class for solution representation

#### Key Methods
- `solve(cube_state)`: Find solution for given cube state
- `validate_solution(cube_state, solution)`: Verify solution correctness

### utils
Utility functions for various operations.

#### Key Functions
- `parse_move_sequence(move_string)`: Parse move notation
- `inverse_move(move)`: Get inverse of a move
- `simplify_move_sequence(moves)`: Optimize move sequences
- `validate_color_count(cube_state)`: Validate color distribution

## JSON Schema

### Cube State Format
```json
{
  "format_version": "1.0",
  "cube_state": {
    "faces": {
      "U": [[3x3 color array]],
      "D": [[3x3 color array]],
      "F": [[3x3 color array]],
      "B": [[3x3 color array]],
      "L": [[3x3 color array]],
      "R": [[3x3 color array]]
    }
  },
  "metadata": {
    "timestamp": "ISO 8601",
    "scramble": "move sequence or null",
    "description": "optional description"
  }
}
```

### Color Codes
- `W`: White
- `Y`: Yellow
- `R`: Red
- `O`: Orange
- `G`: Green
- `B`: Blue

## Move Notation

### Basic Moves
- `F`: Front face clockwise
- `B`: Back face clockwise
- `U`: Up face clockwise
- `D`: Down face clockwise
- `L`: Left face clockwise
- `R`: Right face clockwise

### Modifiers
- `'`: Counterclockwise (e.g., `F'`)
- `2`: 180-degree turn (e.g., `F2`)
- lowercase: Wide moves (e.g., `f` moves front two layers)

## Examples

### Loading and Visualizing a Cube
```python
from src.cube_model import Cube
from src.visualizer import CubeVisualizer

cube = Cube()
cube.from_json("examples/scrambled_cube.json")

visualizer = CubeVisualizer()
visualizer.create_net_visualization(cube.state, "output.png")
```

### Solving a Cube
```python
from src.solver import CubeSolver

solver = CubeSolver(method="layer_by_layer")
solution = solver.solve(cube.state)
print(f"Solution: {' '.join(solution.moves)}")
print(f"Move count: {solution.move_count}")
```