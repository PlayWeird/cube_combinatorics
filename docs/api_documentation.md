# Cube Combinatorics API Documentation

## Overview
This document provides detailed API documentation for the Rubik's Cube Combinatorics library, which implements a mathematically rigorous approach to cube manipulation with position tracking.

## Core Classes

### cube_model.Cube
Main cube class with position-based operations and mathematical validation.

#### Constructor
```python
Cube() -> Cube
```
Initialize a solved cube with position tracking.

#### Key Methods

##### State Management
- `from_json(json_path: str) -> None`: Load cube state from hybrid JSON format
- `to_json(json_path: str, format_version: str = '2.0', scramble: str = None) -> None`: Save state with validation data
- `is_solved() -> bool`: Check if cube is in solved state
- `validate_state() -> Tuple[bool, List[str]]`: Validate mathematical legality

##### Move Operations
- `apply_move(move: str) -> None`: Apply single move (supports F, R, U, B, L, D with ', 2 modifiers)
- `scramble(num_moves: int = 20, seed: Optional[int] = None, avoid_redundancy: bool = True) -> str`: Generate scramble sequence

##### Internal Classes
- `Sticker`: Represents individual cube sticker with position tracking
  - `id: int`: Current position ID (1-54)
  - `face: str`: Face name (U, L, F, R, B, D)
  - `position: Tuple[int, int]`: Face coordinates
  - `color: str`: Current color (W, Y, R, O, G, B)
  - `original_id: int`: Original position for permutation tracking

### visualizer.CubeVisualizer
Visualization with position overlay and dual-mode rendering.

#### Key Methods
- `create_2d_net(stickers: List[Sticker], show_numbers: bool = True, output_path: str = None) -> matplotlib.figure.Figure`: Create cube net with optional position numbers
- `_draw_face(ax, stickers: List[Sticker], face_offset: Tuple[int, int], show_numbers: bool)`: Draw individual face
- `_get_face_stickers(stickers: List[Sticker], face: str) -> List[Sticker]`: Extract stickers for specific face

### solver.Solver (Placeholder)
Future solving implementation with mathematical validation.

#### Planned Methods
- `solve(cube: Cube, method: str = 'layer_by_layer') -> List[str]`: Find solution sequence
- `validate_solution(cube: Cube, moves: List[str]) -> bool`: Verify solution correctness

## JSON Schema

### Hybrid Cube State Format (v2.0)
```json
{
  "format_version": "2.0",
  "cube_state": {
    "representation": "hybrid",
    "stickers": [
      {
        "id": 1,
        "face": "U",
        "position": [0, 0],
        "color": "W",
        "original_id": 1
      },
      {
        "id": 2,
        "face": "U", 
        "position": [0, 1],
        "color": "G",
        "original_id": 15
      }
    ],
    "validation": {
      "parity": "even",
      "corner_orientation_sum": 0,
      "edge_orientation_sum": 0,
      "is_solvable": true
    }
  },
  "metadata": {
    "timestamp": "2025-08-29T09:32:25.500588Z",
    "scramble": "F",
    "scramble_length": 1
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

## CLI Usage

### Available Commands
```bash
# Visualize cube state with position tracking
python main.py visualize <input.json> -o <output.png>

# Validate cube state mathematical legality  
python main.py validate <input.json>

# Generate random scramble
python main.py scramble -n <num_moves> -o <output.json>

# Generate specific move sequence
python main.py scramble -s "<move_sequence>" -o <output.json>

# Apply single move to solved cube
python main.py single-move "<move>" -o <output.json>

# Solve scrambled cube (future implementation)
python main.py solve <input.json> --method=<algorithm>
```

## Code Examples

### Basic Cube Operations
```python
from src.cube_model import Cube

# Create solved cube
cube = Cube()

# Apply moves
cube.apply_move("R")
cube.apply_move("U")  
cube.apply_move("R'")

# Check state
print(f"Solved: {cube.is_solved()}")
is_valid, errors = cube.validate_state()
print(f"Valid: {is_valid}")

# Save to file
cube.to_json("scrambled.json", scramble="R U R'")
```

### Visualization
```python
from src.visualizer import CubeVisualizer

# Create visualizer
viz = CubeVisualizer()

# Generate visualization with position numbers
fig = viz.create_2d_net(cube.stickers, show_numbers=True)

# Save as PNG
fig.savefig("cube_state.png", dpi=300, bbox_inches='tight')
```