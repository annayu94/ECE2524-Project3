# ECE2524 Project3 - Anna Yu
## What if AI plays 2048 game?
This program plays 2048 game itself. Using heuristic search, program will learn and find out solutions itself.
It will determine how 2048 board is well composed and decided which direction it will choose for next move (Up, Down, Right, Left).
For this progject, maximize algorithm was used as a base algorithm.

## How to run? (Instruction)
* prerequisite: python version (3.8.1), pygame version (2.0.0.dev6), SDL version (2.0.10)
* Python Module needed: 2048
``` 
  python3 -m pip install 2048
```  
1. Download and install Xming utility for graphical environment
  - https://sourceforge.net/projects/xming/
2. Launch Xming
3. Run the following commands to activate
```
  sudo apt-get update  
  sudo apt install python3-tk
  export DISPLAY=localhost:0.0
```  
4. Run python program
```  
  python3 run_game.py
```
