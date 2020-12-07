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
1. Download and install Xming utility for graphical environment(https://sourceforge.net/projects/xming/)
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

## 2048 Game Rules
* Board can be moved in four directions: UP, RIGHT, DOWN, LEFT
* All tile moves to the direction where board is moved
* If there is a tile with the same number in moved direction, it can be merged (example: 4 + 4 = 8)
* Every time the board is moved, a new tile is created
  * A tile with a number **2** is created with 90%
  * A tile with a number **4** is created with 10%
  
  
## Huristics
### 1. Big

![Alt text](Image/big.jpg?raw=true)

Next move should make a big number. For example, moving left or right (4096 + 4096) is better than moving up and down (4 + 4)

### 2. Emptiness

![Alt text](Image/emptiness.jpg?raw=true)

Next move should make as mans as empty cells so that the number of spaces to move become greater and the percentage of losing the game become smaller.

### 3. Monotonicity

![Alt text](Image/goodmonotonicity.jpg?raw=true)

![Alt text](Image/badmonotonicity.jpg?raw=true)

The first image represents good monotonicity and the second image represents bad monotonicity.
The tile with the greatest number should be placed in a corner and next tiles should be smaller and smaller. For example, in the first image, the greatest number 512 is placed in right-upper corner and tiles are placed in order to decrease (up to down, right to left). However, in the second image, all tiles are placed randomly. There is a 4 in left-bottom corner. It is stucked around 16 so it just occupies a space and cannot be merged with other 4 tiles.

### 4. Smoothness

![Alt text](Image/smoothness.jpg?raw=true)

If tiles next to each other have a similar number, then it means smoothness is good. So, in other words, it the smoothness is good, then tiles can be merged.


## Sources
* Python 2048 packages: https://pypi.org/project/2048/
* Algorithm  inspired by: https://stackoverflow.com/a/22389702
