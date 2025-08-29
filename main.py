#!/usr/bin/env python3
"""
Main CLI entry point for the Rubik's Cube Combinatorics application.

Usage:
    python main.py visualize input.json -o output.png
    python main.py solve input.json --method=layer_by_layer
    python main.py validate input.json
    python main.py scramble -n 20 -o scrambled.json
"""

import argparse
import sys
from pathlib import Path
from typing import Any

from src.cube_model import Cube
from src.visualizer import CubeVisualizer
from src.solver import CubeSolver


def ensure_output_directory(output_path: str) -> None:
    """Ensure the output directory exists for the given file path."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)


def validate_input_file(input_path: str) -> None:
    """Validate that the input file exists."""
    if not Path(input_path).exists():
        print(f"Error: Input file '{input_path}' not found", file=sys.stderr)
        sys.exit(1)


def display_validation_results(is_valid: bool, errors: list) -> None:
    """Display cube state validation results."""
    if not is_valid:
        print("Warning: Generated cube state has validation issues:")
        for error in errors:
            print(f"  - {error}")
    
    if is_valid:
        print("Validation: ✓ Valid cube state generated")
    else:
        print("Validation: ⚠ Warning - potential issues detected")


def save_cube_state(cube: Cube, output_path: str, move_sequence: str, format_version: str = '2.0') -> None:
    """Save cube state to JSON file with validation."""
    ensure_output_directory(output_path)
    
    # Validate cube state
    is_valid, errors = cube.validate_state()
    
    # Save to file
    cube.to_json(output_path, format_version, move_sequence)
    
    # Display results
    print(f"Output saved to: {output_path}")
    display_validation_results(is_valid, errors)


def visualize_command(args: Any) -> None:
    """Handle visualization command."""
    try:
        validate_input_file(args.input)
        ensure_output_directory(args.output)
        
        visualizer = CubeVisualizer()
        
        print(f"Visualizing cube from {args.input}...")
        
        # Create visualization with colors and numbers
        show_numbers = getattr(args, 'numbered', True)
        visualizer.visualize_from_json(args.input, args.output, show_numbers=show_numbers)
        
        print(f"Generated visualization: {args.output}")
        print("Visualization completed successfully!")
        
    except Exception as e:
        print(f"Error creating visualization: {e}", file=sys.stderr)
        sys.exit(1)


def solve_command(args: Any) -> None:
    """Handle solve command."""
    print(f"Solving cube from {args.input} using {args.method} method...")
    # TODO: Implementation will be added when solver is ready
    print("Note: Solver implementation is not yet available")


def validate_command(args: Any) -> None:
    """Handle validate command."""
    try:
        validate_input_file(args.input)
        
        cube = Cube()
        cube.from_json(args.input)
        
        print(f"Validating cube state from {args.input}...")
        is_valid, errors = cube.validate_state()
        
        if is_valid:
            print("✓ Cube state is valid")
        else:
            print("✗ Cube state has validation issues:")
            for error in errors:
                print(f"  - {error}")
                
    except Exception as e:
        print(f"Error validating cube: {e}", file=sys.stderr)
        sys.exit(1)


def apply_move_sequence(cube: Cube, sequence: str) -> None:
    """Apply a sequence of moves to the cube."""
    moves = sequence.split()
    for move in moves:
        cube.apply_move(move)


def generate_random_scramble(cube: Cube, args: Any) -> str:
    """Generate a random scramble sequence."""
    scramble_params = {
        'num_moves': args.moves,
        'avoid_redundancy': not getattr(args, 'allow_redundancy', False),
        'min_moves': getattr(args, 'min_moves', 15)
    }
    
    if hasattr(args, 'seed') and args.seed is not None:
        scramble_params['seed'] = args.seed
    
    print(f"Generating scrambled cube with {args.moves} moves...")
    return cube.scramble(**scramble_params)


def scramble_command(args: Any) -> None:
    """Handle scramble command."""
    try:
        cube = Cube()
        
        # Determine move sequence
        if args.sequence:
            move_sequence = args.sequence
            print(f"Applying move sequence: {move_sequence}")
            apply_move_sequence(cube, move_sequence)
            
        elif args.moves:
            move_sequence = generate_random_scramble(cube, args)
            
        else:
            print("Error: Must specify either --moves for random scramble or --sequence for specific moves", file=sys.stderr)
            sys.exit(1)
        
        # Save cube state with validation
        format_version = getattr(args, 'format', '2.0')
        save_cube_state(cube, args.output, move_sequence, format_version)
        
        # Display sequence info
        print(f"Applied sequence: {move_sequence}")
        print(f"Sequence length: {len(move_sequence.split())} moves")
            
    except Exception as e:
        print(f"Error generating scramble: {e}", file=sys.stderr)
        sys.exit(1)


def get_default_output_path(move: str) -> str:
    """Generate default output filename for a move."""
    # Clean move name for filename (replace ' with prime)
    clean_move = move.replace("'", "prime").replace("2", "2")
    return f"outputs/scrambles/{clean_move}.json"


def single_move_command(args: Any) -> None:
    """Handle single move command."""
    try:
        # Set default output filename if not provided
        output_path = args.output or get_default_output_path(args.move)
        
        cube = Cube()
        
        # Apply the single move
        print(f"Applying move: {args.move}")
        cube.apply_move(args.move)
        
        # Save cube state with validation
        format_version = getattr(args, 'format', '2.0')
        save_cube_state(cube, output_path, args.move, format_version)
        
        print(f"Applied move: {args.move}")
            
    except Exception as e:
        print(f"Error applying single move: {e}", file=sys.stderr)
        sys.exit(1)


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the main argument parser."""
    parser = argparse.ArgumentParser(
        description="Rubik's Cube Combinatorics CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Visualize command
    viz_parser = subparsers.add_parser('visualize', help='Visualize a cube state')
    viz_parser.add_argument('input', help='Input JSON file')
    viz_parser.add_argument('-o', '--output', 
                           default='outputs/visualizations/cube_visualization.png', 
                           help='Output image file')
    viz_parser.add_argument('--numbered', action='store_true', 
                           help='Include position numbers (1-54)')
    
    # Solve command  
    solve_parser = subparsers.add_parser('solve', help='Solve a scrambled cube')
    solve_parser.add_argument('input', help='Input JSON file')
    solve_parser.add_argument('--method', default='layer_by_layer', 
                              choices=['layer_by_layer', 'kociemba'],
                              help='Solving method to use')
    solve_parser.add_argument('--verbose', action='store_true', 
                             help='Show detailed solution steps')
    
    # Validate command
    val_parser = subparsers.add_parser('validate', help='Validate a cube state')
    val_parser.add_argument('input', help='Input JSON file')
    
    # Scramble command
    scram_parser = subparsers.add_parser('scramble', help='Generate a scrambled cube')
    scram_parser.add_argument('-n', '--moves', type=int, 
                             help='Number of random scramble moves')
    scram_parser.add_argument('-s', '--sequence', type=str, 
                             help='Specific move sequence (e.g., "R U R\' U\'")')
    scram_parser.add_argument('-o', '--output', 
                             default='outputs/scrambles/scrambled.json', 
                             help='Output JSON file')
    scram_parser.add_argument('--min-moves', type=int, default=15, 
                             help='Minimum moves for proper scrambling (random mode)')
    scram_parser.add_argument('--seed', type=int, 
                             help='Random seed for reproducible scrambles')
    scram_parser.add_argument('--format', choices=['1.0', '2.0'], default='2.0', 
                             help='JSON format version')
    scram_parser.add_argument('--allow-redundancy', action='store_true', 
                             help='Allow consecutive moves on same face')
    
    # Single move command
    single_parser = subparsers.add_parser('single-move', 
                                         help='Apply a single move to solved cube')
    single_parser.add_argument('move', 
                              help='Single move to apply (F, R, U, B, L, D, etc.)')
    single_parser.add_argument('-o', '--output', 
                              help='Output JSON file (default: auto-generated)')
    single_parser.add_argument('--format', choices=['1.0', '2.0'], default='2.0', 
                              help='JSON format version')
    
    return parser


def main() -> None:
    """Main CLI function."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Command mapping
    commands = {
        'visualize': visualize_command,
        'solve': solve_command,
        'validate': validate_command,
        'scramble': scramble_command,
        'single-move': single_move_command
    }
    
    # Execute command
    try:
        commands[args.command](args)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()