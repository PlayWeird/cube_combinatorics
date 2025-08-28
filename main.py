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
import json
from pathlib import Path

from src.cube_model import Cube
from src.visualizer import CubeVisualizer
from src.solver import CubeSolver


def visualize_command(args):
    """Handle visualization command."""
    try:
        # Check if input file exists
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
            sys.exit(1)
        
        # Ensure output directory exists
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create visualizer
        visualizer = CubeVisualizer()
        
        print(f"Visualizing cube from {args.input}...")
        
        # Create visualization - always shows both colors and numbers
        visualizer.visualize_from_json(args.input, args.output, show_numbers=True)
        print(f"Generated visualization with colors and numbers: {args.output}")
        
        print("Visualization completed successfully!")
        
    except Exception as e:
        print(f"Error creating visualization: {e}", file=sys.stderr)
        sys.exit(1)


def solve_command(args):
    """Handle solve command."""
    print(f"Solving cube from {args.input} using {args.method} method...")
    # Implementation will be added
    pass


def validate_command(args):
    """Handle validate command."""
    print(f"Validating cube state from {args.input}...")
    # Implementation will be added
    pass


def scramble_command(args):
    """Handle scramble command."""
    try:
        # Ensure output directory exists
        output_dir = Path(args.output).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize cube in solved state
        cube = Cube()
        
        # Check if using specific sequence or random scramble
        if args.sequence:
            # Apply specific move sequence
            move_sequence = args.sequence
            print(f"Applying move sequence: {move_sequence}")
            
            # Split the sequence and apply each move
            moves = move_sequence.split()
            for move in moves:
                cube.apply_move(move)
                
        elif args.moves:
            # Generate random scramble
            scramble_params = {
                'num_moves': args.moves,
                'avoid_redundancy': not args.allow_redundancy if hasattr(args, 'allow_redundancy') else True,
                'min_moves': args.min_moves if hasattr(args, 'min_moves') else 15
            }
            
            if hasattr(args, 'seed') and args.seed is not None:
                scramble_params['seed'] = args.seed
            
            print(f"Generating scrambled cube with {args.moves} moves...")
            move_sequence = cube.scramble(**scramble_params)
            
        else:
            print("Error: Must specify either --moves for random scramble or --sequence for specific moves", file=sys.stderr)
            sys.exit(1)
        
        # Validate cube state
        is_valid, errors = cube.validate_state()
        if not is_valid:
            print("Warning: Generated cube state has validation issues:")
            for error in errors:
                print(f"  - {error}")
        
        # Save to file
        format_version = getattr(args, 'format', '2.0')
        cube.to_json(args.output, format_version, move_sequence)
        
        # Display results
        print(f"Applied sequence: {move_sequence}")
        print(f"Sequence length: {len(move_sequence.split())} moves")
        print(f"Output saved to: {args.output}")
        
        if is_valid:
            print("Validation: ✓ Valid cube state generated")
        else:
            print("Validation: ⚠ Warning - potential issues detected")
            
    except Exception as e:
        print(f"Error generating scramble: {e}", file=sys.stderr)
        sys.exit(1)


def single_move_command(args):
    """Handle single move command."""
    try:
        # Set default output filename if not provided
        if not args.output:
            # Clean the move name for filename (replace ' with p)
            clean_move = args.move.replace("'", "p").replace("2", "2")
            args.output = f"outputs/scrambles/{clean_move}.json"
        
        # Ensure output directory exists
        output_dir = Path(args.output).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize cube in solved state
        cube = Cube()
        
        # Apply the single move
        print(f"Applying move: {args.move}")
        cube.apply_move(args.move)
        
        # Validate cube state
        is_valid, errors = cube.validate_state()
        if not is_valid:
            print("Warning: Generated cube state has validation issues:")
            for error in errors:
                print(f"  - {error}")
        
        # Save to file
        format_version = getattr(args, 'format', '2.0')
        cube.to_json(args.output, format_version, args.move)
        
        # Display results
        print(f"Applied move: {args.move}")
        print(f"Output saved to: {args.output}")
        
        if is_valid:
            print("Validation: ✓ Valid cube state generated")
        else:
            print("Validation: ⚠ Warning - potential issues detected")
            
    except Exception as e:
        print(f"Error applying single move: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Rubik's Cube Combinatorics CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Visualize command
    viz_parser = subparsers.add_parser('visualize', help='Visualize a cube state')
    viz_parser.add_argument('input', help='Input JSON file')
    viz_parser.add_argument('-o', '--output', default='outputs/visualizations/cube_visualization.png', help='Output image file')
    viz_parser.add_argument('--numbered', action='store_true', help='Include position numbers (1-54)')
    viz_parser.add_argument('--format', choices=['png', 'svg'], default='png', help='Output image format')
    
    # Solve command
    solve_parser = subparsers.add_parser('solve', help='Solve a scrambled cube')
    solve_parser.add_argument('input', help='Input JSON file')
    solve_parser.add_argument('--method', default='layer_by_layer', 
                              choices=['layer_by_layer', 'kociemba'],
                              help='Solving method to use')
    solve_parser.add_argument('--verbose', action='store_true', help='Show detailed solution steps')
    
    # Validate command
    val_parser = subparsers.add_parser('validate', help='Validate a cube state')
    val_parser.add_argument('input', help='Input JSON file')
    
    # Scramble command
    scram_parser = subparsers.add_parser('scramble', help='Generate a scrambled cube')
    scram_parser.add_argument('-n', '--moves', type=int, help='Number of random scramble moves (mutually exclusive with --sequence)')
    scram_parser.add_argument('-s', '--sequence', type=str, help='Specific move sequence to apply (e.g., "R U R\' U\'")')
    scram_parser.add_argument('-o', '--output', default='outputs/scrambles/scrambled.json', help='Output JSON file')
    scram_parser.add_argument('--min-moves', type=int, default=15, help='Minimum moves to ensure proper scrambling (random mode only)')
    scram_parser.add_argument('--seed', type=int, help='Random seed for reproducible scrambles (random mode only)')
    scram_parser.add_argument('--format', choices=['1.0', '2.0'], default='2.0', help='JSON format version')
    scram_parser.add_argument('--allow-redundancy', action='store_true', help='Allow consecutive moves on same face (random mode only)')
    scram_parser.add_argument('--include-sequence', action='store_true', help='Store move sequence in metadata (default: true)')
    scram_parser.add_argument('--validation', action='store_true', default=True, help='Include solvability validation in output (default: true)')
    
    # Single move command
    single_parser = subparsers.add_parser('single-move', help='Apply a single move to solved cube')
    single_parser.add_argument('move', help='Single move to apply (F, R, U, B, L, D, F\', R\', etc.)')
    single_parser.add_argument('-o', '--output', help='Output JSON file (default: outputs/scrambles/{move}.json)')
    single_parser.add_argument('--format', choices=['1.0', '2.0'], default='2.0', help='JSON format version')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute the appropriate command
    commands = {
        'visualize': visualize_command,
        'solve': solve_command,
        'validate': validate_command,
        'scramble': scramble_command,
        'single-move': single_move_command
    }
    
    try:
        commands[args.command](args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()