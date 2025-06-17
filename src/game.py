"""
Main game class managing the extended tic-tac-toe game
"""
import pygame
from typing import Optional, List, Tuple
from player_types import PlayerType
from board import Board
from constants import COLORS, WINDOW_SIZE, BOARD_SIZE

class Game:
    """Main game class managing the extended tic-tac-toe game"""
    
    def __init__(self, player_count: int = 2):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
        pygame.display.set_caption("Mind-Bender Tic-Tac-Toe")
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