# Rubik's Cube Combinatorics

A Python application for visualizing and solving Rubik's Cube positions using group theory and mathematical constraints.

## Overview

This project implements a mathematically rigorous approach to Rubik's Cube manipulation, based on group theory principles documented in `docs/rubik.pdf`. Unlike simple color-based representations, we track piece positions (1-54) to ensure mathematical validity and detect impossible configurations.

### Key Features

- 🔢 **Position Tracking**: Tracks original positions (1-54) like the reference image
- ✅ **Mathematical Validation**: Enforces parity constraints and orientation rules
- 🎨 **Dual Visualization**: Shows both colors and position permutations
- 🧮 **Group Theory Based**: Implements constraints from mathematical literature
- 🚫 **Impossibility Detection**: Identifies unsolvable configurations

## Project Status

### ✅ Completed
- [x] Project structure and development guidelines (`CLAUDE.md`)
- [x] Position-based JSON schema design (`docs/json_schema_design.md`)
- [x] Mathematical foundation documentation
- [x] Skeleton code with proper architecture

### 🚧 In Progress
- [ ] Core cube model with position tracking (`src/cube_model.py`)
- [ ] Mathematical validation functions
- [ ] JSON I/O with hybrid format

### 📋 Planned
- [ ] Visualization module with position overlay (`src/visualizer.py`)
- [ ] Layer-by-layer solver implementation (`src/solver.py`)
- [ ] CLI interface (`main.py`)
- [ ] Comprehensive test suite
- [ ] Example cube states and documentation

## Quick Start

### Installation
```bash
git clone <repository-url>
cd cube_combinatorics
pip install -r requirements.txt
```

### Usage (Planned)
```bash
# Visualize a cube state with position tracking
python main.py visualize examples/scrambled_cube.json -o output.png --numbered

# Validate if a cube state is mathematically solvable
python main.py validate examples/impossible_cube.json

# Solve a scrambled cube
python main.py solve examples/scrambled_cube.json --method=layer_by_layer

# Generate a valid scramble
python main.py scramble -n 20 -o scrambled.json
```

## Mathematical Foundation

This project implements constraints from group theory:

- **Parity**: Only even permutations are reachable from solved state
- **Corner Orientation**: Sum of corner twists ≡ 0 (mod 3)
- **Edge Orientation**: Sum of edge flips ≡ 0 (mod 2)
- **Total Valid States**: 43,252,003,274,489,856,000 configurations

**Important**: ~11/12 of random color arrangements are mathematically impossible to solve!

## JSON Format

We use a hybrid approach tracking both positions and colors:

```json
{
  "format_version": "2.0",
  "cube_state": {
    "representation": "hybrid",
    "stickers": [
      {"id": 1, "face": "U", "position": [0, 0], "color": "W", "original_id": 1},
      {"id": 2, "face": "U", "position": [0, 1], "color": "G", "original_id": 15}
    ],
    "validation": {
      "parity": "even",
      "corner_orientation_sum": 0,
      "edge_orientation_sum": 0,
      "is_solvable": true
    }
  }
}
```

## Visualization

Generates images similar to `images/mathematics-permutation-group.jpg` showing:
- Standard cube net layout (cross pattern)
- Position numbers (1-54) overlaid on colors
- Before/after permutation comparisons
- Both color-only and position-tracking modes

## Development

### Architecture
```
src/
├── cube_model.py    # Core cube representation with position tracking
├── visualizer.py    # Image generation with position overlay
├── solver.py        # Layer-by-layer and advanced algorithms
└── utils.py         # Validation and helper functions
```

### Testing
- Mathematical constraint validation
- Parity and orientation checks
- Visual regression testing
- Performance benchmarks

## References

- **Primary**: `docs/rubik.pdf` - "The Mathematics of the Rubik's Cube" (MIT)
- **Position Reference**: `images/mathematics-permutation-group.jpg`
- **Schema Design**: `docs/json_schema_design.md`
- **Development Guide**: `CLAUDE.md`

## Contributing

1. Follow mathematical constraints from `docs/rubik.pdf`
2. Maintain position tracking for all operations
3. Validate solvability before attempting solutions
4. Include comprehensive tests for edge cases

## License

[License to be determined]

---

**Note**: This is an active development project. The core mathematical framework is established, and implementation is underway. See `CLAUDE.md` for detailed development guidelines.