"""
Node class representing a basic tic-tac-toe token
"""
import pygame
import os
from typing import Tuple
from player_types import PlayerType
from constants import COLORS, CELL_SIZE

class Node:
    """Represents a basic tic-tac-toe token"""
    
    def __init__(self, player: PlayerType, position: Tuple[int, int]):
        self.player = player
        self.position = position
        self.image = None
        self.load_image()
    
    def load_image(self):
        """Load player images, fallback to text if images not found"""
        image_files = {
            PlayerType.SIGMA: 'sigma.png',
            PlayerType.INTEGRAL: 'integral.png',
            PlayerType.ALPHA: 'alpha.png',
            PlayerType.BETA: 'beta.png'
        }
        
        try:
            if os.path.exists(image_files[self.player]):
                self.image = pygame.image.load(image_files[self.player])
                self.image = pygame.transform.scale(self.image, (CELL_SIZE - 10, CELL_SIZE - 10))
        except:
            self.image = None
    
    def display(self, surface: pygame.Surface, x: int, y: int, cell_size: int = CELL_SIZE):
        """Display the node on the given surface"""
        if self.image:
            scaled_image = pygame.transform.scale(self.image, (cell_size - 10, cell_size - 10))
            surface.blit(scaled_image, (x + 5, y + 5))
        else:
            # Fallback to text symbols
            symbols = {
                PlayerType.SIGMA: 'Σ',
                PlayerType.INTEGRAL: 'I',
                PlayerType.ALPHA: 'α',
                PlayerType.BETA: 'β'
            }
            colors = {
                PlayerType.SIGMA: COLORS['RED'],
                PlayerType.INTEGRAL: COLORS['BLUE'],
                PlayerType.ALPHA: COLORS['GREEN'],
                PlayerType.BETA: COLORS['YELLOW']
            }
            
            font = pygame.font.Font(None, cell_size // 2)
            text = font.render(symbols[self.player], True, colors[self.player])
            text_rect = text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
            surface.blit(text, text_rect)