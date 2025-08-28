"""
Cube visualization module.

Provides functions to generate visual representations of Rubik's Cube states.
"""

from typing import Optional, Tuple, Dict
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import os


class CubeVisualizer:
    """Handles visualization of Rubik's Cube states."""
    
    # Color mapping for visualization
    COLOR_MAP = {
        'W': '#FFFFFF',  # White
        'Y': '#FFFF00',  # Yellow
        'R': '#FF0000',  # Red
        'O': '#FFA500',  # Orange
        'G': '#00FF00',  # Green
        'B': '#0000FF'   # Blue
    }
    
    # Net layout positions for faces in the standard unfolded cube pattern
    # Layout:    U
    #        L  F  R  B  
    #           D
    NET_LAYOUT = {
        'U': (1, 0),  # Up face - top (after y-flip: 2-0=2, so top)
        'L': (0, 1),  # Left face - middle row left
        'F': (1, 1),  # Front face - middle row center  
        'R': (2, 1),  # Right face - middle row right
        'B': (3, 1),  # Back face - middle row far right
        'D': (1, 2)   # Down face - bottom (after y-flip: 2-2=0, so bottom)
    }
    
    def __init__(self):
        """Initialize the visualizer with default settings."""
        self.fig_size = (12, 9)
        self.square_size = 1.0
        self.gap_size = 0.1
    
    def create_net_visualization(self, cube, output_path: str, 
                                show_numbers: bool = True) -> None:
        """
        Create a 2D net visualization of the cube.
        
        Args:
            cube: The cube object to visualize
            output_path: Path to save the output image
            show_numbers: Whether to show position numbers (1-54)
        """
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:  # Only create directory if there is one
            os.makedirs(output_dir, exist_ok=True)
        
        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=self.fig_size)
        ax.set_xlim(-0.5, 14.5)
        ax.set_ylim(-1.5, 11.0)  # More space for labels
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Extract face data from cube
        face_data = self._extract_face_data(cube)
        
        # Draw each face
        for face_name, (grid_x, grid_y) in self.NET_LAYOUT.items():
            self._draw_face(ax, face_data[face_name], face_name, 
                          grid_x, grid_y, show_numbers, cube)
        
        # Add title
        scramble_info = ""
        if hasattr(cube, '_last_scramble'):
            scramble_info = f" - {cube._last_scramble}"
        
        plt.title(f'Rubik\'s Cube State{scramble_info}', 
                 fontsize=16, fontweight='bold', pad=20)
        
        # Save the figure
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
    
    def create_numbered_visualization(self, cube, output_path: str) -> None:
        """
        Create a visualization with numbered positions (1-54) on colored squares.
        
        Args:
            cube: The cube object to visualize
            output_path: Path to save the output image
        """
        self.create_net_visualization(cube, output_path, show_numbers=True)
    
    def _extract_face_data(self, cube) -> Dict[str, list]:
        """Extract face color data from cube object."""
        face_data = {}
        
        # Map sticker positions to faces
        face_ranges = {
            'U': (0, 9),
            'L': (9, 18),
            'F': (18, 27),
            'R': (27, 36),
            'B': (36, 45),
            'D': (45, 54)
        }
        
        for face_name, (start, end) in face_ranges.items():
            face_stickers = cube.stickers[start:end]
            # Organize into 3x3 grid
            face_grid = []
            for i in range(3):
                row = []
                for j in range(3):
                    sticker_idx = i * 3 + j
                    row.append(face_stickers[sticker_idx].color)
                face_grid.append(row)
            face_data[face_name] = face_grid
            
        return face_data
    
    def _draw_face(self, ax, face_grid, face_name: str, grid_x: int, grid_y: int, 
                   show_numbers: bool = False, cube=None):
        """Draw a single face of the cube."""
        # Calculate base position for this face
        base_x = grid_x * 3.5
        base_y = (2 - grid_y) * 3.5  # Flip Y for correct orientation
        
        # Draw each square in the 3x3 face
        for i in range(3):
            for j in range(3):
                x = base_x + j
                y = base_y + (2 - i)  # Flip i so that i=0 gives top row
                
                # Get color and draw colored square
                color = face_grid[i][j]
                color_hex = self.COLOR_MAP.get(color, '#CCCCCC')
                
                square = patches.Rectangle((x, y), 1, 1,
                                         linewidth=2, edgecolor='black',
                                         facecolor=color_hex)
                ax.add_patch(square)
                
                if show_numbers:
                    # Get the original_id of the sticker at this position
                    face_order = ['U', 'L', 'F', 'R', 'B', 'D']
                    face_idx = face_order.index(face_name)
                    current_position_idx = face_idx * 9 + i * 3 + j  # 0-based index
                    sticker = cube.stickers[current_position_idx]
                    original_number = sticker.original_id
                    
                    # Choose text color for good contrast
                    text_color = 'white' if color in ['R', 'B', 'G'] else 'black'
                    
                    # Add original position number (the number that follows this sticker)
                    ax.text(x + 0.5, y + 0.5, str(original_number),
                           ha='center', va='center', fontsize=10, fontweight='bold',
                           color=text_color)
        
        # Add face label - very close to the face
        label_x = base_x + 1.5
        label_y = base_y - 0.1  # Even closer to the squares
        ax.text(label_x, label_y, face_name, ha='center', va='top',
               fontsize=14, fontweight='bold')
    
    def visualize_from_json(self, json_path: str, output_path: str, 
                           show_numbers: bool = True) -> None:
        """
        Create visualization directly from JSON file.
        
        Args:
            json_path: Path to the cube state JSON file
            output_path: Path to save the output image
            show_numbers: Whether to show position numbers
        """
        from .cube_model import Cube
        
        cube = Cube()
        cube.from_json(json_path)
        
        # Try to extract scramble info from JSON metadata
        import json
        with open(json_path, 'r') as f:
            data = json.load(f)
            scramble = data.get('metadata', {}).get('scramble', '')
            if scramble:
                cube._last_scramble = scramble
        
        self.create_net_visualization(cube, output_path, show_numbers)
    
    def export_as_png(self, figure, output_path: str) -> None:
        """Export visualization as PNG."""
        figure.savefig(output_path, format='png', dpi=300, bbox_inches='tight')
    
    def export_as_svg(self, figure, output_path: str) -> None:
        """Export visualization as SVG."""
        figure.savefig(output_path, format='svg', bbox_inches='tight')