"""
Board class representing a tic-tac-toe board that can contain Nodes or sub-Boards
"""
import pygame
from typing import Optional, Tuple, Union
from player_types import PlayerType
from node import Node
from constants import COLORS

class Board:
    """Represents a tic-tac-toe board that can contain Nodes or sub-Boards"""
    
    def __init__(self, size: int = 3, parent: Optional['Board'] = None, parent_position: Optional[Tuple[int, int]] = None):
        self.size = size
        self.parent = parent
        self.parent_position = parent_position
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.winner = None
        self.is_full = False
        
        # Initialize with sub-boards if this is the root board
        if parent is None:
            for i in range(size):
                for j in range(size):
                    self.grid[i][j] = Board(size, self, (i, j))
    
    def place_node(self, row: int, col: int, player: PlayerType) -> bool:
        """Place a node at the specified position"""
        if self.grid[row][col] is None:
            self.grid[row][col] = Node(player, (row, col))
            self.check_winner()
            self.check_full()
            return True
        return False
    
    def get_cell(self, row: int, col: int) -> Union[None, Node, 'Board']:
        """Get the content of a cell"""
        return self.grid[row][col]
    
    def check_winner(self) -> Optional[PlayerType]:
        """Check if there's a winner on this board"""
        if self.winner:
            return self.winner
            
        # Check rows, columns, and diagonals
        for i in range(self.size):
            # Check rows
            if all(self.grid[i][j] and self.grid[i][0] and isinstance(self.grid[i][j], Node) and 
                   self.grid[i][j].player == self.grid[i][0].player 
                   for j in range(self.size) if self.grid[i][j] is not None):
                if all(self.grid[i][j] is not None for j in range(self.size)):
                    self.winner = self.grid[i][0].player
                    return self.winner
            
            # Check columns
            if all(self.grid[j][i] and self.grid[0][i] and isinstance(self.grid[j][i], Node) and 
                   self.grid[j][i].player == self.grid[0][i].player 
                   for j in range(self.size) if self.grid[j][i] is not None):
                if all(self.grid[j][i] is not None for j in range(self.size)):
                    self.winner = self.grid[0][i].player
                    return self.winner
        
        # Diagonal left top -> right bottom 
        if all(self.grid[i][i] and self.grid[0][0] and isinstance(self.grid[i][i], Node) and 
               self.grid[i][i].player == self.grid[0][0].player 
               for i in range(self.size) if self.grid[i][i] is not None):
            if all(self.grid[i][i] is not None for i in range(self.size)):
                self.winner = self.grid[0][0].player
                return self.winner

        # Diagonal right top -> left bottom 
        if all(self.grid[i][self.size-1-i] and self.grid[0][self.size-1] and isinstance(self.grid[i][self.size-1-i], Node) and 
               self.grid[i][self.size-1-i].player == self.grid[0][self.size-1].player 
               for i in range(self.size) if self.grid[i][self.size-1-i] is not None):
            if all(self.grid[i][self.size-1-i] is not None for i in range(self.size)):
                self.winner = self.grid[0][self.size-1].player
                return self.winner
        
        return None
    
    def check_full(self) -> bool:
        """Check if the board is full"""
        self.is_full = all(self.grid[i][j] is not None for i in range(self.size) for j in range(self.size))
        return self.is_full
    
    def convert_to_node(self, player: PlayerType):
        """Convert this board to a winning node"""
        if self.parent and self.parent_position:
            self.parent.grid[self.parent_position[0]][self.parent_position[1]] = Node(player, self.parent_position)
    
    def display(self, surface: pygame.Surface, x: int, y: int, cell_size: int):
        """Display the board on the given surface"""
        # Draw board outline
        pygame.draw.rect(surface, COLORS['BLACK'], (x, y, cell_size * self.size, cell_size * self.size), 2)
        
        # Draw grid lines
        for i in range(1, self.size):
            pygame.draw.line(surface, COLORS['GRAY'], 
                           (x + i * cell_size, y), 
                           (x + i * cell_size, y + cell_size * self.size))
            pygame.draw.line(surface, COLORS['GRAY'], 
                           (x, y + i * cell_size), 
                           (x + cell_size * self.size, y + i * cell_size))
        
        # Draw contents
        for i in range(self.size):
            for j in range(self.size):
                cell_x = x + j * cell_size
                cell_y = y + i * cell_size
                
                if isinstance(self.grid[i][j], Node):
                    self.grid[i][j].display(surface, cell_x, cell_y, cell_size)
                elif isinstance(self.grid[i][j], Board):
                    sub_cell_size = cell_size // self.size
                    self.grid[i][j].display(surface, cell_x, cell_y, sub_cell_size)