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
    print(f"Visualizing cube from {args.input}...")
    # Implementation will be added
    pass


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
    print(f"Generating scrambled cube with {args.moves} moves...")
    # Implementation will be added
    pass


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
    viz_parser.add_argument('-o', '--output', default='output.png', help='Output image file')
    viz_parser.add_argument('--numbered', action='store_true', help='Include position numbers')
    
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
    scram_parser.add_argument('-n', '--moves', type=int, default=20, help='Number of scramble moves')
    scram_parser.add_argument('-o', '--output', default='scrambled.json', help='Output JSON file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute the appropriate command
    commands = {
        'visualize': visualize_command,
        'solve': solve_command,
        'validate': validate_command,
        'scramble': scramble_command
    }
    
    try:
        commands[args.command](args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()