import pygame, random, math
import numpy as np
import _2048
from _2048.game import Game2048
from _2048.manager import GameManager

# define evenets for movements
EVENTS = [ pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}),
           pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}),
           pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}),
           pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})]

# define movement of cells
CELLS = [ [(row, column) for column in range(4) for row in range(4)],                # UP
          [(row, column) for row in range(4) for column in range(4 - 1, -1, -1)],    # RIGHT
          [(row, column) for column in range(4) for row in range(4 - 1, -1, -1)],    # DOWN
          [(row, column) for row in range(4) for column in range(4)]]                # LEFT

GET_DELTAS = [ lambda row, column: ((i, column) for i in range(row + 1, 4)),        # UP
               lambda row, column: ((row, i) for i in range(column - 1, -1, -1)),   # RIGHT
               lambda row, column: ((i, column) for i in range(row - 1, -1, -1)),   # DOWN
               lambda row, column: ((row, i) for i in range(column + 1, 4))]        # LEFT

# Calculate empty cells
def empty_cells(grid):
    return [(x, y) for x in range(4) for y in range(4) if not grid[y][x]]

def move(grid, action):
    moved = 0
    sum = 0
    for row, column in CELLS[action]:
        for delta_r, delta_c in GET_DELTAS[action](row, column):
            # When the current cell is empty, but desired moving cell has value:
            if not grid[row][column] and grid[delta_r][delta_c]:
                # Move cell to the current title
                grid[row][column], grid[delta_r][delta_c] = grid[delta_r][delta_c], 0
                moved += 1
            if grid[delta_r][delta_c]:
                # When desired moving cell can be merged with the current cell
                if grid[row][column] == grid[delta_r][delta_c]:
                    grid[row][column] *= 2
                    grid[delta_r][delta_c] = 0
                    sum += grid[row][column]
                    moved+=1
                # When stop moving
                break
    return grid, moved, sum

def evaluatoin(grid, num_empty):
    grid = np.array(grid)

    score = 0

    # Sum of grids
    sum_grid = np.sum(np.power(grid, 2))

    # monotonicity
    monotonicity_up = 0
    monotonicity_right = 0
    monotonicity_down = 0
    monotonicity_left = 0

    # smoothness
    smoothness = 0
    s_grid = np.sqrt(grid)

    smoothness -= np.sum(np.abs(s_grid[:, 0] - s_grid[:, 1]))
    smoothness -= np.sum(np.abs(s_grid[:, 1] - s_grid[:, 2]))
    smoothness -= np.sum(np.abs(s_grid[:, 2] - s_grid[:, 3]))
    smoothness -= np.sum(np.abs(s_grid[0, :] - s_grid[1, :]))
    smoothness -= np.sum(np.abs(s_grid[1, :] - s_grid[2, :]))
    smoothness -= np.sum(np.abs(s_grid[2, :] - s_grid[3, :]))
