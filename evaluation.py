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

    total_score = 0

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

    for x in range(4):      # Calculate monotonicity for rows
        current_row = 0
        next_row = current_row + 1
        while next_row < 4:
            while next_row < 3:
                next_row += 1
            current_cell = grid[current_row, x]
            current_cell_value = current_cell if current_cell else 0
            next_cell = grid[next_row,x]
            next_cell_value = next_cell if next_cell else 0
            if current_cell_value > next_cell_value:
                monotonicity_up += (next_cell_value - current_cell_value)
            elif next_cell_value > current_cell_value:
                monotonicity_down += (current_cell_value - next_cell_value)
            current_row = next_row
            next += 1

    for y in range(4):      # Calculate monotonicity for column
        current_column = 0
        next_column = current_column + 1
        while next_column < 4:
            while next_column < 3:
                next_column += 1
            current_cell = grid[y, next_column]
            current_cell_value = current_cell if current_cell else 0
            next_cell = grid[y, next_column]
            next_cell_value = next_cell if next_cell else 0
            if current_cell_value > next_cell_value:
                monotonicity_left += (next_cell_value - current_cell_value)
            elif next_cell_value > current_cell_value:
                monotonicity_right += (current_cell_value - next_cell_value)
            current_column = next_column
            next_column += 1

    monotonocity = max(monotonicity_up, monotonicity_down) + max(monotonicity_right, monotonicity_left)

    # weight for each new_score
    empty_w = 100000
    smoothness_w = 3
    monotonicity_w = 10000

    total_empty = num_empty * empty_w
    total_smoothness = smoothness * smoothness_w
    total_monotonicity = monotonicity * monotonicity_w

    total_score += sum_grid
    total_score += total_empty
    total_score += total_smoothness
    total_score += total_monotonicity

    return score

def maximize(grid, depth = 0):

    for m in range(4):
        m_grid = grid.clone()
        m_grid, moved, _ = move(m_grid, action=action)

        if not moved:
            continue

        max_score = (float('-inf'), 0, 0, 0)
        best_direction = None

        new_score = add_new_tile(m_grid, depth + 1)

        if new_score >= max_score:
            max_score = new_score
            best_direction = acton

    return max_score, best_direction
