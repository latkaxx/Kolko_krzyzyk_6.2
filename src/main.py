import pygame
import sys
import os
from enum import Enum
from typing import Optional, List, Tuple, Union

# Game constants
WINDOW_SIZE = 800
BOARD_SIZE = 3
CELL_SIZE = WINDOW_SIZE // (BOARD_SIZE * 3)  # Accounting for nested boards
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (128, 128, 128),
    'LIGHT_GRAY': (200, 200, 200),
    'RED': (255, 0, 0),
    'BLUE': (0, 0, 255),
    'GREEN': (0, 255, 0),
    'YELLOW': (255, 255, 0)
}

class PlayerType(Enum):
    SIGMA = 0
    INTEGRAL = 1
    ALPHA = 2
    BETA = 3

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
            # Check row
            if all(self.grid[i][j] and       self.grid[i][0] and isinstance(self.grid[i][j], Node) and 
                   self.grid[i][j].player == self.grid[i][0].player 
                   for j in range(self.size) if self.grid[i][j] is not None):
                if all(self.grid[i][j] is not None for j in range(self.size)):
                    self.winner = self.grid[i][0].player
                    return self.winner
            
            # Check column
            if all(self.grid[j][i] and       self.grid[0][i] and isinstance(self.grid[j][i], Node) and 
                   self.grid[j][i].player == self.grid[0][i].player 
                   for j in range(self.size) if self.grid[j][i] is not None):
                if all(self.grid[j][i] is not None for j in range(self.size)):
                    self.winner = self.grid[0][i].player
                    return self.winner
        
        # Check diagonals
        if all(self.grid[i][i] and self.grid[0][0] and isinstance(self.grid[i][i], Node) and 
               self.grid[i][i].player == self.grid[0][0].player 
               for i in range(self.size) if self.grid[i][i] is not None):
            if all(self.grid[i][i] is not None for i in range(self.size)):
                self.winner = self.grid[0][0].player
                return self.winner
                
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

class Game:
    """Main game class managing the extended tic-tac-toe game"""
    
    def __init__(self, player_count: int = 2):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
        pygame.display.set_caption("Extended Tic-Tac-Toe")
        self.clock = pygame.time.Clock()
        
        self.player_count = min(max(player_count, 2), 4)
        self.players = [PlayerType.SIGMA, PlayerType.INTEGRAL, PlayerType.ALPHA, PlayerType.BETA][:self.player_count]
        self.current_player_index = 0
        
        self.root_board = Board(BOARD_SIZE)
        self.active_board = None
        self.game_over = False
        self.winner = None
        
        # UI elements
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def get_current_player(self) -> PlayerType:
        return self.players[self.current_player_index]
    
    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.player_count
    
    def get_board_at_position(self, mouse_pos: Tuple[int, int]) -> Tuple[Optional[Board], Tuple[int, int]]:
        """Get the deepest board and position clicked"""
        x, y = mouse_pos
        
        if y > WINDOW_SIZE:  # Clicked in UI area
            return None, (-1, -1)
        
        # Start from root board
        current_board = self.root_board
        board_x, board_y = 0, 0
        board_size = WINDOW_SIZE
        
        while True:
            cell_size = board_size // current_board.size
            row = (y - board_y) // cell_size
            col = (x - board_x) // cell_size
            
            if row >= current_board.size or col >= current_board.size:
                return None, (-1, -1)
            
            cell = current_board.get_cell(row, col)
            
            if isinstance(cell, Board):
                # Continue deeper
                current_board = cell
                board_x += col * cell_size
                board_y += row * cell_size
                board_size = cell_size
            else:
                # Found the target board and position
                return current_board, (row, col)
    
    def find_next_board(self, last_move: Tuple[int, int]) -> Optional[Board]:
        """Find the next board to play on based on the last move"""
        row, col = last_move
        
        if self.active_board and self.active_board.parent:
            parent = self.active_board.parent
            target_cell = parent.get_cell(row, col)
            
            if isinstance(target_cell, Board):
                return target_cell
            else:
                # Cell is occupied, find next available board
                for offset in range(1, parent.size * parent.size):
                    new_col = (col + offset) % parent.size
                    new_row = row if new_col != col else (row + offset // parent.size) % parent.size
                    
                    target_cell = parent.get_cell(new_row, new_col)
                    if isinstance(target_cell, Board):
                        return target_cell
        
        return None
    
    def handle_click(self, mouse_pos: Tuple[int, int]):
        """Handle mouse click events"""
        if self.game_over:
            return
        
        # Check resign button
        if mouse_pos[1] > WINDOW_SIZE:
            self.resign_current_player()
            return
        
        target_board, position = self.get_board_at_position(mouse_pos)
        
        if target_board is None or position == (-1, -1):
            return
        
        # Check if this is a valid move
        if self.active_board is None:
            # First move - player can choose any deepest board
            deepest_boards = self.get_deepest_boards(self.root_board)
            if target_board in deepest_boards:
                self.active_board = target_board
            else:
                return
        elif target_board != self.active_board:
            return
        
        # Make the move
        row, col = position
        if target_board.place_node(row, col, self.get_current_player()):
            # Check if board is won
            if target_board.check_winner():
                target_board.convert_to_node(target_board.winner)
                
                # Check if root board is won
                if self.root_board.check_winner():
                    self.winner = self.root_board.winner
                    self.game_over = True
                    return
            
            # Determine next board
            next_board = self.find_next_board((row, col))
            self.active_board = next_board
            
            self.next_player()
    
    def get_deepest_boards(self, board: Board) -> List[Board]:
        """Get all deepest level boards"""
        deepest = []
        
        def find_deepest(b: Board, depth: int, max_depth: int):
            current_depth = depth
            has_sub_boards = False
            
            for i in range(b.size):
                for j in range(b.size):
                    if isinstance(b.grid[i][j], Board):
                        has_sub_boards = True
                        find_deepest(b.grid[i][j], depth + 1, max_depth)
            
            if not has_sub_boards and depth >= max_depth:
                deepest.append(b)
        
        # Find maximum depth first
        max_depth = self.get_max_depth(board)
        find_deepest(board, 0, max_depth - 1)
        
        return deepest
    
    def get_max_depth(self, board: Board) -> int:
        """Get maximum depth of nested boards"""
        max_depth = 0
        
        def find_depth(b: Board, depth: int):
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            
            for i in range(b.size):
                for j in range(b.size):
                    if isinstance(b.grid[i][j], Board):
                        find_depth(b.grid[i][j], depth + 1)
        
        find_depth(board, 0)
        return max_depth + 1
    
    def resign_current_player(self):
        """Current player resigns"""
        remaining_players = [p for i, p in enumerate(self.players) if i != self.current_player_index]
        if len(remaining_players) == 1:
            self.winner = remaining_players[0]
            self.game_over = True
        else:
            # Remove current player and continue
            self.players.pop(self.current_player_index)
            self.player_count -= 1
            if self.current_player_index >= len(self.players):
                self.current_player_index = 0
    
    def draw(self):
        """Draw the game state"""
        self.screen.fill(COLORS['WHITE'])
        
        # Draw main board
        self.root_board.display(self.screen, 0, 0, WINDOW_SIZE // BOARD_SIZE)
        
        # Highlight active board
        if self.active_board and not self.game_over:
            # This is simplified - in a full implementation, you'd track the screen position
            pygame.draw.rect(self.screen, COLORS['GREEN'], (0, 0, 50, 50), 3)
        
        # Draw UI
        ui_y = WINDOW_SIZE + 10
        
        if self.game_over:
            if self.winner:
                winner_text = f"Winner: {self.winner.name}"
            else:
                winner_text = "Game Over"
            text = self.font.render(winner_text, True, COLORS['BLACK'])
            self.screen.blit(text, (10, ui_y))
        else:
            current_text = f"Current Player: {self.get_current_player().name}"
            text = self.font.render(current_text, True, COLORS['BLACK'])
            self.screen.blit(text, (10, ui_y))
            
            resign_text = "Click here to resign"
            resign_surface = self.small_font.render(resign_text, True, COLORS['RED'])
            self.screen.blit(resign_surface, (10, ui_y + 40))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reset game
                        self.__init__(self.player_count)
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Create game with 2 players (can be changed to 2-4)
    game = Game(player_count=2)
    game.run()
