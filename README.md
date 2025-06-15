# TicTacToe project 

A group project for subject 'Tools for Team Development' - ToTD - (in polish Narzędzia Pracy Grupowej (NPG)) on the Automation and Robotics course at AGH UST. It is an extended version of a classic TicTacToe game implemented in Python with PyGame. The rules are explained below

## Description

**Mind-Bender Tic-Tac-Toe** is a recursive, multi-layered twist on the classic tic-tac-toe game, developed using Python and Pygame. It introduces a deeply nested board structure, strategic depth, and support for up to 4 unique players, each represented by mathematical symbols.

### Game concept

Instead of playing on a single 3×3 grid, each cell of the main board contains another 3×3 board, and each of those may contain further sub-boards—creating a layered hierarchy. Players must win on the lowest-level boards to claim cells in higher-level ones, ultimately aiming to win the root board.

The game supports up to **four players**, each identified with a symbol and color:

Σ (Sigma) – Red
I (Integral) – Blue
α (Alpha) – Green
β (Beta) – Yellow

Turns rotate automatically, and players can resign mid-game. The interface is fully interactive using mouse clicks, with real-time visual feedback, board highlighting, and win detection. The game ends when the root board is won or when only one player remains.

### How to play

1. Run the game (lauching instructions below);
2. Click on any deepest sub-board to make the first move;
3. After each move, your opponent is directed to play in the sub-board that corresponds to the position of your last move: 
*the location of a player’s move determines the sub-board the next player must play in: the row and column of the clicked cell correspond to the next active sub-board’s position within its parent board; if that target sub-board is already won or full, the next player can freely choose any other available deepest board*;
4. Win a sub-board to claim it, and win the root board to win the game;
5. Click **R** to restart, or click the red button at the bottom area to resign (both actions can be performed mid-game);
6. **Have fun!**

## Setup of the environment

### Linux

Open terminal in the main project directory, navigate to the `setup/` folder using:
```bash
cd setup
```

Then run the setup script using following commands:
```bash
chmod +x setup.sh
source setup.sh
```

After that navigate to the main/src directory and run `main.py` file using python that you have at your disposal, that would be:
```bash
cd ../src # or cd ./src if you are currently in the main project directory
python main.py
```

### Windows 

Run setup.bat or setup.ps1 script (it should work by double-clicking either of them), then in the same terminal navigate to \src directory and run the main project file with, like so:
```bat
cd ..\src
python main.py
```

The game has been successfully tested on **Windows 10 and 11** using both the `setup.bat` and `setup.ps1` scripts. If you encounter any issues, consider the following:

-Make sure **Python is added to your system PATH**.

-Use **PowerShell** or **Command Prompt** with administrative privileges if needed.

-If script execution is blocked, enable it in PowerShell with:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
For a temporary bypass without changing global settings, you can alternatively run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

-To run the game, navigate to the src directory and execute:
```bat
cd ..\src
python main.py
```

## Implementation 

<!-- TODO - Implementation details -->

