"""
Main entry point for Mind-Bender Tic-Tac-Toe
"""
import sys
from game import Game

if __name__ == "__main__":
    # Create game with 2 players, 4 can join at most (for bigger N)
    game = Game(player_count=2)
    game.run()
    sys.exit()
