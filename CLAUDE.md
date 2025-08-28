# Rubik's Cube Combinatorics Project

## Mission Statement
Build a Python application that:
1. **Visualizes** Rubik's Cube positions from JSON input files with position tracking (1-54)
2. **Validates** cube states using mathematical constraints from group theory
3. **Solves** cube positions with minimal move sequences

## Project Structure
```
cube_combinatorics/
├── src/
│   ├── __init__.py
│   ├── cube_model.py        # Core cube representation and operations
│   ├── visualizer.py        # Cube visualization module
│   ├── solver.py            # Solving algorithms
│   └── utils.py             # Helper functions
├── tests/
│   ├── test_cube_model.py
│   ├── test_visualizer.py
│   └── test_solver.py
├── examples/
│   ├── solved_cube.json
│   ├── scrambled_cube.json
│   └── example_outputs/
├── docs/
│   └── api_documentation.md
├── requirements.txt
├── main.py                  # CLI entry point
└── README.md
```

## Technical Requirements

### JSON Schema for Cube Position
```json
{
  "format_version": "2.0",
  "cube_state": {
    "representation": "hybrid",
    "stickers": [
      {"id": 1, "face": "U", "position": [0, 0], "color": "W", "original_id": 1},
      // ... all 54 stickers with position tracking
    ],
    "validation": {
      "parity": "even",
      "corner_orientation_sum": 0,
      "edge_orientation_sum": 0,
      "is_solvable": true
    }
  },
  "metadata": {
    "timestamp": "ISO 8601",
    "scramble": "optional move sequence"
  }
}
```

Colors: W (white), Y (yellow), R (red), O (orange), G (green), B (blue)
Note: Position tracking (1-54) enables validation of mathematical constraints per rubik.pdf

### Visualization Requirements
- Generate images similar to the unfolded cube layout in `images/mathematics-permutation-group.jpg`
- Show all 6 faces in a cross pattern (standard net representation)
- Display position numbers (1-54) overlaid on colored squares
- Show both original position and current position for permutation tracking
- Support dual-mode visualization:
  - Color-only mode for standard view
  - Position-tracking mode showing permutations (like reference image)
- Output formats: PNG, SVG
- Use matplotlib or PIL for image generation

### Solver Requirements
- Validate cube solvability before attempting solution (parity checks)
- Implement layer-by-layer algorithm (as documented in rubik.pdf)
- Consider Kociemba's two-phase algorithm for optimization
- Return solution in standard notation (F, R, U, B, L, D with ', 2 modifiers)
- Ensure all moves preserve parity constraints
- Provide step-by-step solution breakdown
- Track permutation cycles during solving

## Development Guidelines

### Code Quality Standards
1. **Type Hints**: Use typing module for all function signatures
2. **Docstrings**: Google-style docstrings for all public methods
3. **Testing**: Maintain >90% test coverage
4. **Linting**: Use black, flake8, mypy
5. **Error Handling**: Comprehensive validation for JSON input
6. **Logging**: Structured logging with appropriate levels

### Best Practices
1. **Separation of Concerns**: Keep visualization, solving, and model logic separate
2. **Immutability**: Cube state should be immutable; operations return new states
3. **Validation**: Validate cube states (correct number of each color, solvability)
4. **Performance**: Cache computed states, use efficient data structures
5. **Documentation**: Keep README updated, inline comments for complex algorithms

### Git Workflow
- Main branch for stable releases
- Feature branches for new functionality
- Meaningful commit messages following conventional commits
- PR reviews before merging

## Implementation Phases

### Phase 1: Core Model (Priority: High)
- Position-based cube state representation (1-54 tracking)
- Move operations (F, R, U, B, L, D and inverses) with permutation tracking
- Mathematical validation (parity, orientation, solvability)
- JSON serialization/deserialization for hybrid format

### Phase 2: Visualization (Priority: High)
- 2D net visualization with position overlay (1-54)
- Dual-mode rendering (colors + positions like reference image)
- Before/after comparison showing permutations
- Export functionality (PNG, SVG)

### Phase 3: Solver (Priority: High)
- Solvability validation using parity/orientation checks
- Layer-by-layer solver implementation
- Move sequence optimization
- Solution verification with permutation tracking

### Phase 4: Enhancement (Priority: Medium)
- Advanced solving algorithms
- 3D visualization option
- Performance optimizations
- GUI interface (optional)

## Testing Strategy
- Unit tests for all core functions
- Mathematical validation tests (parity, orientation constraints)
- Integration tests for JSON I/O with position tracking
- Visual regression tests for output images
- Performance benchmarks for solver
- Edge cases: invalid states, impossible cubes, parity violations

## Dependencies
```
numpy>=1.21.0          # Efficient array operations
matplotlib>=3.5.0      # Visualization
pillow>=9.0.0         # Image processing
pytest>=7.0.0         # Testing framework
black>=22.0.0         # Code formatting
mypy>=0.950           # Type checking
```

## CLI Interface
```bash
# Visualize a cube
python main.py visualize input.json -o output.png

# Solve a cube
python main.py solve input.json --method=kociemba

# Validate a cube state
python main.py validate input.json

# Generate scrambled cube
python main.py scramble -n 20 -o scrambled.json
```

## Performance Goals
- Visualization: < 1 second for standard resolution
- Solving: < 5 seconds for any valid configuration
- Memory usage: < 100MB for typical operations

## Position Numbering Convention

Each cube face uses **top-left to bottom-right** numbering (reading order):

```
         Up (U)
      1  2  3
      4  5  6
      7  8  9

Left   Front  Right  Back
10 11 12 | 19 20 21 | 28 29 30 | 37 38 39
13 14 15 | 22 23 24 | 31 32 33 | 40 41 42  
16 17 18 | 25 26 27 | 34 35 36 | 43 44 45

        Down (D)
     46 47 48
     49 50 51
     52 53 54
```

**Face Assignments:**
- **U (1-9)**: White (Up face)
- **L (10-18)**: Green (Left face)
- **F (19-27)**: Red (Front face)
- **R (28-36)**: Blue (Right face)
- **B (37-45)**: Orange (Back face)
- **D (46-54)**: Yellow (Down face)

## Mathematical Foundation
This project is based on group theory principles documented in `docs/rubik.pdf`:
- **Parity Constraints**: Only even permutations are reachable (Page 7-8)
- **Orientation Rules**: Corner orientation sum ≡ 0 (mod 3), Edge orientation sum ≡ 0 (mod 2)
- **Total Positions**: 43,252,003,274,489,856,000 valid configurations
- **Impossibility**: ~11/12 of random color arrangements are unsolvable

## Notes for Future Development
- Consider WebAssembly compilation for browser-based solver
- Explore parallel processing for batch operations
- Add support for different cube sizes (2x2, 4x4, etc.)
- Implement pattern recognition for common configurations
- Add educational mode explaining group theory concepts

---
**Key Reference**: Follow group theory constraints from `docs/rubik.pdf` at all times.
Remember to maintain clean, well-documented code and follow the established project structure.