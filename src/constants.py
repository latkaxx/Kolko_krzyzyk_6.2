"""
Constants and configuration for Mind-Bender Tic-Tac-Toe
"""

WINDOW_SIZE = 600
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