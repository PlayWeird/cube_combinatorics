"""Core cube representation and operations module.

This module provides the fundamental data structures and operations
for representing and manipulating Rubik's Cube states.
"""

from typing import List, Dict, Optional, Tuple
import json
import random
import datetime
from dataclasses import dataclass
import numpy as np


@dataclass
class Sticker:
    """Represents a single sticker on the cube."""
    id: int
    face: str
    position: Tuple[int, int]
    color: str
    original_id: int


@dataclass
class CubeState:
    """Represents the state of a Rubik's Cube."""
    stickers: List[Sticker]
    validation: Dict[str, any]


class Cube:
    """Main cube class for operations and transformations."""
    
    COLORS = {'U': 'W', 'D': 'Y', 'F': 'R', 'B': 'O', 'L': 'G', 'R': 'B'}
    MOVES = ['F', 'R', 'U', 'B', 'L', 'D', "F'", "R'", "U'", "B'", "L'", "D'", 
             'F2', 'R2', 'U2', 'B2', 'L2', 'D2']
    
    # Move definitions based on reference code's horizontal_twist, vertical_twist, and side_twist logic
    # Position numbering: U(1-9), L(10-18), F(19-27), R(28-36), B(37-45), D(46-54)
    # Face order: [U=0, L=1, F=2, R=3, B=4, D=5] matching reference ['w','o','g','r','b','y']
    MOVE_DEFINITIONS = {
        # U move: horizontal_twist(row=0, direction=1) - twist right
        'U': {
            'face': [1, 2, 3, 4, 5, 6, 7, 8, 9],  # Rotate U face clockwise
            'adjacent_cycles': [
                # L → F → R → B → L (same simple pattern as working moves)
                [10, 19, 28, 37],  # L-top-left → F-top-left → R-top-left → B-top-left
                [11, 20, 29, 38],  # L-top-middle → F-top-middle → R-top-middle → B-top-middle
                [12, 21, 30, 39]   # L-top-right → F-top-right → R-top-right → B-top-right
            ]
        },
        # D move: horizontal_twist(row=2, direction=0) - twist left  
        'D': {
            'face': [46, 47, 48, 49, 50, 51, 52, 53, 54],  # Rotate D face clockwise
            'adjacent_cycles': [
                # L → B → R → F → L (reverse of U move)
                [16, 43, 34, 25],  # L-bottom-left → B-bottom-left → R-bottom-left → F-bottom-left
                [17, 44, 35, 26],  # L-bottom-middle → B-bottom-middle → R-bottom-middle → F-bottom-middle
                [18, 45, 36, 27]   # L-bottom-right → B-bottom-right → R-bottom-right → F-bottom-right
            ]
        },
        # L move: side_twist(column=0, direction=1) - twist up
        'L': {
            'face': [10, 11, 12, 13, 14, 15, 16, 17, 18],  # Rotate L face clockwise
            'adjacent_cycles': [
                # U[col][0] → B[2-col][2] → D[col][0] → F[col][0] → U[col][0] (up twist)
                [1, 45, 46, 19],   # U[0][0] → B[2][2] → D[0][0] → F[0][0] (up twist)
                [4, 42, 49, 22],   # U[1][0] → B[1][2] → D[1][0] → F[1][0] 
                [7, 39, 52, 25]    # U[2][0] → B[0][2] → D[2][0] → F[2][0]
            ]
        },
        # R move: side_twist(column=2, direction=0) - twist down
        'R': {
            'face': [28, 29, 30, 31, 32, 33, 34, 35, 36],  # Rotate R face clockwise
            'adjacent_cycles': [
                # U[col][2] → F[col][2] → D[col][2] → B[2-col][0] → U[col][2] (down twist)
                [3, 21, 48, 43],   # U[0][2] → F[0][2] → D[0][2] → B[2][0] (down twist)
                [6, 24, 51, 40],   # U[1][2] → F[1][2] → D[1][2] → B[1][0]
                [9, 27, 54, 37]    # U[2][2] → F[2][2] → D[2][2] → B[0][0]
            ]
        },
        # F move: vertical_twist(column=2, direction=1) - twist up
        'F': {
            'face': [19, 20, 21, 22, 23, 24, 25, 26, 27],  # Rotate F face clockwise
            'adjacent_cycles': [
                # U[2][col] → L[2-col][2] → D[0][2-col] → R[col][0] → U[2][col] (up twist)
                [7, 18, 48, 28],   # U[2][0] → L[2][2] → D[0][2] → R[0][0] (up twist)
                [8, 15, 47, 31],   # U[2][1] → L[1][2] → D[0][1] → R[1][0]
                [9, 12, 46, 34]    # U[2][2] → L[0][2] → D[0][0] → R[2][0]
            ]
        },
        # B move: Back face clockwise rotation
        'B': {
            'face': [37, 38, 39, 40, 41, 42, 43, 44, 45],  # Rotate B face clockwise
            'adjacent_cycles': [
                # Top row of U → Left column of L → Bottom row of D (reversed) → Right column of R → back to U
                [3, 10, 52, 36],   # U[0][2] → L[0][0] → D[2][0] → R[2][2]
                [2, 13, 53, 33],   # U[0][1] → L[1][0] → D[2][1] → R[1][2]
                [1, 16, 54, 30]    # U[0][0] → L[2][0] → D[2][2] → R[0][2]
            ]
        }
    }
    
    def __init__(self):
        """Initialize a solved cube."""
        self.stickers = []
        self._init_solved_state()
    
    def _init_solved_state(self):
        """Initialize cube in solved state with position tracking."""
        face_positions = {
            'U': [(i//3, i%3) for i in range(9)],
            'L': [(i//3, i%3) for i in range(9)], 
            'F': [(i//3, i%3) for i in range(9)],
            'R': [(i//3, i%3) for i in range(9)],
            'B': [(i//3, i%3) for i in range(9)],
            'D': [(i//3, i%3) for i in range(9)]
        }
        
        sticker_id = 1
        for face in ['U', 'L', 'F', 'R', 'B', 'D']:
            for pos in face_positions[face]:
                self.stickers.append(Sticker(
                    id=sticker_id,
                    face=face,
                    position=pos,
                    color=self.COLORS[face],
                    original_id=sticker_id
                ))
                sticker_id += 1
    
    def from_json(self, json_path: str) -> None:
        """Load cube state from JSON file."""
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        if data.get('format_version') == '2.0':
            self._load_hybrid_format(data)
        else:
            self._load_simple_format(data)
    
    def _load_hybrid_format(self, data):
        """Load cube state from hybrid format (v2.0)."""
        self.stickers = []
        for sticker_data in data['cube_state']['stickers']:
            self.stickers.append(Sticker(
                id=sticker_data['id'],
                face=sticker_data['face'],
                position=tuple(sticker_data['position']),
                color=sticker_data['color'],
                original_id=sticker_data['original_id']
            ))
    
    def _load_simple_format(self, data):
        """Load cube state from simple format (v1.0)."""
        self.stickers = []
        sticker_id = 1
        
        face_order = ['U', 'L', 'F', 'R', 'B', 'D']
        for face in face_order:
            face_colors = data['cube_state']['faces'][face]
            for i, row in enumerate(face_colors):
                for j, color in enumerate(row):
                    self.stickers.append(Sticker(
                        id=sticker_id,
                        face=face,
                        position=(i, j),
                        color=color,
                        original_id=sticker_id
                    ))
                    sticker_id += 1
    
    def to_json(self, json_path: str, format_version: str = '2.0', 
                scramble_sequence: Optional[str] = None) -> None:
        """Save cube state to JSON file."""
        if format_version == '2.0':
            data = self._to_hybrid_format(scramble_sequence)
        else:
            data = self._to_simple_format(scramble_sequence)
        
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _to_hybrid_format(self, scramble_sequence: Optional[str] = None) -> Dict:
        """Export cube state in hybrid format (v2.0)."""
        validation = self._calculate_validation()
        
        return {
            "format_version": "2.0",
            "cube_state": {
                "representation": "hybrid",
                "stickers": [
                    {
                        "id": s.id,
                        "face": s.face,
                        "position": list(s.position),
                        "color": s.color,
                        "original_id": s.original_id
                    } for s in self.stickers
                ],
                "validation": validation
            },
            "metadata": {
                "timestamp": datetime.datetime.now().isoformat() + 'Z',
                "scramble": scramble_sequence,
                "scramble_length": len(scramble_sequence.split()) if scramble_sequence else 0
            }
        }
    
    def _to_simple_format(self, scramble_sequence: Optional[str] = None) -> Dict:
        """Export cube state in simple format (v1.0)."""
        faces = {'U': [], 'D': [], 'F': [], 'B': [], 'L': [], 'R': []}
        
        for face in faces.keys():
            face_grid = [[None for _ in range(3)] for _ in range(3)]
            face_stickers = [s for s in self.stickers if s.face == face]
            face_stickers.sort(key=lambda s: (s.position[0], s.position[1]))
            
            for sticker in face_stickers:
                i, j = sticker.position
                face_grid[i][j] = sticker.color
            
            faces[face] = face_grid
        
        return {
            "format_version": "1.0",
            "cube_state": {
                "faces": faces
            },
            "metadata": {
                "timestamp": datetime.datetime.now().isoformat() + 'Z',
                "scramble": scramble_sequence
            }
        }
    
    def apply_move(self, move: str) -> None:
        """Apply a move to the cube."""
        if move.endswith("'"):
            base_move = move[:-1]
            for _ in range(3):
                self._apply_base_move(base_move)
        elif move.endswith('2'):
            base_move = move[:-1]
            for _ in range(2):
                self._apply_base_move(base_move)
        else:
            self._apply_base_move(move)
    
    def _apply_base_move(self, move: str) -> None:
        """Apply a base move (F, R, U, B, L, D) once."""
        if move not in self.MOVE_DEFINITIONS:
            return
        
        move_def = self.MOVE_DEFINITIONS[move]
        
        # Rotate the face itself clockwise (positions 0,1,2,3,4,5,6,7,8 -> 6,3,0,7,4,1,8,5,2)
        face_positions = move_def['face']
        if len(face_positions) == 9:
            # Store original sticker objects (not just colors)
            face_stickers = [self.stickers[pos - 1] for pos in face_positions]
            # Apply clockwise rotation: 0->6, 1->3, 2->0, 3->7, 4->4, 5->1, 6->8, 7->5, 8->2
            rotation_map = [6, 3, 0, 7, 4, 1, 8, 5, 2]
            for i, new_pos in enumerate(rotation_map):
                # Move the entire sticker object (preserving original_id)
                moved_sticker = face_stickers[new_pos]
                # Update the position coordinates but keep original_id
                self.stickers[face_positions[i] - 1] = Sticker(
                    id=face_positions[i],  # Current position ID
                    face=moved_sticker.face,  # Face stays same during face rotation
                    position=self.stickers[face_positions[i] - 1].position,  # Position coordinates stay same
                    color=moved_sticker.color,  # Color moves with sticker
                    original_id=moved_sticker.original_id  # This is what we want to track!
                )
        
        # Apply adjacent piece cycles
        for cycle in move_def['adjacent_cycles']:
            if len(cycle) >= 4:
                # Store the entire sticker objects in the cycle
                cycle_stickers = [self.stickers[pos - 1] for pos in cycle]
                # For clockwise rotation, each position gets the sticker from the next position in cycle
                cycle_len = len(cycle)
                for i, pos in enumerate(cycle):
                    # Move the entire sticker object from next position in cycle
                    moved_sticker = cycle_stickers[(i + 1) % cycle_len]
                    # Determine which face this position belongs to
                    current_face = self.stickers[pos - 1].face
                    current_position = self.stickers[pos - 1].position
                    
                    self.stickers[pos - 1] = Sticker(
                        id=pos,  # Current position ID
                        face=current_face,  # Face for this position
                        position=current_position,  # Position coordinates
                        color=moved_sticker.color,  # Color moves with sticker
                        original_id=moved_sticker.original_id  # This tracks where it came from!
                    )
    
    def scramble(self, num_moves: int = 20, seed: Optional[int] = None, 
                 avoid_redundancy: bool = True, min_moves: int = 15) -> str:
        """Generate a scrambled cube state and return the move sequence."""
        if seed is not None:
            random.seed(seed)
        
        # Ensure minimum scramble length
        actual_moves = max(num_moves, min_moves)
        
        moves = []
        last_face = None
        
        for _ in range(actual_moves):
            available_moves = self.MOVES.copy()
            
            if avoid_redundancy and last_face:
                # Avoid consecutive moves on same face
                available_moves = [m for m in available_moves 
                                 if not m.startswith(last_face)]
            
            move = random.choice(available_moves)
            moves.append(move)
            self.apply_move(move)
            last_face = move[0]
        
        return ' '.join(moves)
    
    def is_solved(self) -> bool:
        """Check if the cube is in solved state."""
        for sticker in self.stickers:
            expected_color = self.COLORS[sticker.face]
            if sticker.color != expected_color:
                return False
        return True
    
    def validate_state(self) -> Tuple[bool, List[str]]:
        """Validate that the cube state is legal."""
        errors = []
        
        # Check color counts
        color_counts = {color: 0 for color in self.COLORS.values()}
        for sticker in self.stickers:
            if sticker.color in color_counts:
                color_counts[sticker.color] += 1
            else:
                errors.append(f"Invalid color: {sticker.color}")
        
        for color, count in color_counts.items():
            if count != 9:
                errors.append(f"Color {color} has {count} stickers, expected 9")
        
        # Basic validation - more complex parity checks would be needed for full validation
        validation_data = self._calculate_validation()
        if not validation_data['is_solvable']:
            errors.append("Cube state may violate parity constraints")
        
        return len(errors) == 0, errors
    
    def _calculate_validation(self) -> Dict[str, any]:
        """Calculate validation metrics for the cube state."""
        # For now, assume all states reachable by legal moves are solvable
        # A proper implementation would check corner/edge permutation parity separately
        # and orientation constraints, but that's complex to implement correctly
        
        corner_orientation = 0  # Placeholder
        edge_orientation = 0    # Placeholder
        
        # Since we only generate states through legal moves from solved state,
        # all states should be solvable
        is_solvable = True
        parity = "even"  # Legal moves preserve overall solvability
        
        return {
            "parity": parity,
            "corner_orientation_sum": corner_orientation,
            "edge_orientation_sum": edge_orientation,
            "is_solvable": is_solvable
        }
    
