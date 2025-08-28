# JSON Schema Design for Rubik's Cube Representation

## Design Decision: Position-Based vs Color-Based

After reviewing the mathematical constraints in the rubik.pdf document, we will use a **hybrid approach** that tracks both positions and colors to ensure:
1. Valid cube state detection
2. Parity constraint enforcement  
3. Proper permutation tracking

## Schema Options

### Option 1: Position-Based (Recommended)
Tracks which original position (1-54) each sticker came from, similar to the image example.

```json
{
  "format_version": "1.1",
  "cube_state": {
    "representation": "position_based",
    "positions": {
      "1": {"current_position": 1, "color": "W"},
      "2": {"current_position": 5, "color": "W"},
      // ... positions 1-54
    },
    "faces": {
      "U": [1, 2, 3, 4, 5, 6, 7, 8, 9],     // Position IDs
      "D": [46, 47, 48, 49, 50, 51, 52, 53, 54],
      "F": [10, 11, 12, 19, 20, 21, 28, 29, 30],
      "B": [37, 38, 39, 40, 41, 42, 43, 44, 45],
      "L": [13, 14, 15, 22, 23, 24, 31, 32, 33],
      "R": [16, 17, 18, 25, 26, 27, 34, 35, 36]
    }
  }
}
```

### Option 2: Hybrid (Comprehensive)
Includes both color and position information for complete tracking.

```json
{
  "format_version": "2.0",
  "cube_state": {
    "representation": "hybrid",
    "stickers": [
      {"id": 1, "face": "U", "position": [0, 0], "color": "W", "original_id": 1},
      {"id": 2, "face": "U", "position": [0, 1], "color": "W", "original_id": 2},
      // ... all 54 stickers
    ],
    "validation": {
      "parity": "even",
      "corner_orientation_sum": 0,  // Must be divisible by 3
      "edge_orientation_sum": 0,     // Must be divisible by 2
      "is_solvable": true
    }
  }
}
```

### Option 3: Simple Color (Limited - Not Recommended)
Original approach - cannot detect all impossible states.

```json
{
  "format_version": "1.0",
  "cube_state": {
    "faces": {
      "U": [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"]],
      // ... other faces
    }
  }
}
```

## Mathematical Constraints to Validate

Based on the document's group theory analysis:

1. **Parity Check**: Total permutation must have even parity
2. **Corner Orientation**: Sum of corner twists must be divisible by 3
3. **Edge Orientation**: Sum of edge flips must be divisible by 2
4. **Color Count**: Exactly 9 of each color (6 colors × 9 = 54)
5. **Center Positions**: Centers are fixed relative to each other

## Position Numbering Convention

Following the image example style (1-54):

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

## Recommended Implementation

Use **Option 2 (Hybrid)** because it:
- Tracks both position permutations and colors
- Enables full validation of cube solvability
- Supports visualization with position numbers (like the reference image)
- Maintains compatibility with standard solving algorithms
- Provides debugging information through validation fields

## Validation Algorithm

```python
def validate_cube_state(cube_state):
    """
    Validates cube state based on mathematical constraints.
    Reference: rubik.pdf pages 7-8 on parity
    """
    # 1. Check color count (9 of each)
    # 2. Check permutation parity (must be even)
    # 3. Check corner orientation sum (divisible by 3)
    # 4. Check edge orientation sum (divisible by 2)
    # 5. Verify no single pair swap (impossible due to parity)
    return is_valid, error_messages
```

## Benefits of Position Tracking

1. **Solvability Detection**: Can detect impossible configurations that look valid by color alone
2. **Move Verification**: Can verify that moves preserve parity
3. **Debugging**: Can trace exactly how pieces moved during scrambling
4. **Educational**: Shows the permutation structure of moves
5. **Optimization**: Solver can use position information for better heuristics