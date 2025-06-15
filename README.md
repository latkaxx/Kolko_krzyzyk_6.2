# TicTacToe project 

A group project for subject 'Tools for Team Development' - ToTD - (in polish Narzędzia Pracy Grupowej (NPG)) on the Automation and Robotics course at AGH UST. It is an extended version of a classic TicTacToe game implemented in Python with PyGame. The rules are explained below

## Description

<!-- TODO - Long description -->

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

