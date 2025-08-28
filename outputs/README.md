# Output Directory Structure

This directory contains all generated files from the Rubik's Cube Combinatorics application.

## Directory Organization

### `/scrambles/`
Generated scrambled cube states in JSON format:
- Format versions: 1.0 (simple) and 2.0 (hybrid with position tracking)
- Contains move sequences and validation data
- Default location for `python main.py scramble` outputs

### `/solutions/`
Generated solution files:
- Step-by-step solving algorithms
- Move sequences and analysis
- Future: solver output files

### `/visualizations/`
Generated cube visualization images:
- PNG and SVG format cube diagrams
- Position-tracked visualizations
- Before/after comparison images
- Future: `python main.py visualize` outputs

## File Naming Conventions

- `scrambled.json` - Default scramble output
- `*_scramble.json` - Named scramble variations
- `*_solution.json` - Solution outputs
- `*_visualization.png` - Image outputs

## Cleanup

Generated files in this directory are safe to delete - they can be regenerated using the CLI commands.