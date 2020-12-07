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
```python
sum_grid = np.sum(np.power(grid, 2))
```

### 2. Emptiness

![Alt text](Image/emptiness.jpg?raw=true)

Next move should make as mans as empty cells so that the number of spaces to move become greater and the percentage of losing the game become smaller.

### 3. Monotonicity

![Alt text](Image/goodmonotonicity.jpg?raw=true)

![Alt text](Image/badmonotonicity.jpg?raw=true)

The first image represents good monotonicity and the second image represents bad monotonicity.
The tile with the greatest number should be placed in a corner and next tiles should be smaller and smaller. For example, in the first image, the greatest number 512 is placed in right-upper corner and tiles are placed in order to decrease (up to down, right to left). However, in the second image, all tiles are placed randomly. There is a 4 in left-bottom corner. It is stucked around 16 so it just occupies a space and cannot be merged with other 4 tiles.

Monotonicity can be caluclatated in four directions: Up, Right, Down, Left. For example, if in rows, calcualte values of current row and next row, then compare two values, if current row value is greater than the next row value, monotonocity appeares in up direction. Otherwise, monotonicy appreaes in down direction. Monotonicity for right and left direction can also be calculated with same method in columns.
```python
for x in range(4):  
        current_row = 0
        next_row = current_row + 1
        while next_row < 4:
            while next_row < 3:
                next_row += 1
            current_cell = grid[current_row, x]
            current_cell_value = math.log(current_cell, 2) if current_cell else 0
            next_cell = grid[next_row,x]
            next_cell_value = math.log(next_cell, 2) if next_cell else 0
            if current_cell_value > next_cell_value:
                monotonicity_up += (next_cell_value - current_cell_value)
            elif next_cell_value > current_cell_value:
                monotonicity_down += (current_cell_value - next_cell_value)
            current_row = next_row
            next_row += 1
```

### 4. Smoothness

![Alt text](Image/smoothness.jpg?raw=true)

If tiles next to each other have a similar number, then it means smoothness is good. So, in other words, it the smoothness is good, then tiles can be merged.
```python
    smoothness = 0
    s_grid = np.sqrt(grid)

    smoothness -= np.sum(np.abs(s_grid[:, 0] - s_grid[:, 1]))
    smoothness -= np.sum(np.abs(s_grid[:, 1] - s_grid[:, 2]))
    smoothness -= np.sum(np.abs(s_grid[:, 2] - s_grid[:, 3]))
    smoothness -= np.sum(np.abs(s_grid[0, :] - s_grid[1, :]))
    smoothness -= np.sum(np.abs(s_grid[1, :] - s_grid[2, :]))
    smoothness -= np.sum(np.abs(s_grid[2, :] - s_grid[3, :]))
```
For example, calculate the sum of absolute value of subtracting column 1 from column 0. If the value is large, then it means the difference of column 0 value and column 1 value is great. It refers the smoothness is bad.

## Sources
* Python 2048 packages: https://pypi.org/project/2048/
* Algorithm  inspired by: https://stackoverflow.com/a/22389702
