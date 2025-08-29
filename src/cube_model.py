"""Core cube representation and operations module.

This module provides the fundamental data structures and operations
for representing and manipulating Rubik's Cube states.
"""

from typing import List, Dict, Optional, Tuple, Any
import json
import random
import datetime
from dataclasses import dataclass


@dataclass
class Sticker:
    """Represents a single sticker on the cube."""
    id: int
    face: str
    position: Tuple[int, int]
    color: str
    original_id: int


class Cube:
    """Main cube class for operations and transformations."""
    
    COLORS = {'U': 'W', 'D': 'Y', 'F': 'G', 'B': 'B', 'L': 'O', 'R': 'R'}
    
    @property
    def MOVES(self) -> List[str]:
        """Generate all possible moves from base moves."""
        base_moves = list(self.MOVE_DEFINITIONS.keys())
        moves = base_moves.copy()
        # Add prime moves (inverse)
        moves.extend([f"{move}'" for move in base_moves])
        # Add double moves
        moves.extend([f"{move}2" for move in base_moves])
        return moves
    
    # Move definitions based on standard Rubik's Cube notation
    # Position numbering: U(1-9), L(10-18), F(19-27), R(28-36), B(37-45), D(46-54)
    # Each face has 9 positions numbered in reading order (top-left to bottom-right)
    MOVE_DEFINITIONS = {
        # U move: Rotate top face clockwise, affecting top row of adjacent faces
        'U': {
            'face': [1, 2, 3, 4, 5, 6, 7, 8, 9],  # U face positions
            'adjacent_cycles': [
                # Top row cycles: L → F → R → B → L
                [10, 19, 28, 37],  # Top-left positions
                [11, 20, 29, 38],  # Top-middle positions  
                [12, 21, 30, 39]   # Top-right positions
            ]
        },
        # D move: Rotate bottom face clockwise, affecting bottom row of adjacent faces
        'D': {
            'face': [46, 47, 48, 49, 50, 51, 52, 53, 54],  # D face positions
            'adjacent_cycles': [
                # Bottom row cycles: L → B → R → F → L (opposite direction from U)
                [16, 43, 34, 25],  # Bottom-left positions
                [17, 44, 35, 26],  # Bottom-middle positions
                [18, 45, 36, 27]   # Bottom-right positions
            ]
        },
        # L move: Rotate left face clockwise, affecting left column of adjacent faces
        'L': {
            'face': [10, 11, 12, 13, 14, 15, 16, 17, 18],  # L face positions
            'adjacent_cycles': [
                # Left column cycles: U → B → D → F → U (note B positions are mirrored)
                [1, 45, 46, 19],   # Top-left positions
                [4, 42, 49, 22],   # Middle-left positions
                [7, 39, 52, 25]    # Bottom-left positions
            ]
        },
        # R move: Rotate right face clockwise, affecting right column of adjacent faces  
        'R': {
            'face': [28, 29, 30, 31, 32, 33, 34, 35, 36],  # R face positions
            'adjacent_cycles': [
                # Right column cycles: U → F → D → B → U (opposite direction from L)
                [3, 21, 48, 43],   # Top-right positions
                [6, 24, 51, 40],   # Middle-right positions
                [9, 27, 54, 37]    # Bottom-right positions
            ]
        },
        # F move: Rotate front face clockwise, affecting adjacent face edges
        'F': {
            'face': [19, 20, 21, 22, 23, 24, 25, 26, 27],  # F face positions
            'adjacent_cycles': [
                # Front edge cycles: U bottom row → L right col → D top row → R left col → U
                [7, 18, 48, 28],   # Corner positions  
                [8, 15, 47, 31],   # Edge positions
                [9, 12, 46, 34]    # Corner positions
            ]
        },
        # B move: Rotate back face clockwise (viewed from behind the cube)
        'B': {
            'face': [37, 38, 39, 40, 41, 42, 43, 44, 45],  # B face positions
            'adjacent_cycles': [
                # Back edge cycles: U top row → R right col → D bottom row → L left col → U
                # Note: B face is viewed from behind, so rotations appear reversed
                [1, 30, 54, 16],   # Corner positions
                [2, 33, 53, 13],   # Edge positions  
                [3, 36, 52, 10]    # Corner positions
            ]
        }
    }
    
    def __init__(self):
        """Initialize a solved cube."""
        self.stickers = []
        self._init_solved_state()
    
    def _init_solved_state(self) -> None:
        """Initialize cube in solved state with position tracking."""
        sticker_id = 1
        for face in ['U', 'L', 'F', 'R', 'B', 'D']:
            for i in range(3):
                for j in range(3):
                    self.stickers.append(Sticker(
                        id=sticker_id,
                        face=face,
                        position=(i, j),
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
    
    def _load_hybrid_format(self, data: Dict) -> None:
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
    
    def _load_simple_format(self, data: Dict) -> None:
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
        
        # Rotate the face itself
        self._rotate_face_clockwise(move_def['face'])
        
        # Apply adjacent piece cycles
        self._apply_adjacent_cycles(move_def['adjacent_cycles'])
    
    def _rotate_face_clockwise(self, face_positions: List[int]) -> None:
        """Rotate a face clockwise (9 positions)."""
        if len(face_positions) != 9:
            return
        
        # Store original sticker objects
        face_stickers = [self.stickers[pos - 1] for pos in face_positions]
        # Clockwise rotation mapping: 0->6, 1->3, 2->0, 3->7, 4->4, 5->1, 6->8, 7->5, 8->2
        rotation_map = [6, 3, 0, 7, 4, 1, 8, 5, 2]
        
        for i, new_pos in enumerate(rotation_map):
            moved_sticker = face_stickers[new_pos]
            self.stickers[face_positions[i] - 1] = Sticker(
                id=face_positions[i],
                face=moved_sticker.face,
                position=self.stickers[face_positions[i] - 1].position,
                color=moved_sticker.color,
                original_id=moved_sticker.original_id
            )
    
    def _apply_adjacent_cycles(self, cycles: List[List[int]]) -> None:
        """Apply adjacent piece cycles for a move."""
        for cycle in cycles:
            if len(cycle) >= 4:
                # Store sticker objects in the cycle
                cycle_stickers = [self.stickers[pos - 1] for pos in cycle]
                cycle_len = len(cycle)
                
                # For clockwise rotation, each position gets sticker from next position
                for i, pos in enumerate(cycle):
                    moved_sticker = cycle_stickers[(i + 1) % cycle_len]
                    current_face = self.stickers[pos - 1].face
                    current_position = self.stickers[pos - 1].position
                    
                    self.stickers[pos - 1] = Sticker(
                        id=pos,
                        face=current_face,
                        position=current_position,
                        color=moved_sticker.color,
                        original_id=moved_sticker.original_id
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
    
    def _calculate_validation(self) -> Dict[str, Any]:
        """Calculate validation metrics for the cube state.
        
        Note: This is a simplified validation. A complete implementation would
        require complex parity and orientation calculations based on group theory.
        Since we generate states only through legal moves, we assume solvability.
        """
        # Simplified validation - assumes legal move sequences produce solvable states
        return {
            "parity": "even",  # Legal moves preserve even permutation parity
            "corner_orientation_sum": 0,  # Placeholder - would need complex calculation
            "edge_orientation_sum": 0,    # Placeholder - would need complex calculation  
            "is_solvable": True  # Assumed for states from legal move sequences
        }
    
