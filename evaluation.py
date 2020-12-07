import pygame, random, math
import numpy as np
from copy import deepcopy
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

def movement(grid, action):
    num_moved = 0
    sum = 0
    for row, column in CELLS[action]:
        for delta_r, delta_c in GET_DELTAS[action](row, column):
            # When the current cell is empty, but desired moving cell has value:
            if not grid[row][column] and grid[delta_r][delta_c]:
                # Move cell to the current title
                grid[row][column], grid[delta_r][delta_c] = grid[delta_r][delta_c], 0
                num_moved += 1
            if grid[delta_r][delta_c]:
                # When desired moving cell can be merged with the current cell
                if grid[row][column] == grid[delta_r][delta_c]:
                    grid[row][column] *= 2
                    grid[delta_r][delta_c] = 0
                    sum += grid[row][column]
                    num_moved += 1
                # When stop moving
                break
    return grid, num_moved, sum

def evaluation(grid, num_empty):
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
            current_cell_value = math.log(current_cell, 2) if current_cell else 0
            next_cell = grid[next_row,x]
            next_cell_value = math.log(next_cell, 2) if next_cell else 0
            if current_cell_value > next_cell_value:
                monotonicity_up += (next_cell_value - current_cell_value)
            elif next_cell_value > current_cell_value:
                monotonicity_down += (current_cell_value - next_cell_value)
            current_row = next_row
            next_row += 1

    for y in range(4):      # Calculate monotonicity for column
        current_column = 0
        next_column = current_column + 1
        while next_column < 4:
            while next_column < 3:
                next_column += 1
            current_cell = grid[y, next_column]
            current_cell_value = math.log(current_cell, 2) if current_cell else 0
            next_cell = grid[y, next_column]
            next_cell_value = math.log(next_cell, 2) if next_cell else 0
            if current_cell_value > next_cell_value:
                monotonicity_left += (next_cell_value - current_cell_value)
            elif next_cell_value > current_cell_value:
                monotonicity_right += (current_cell_value - next_cell_value)
            current_column = next_column
            next_column += 1

    monotonicity = max(monotonicity_up, monotonicity_down) + max(monotonicity_right, monotonicity_left)

    # weight for each new_score
    empty_w = 100000
    smoothness_w = 3
    monotonicity_w = 10000

    total_empty = num_empty * empty_w
    total_smoothness = smoothness ** smoothness_w
    total_monotonicity = monotonicity * monotonicity_w

    total_score += sum_grid
    total_score += total_empty
    total_score += total_smoothness
    total_score += total_monotonicity

    return total_score

def maximize(grid, depth = 0):
    max_score = -np.inf
    best_direction = None

    for m in range(4):      # 4 times: Up, Right, Down, Left
        m_grid = deepcopy(grid)
        m_grid, moved, _ = movement(m_grid, action=m)

        if not moved:
            continue

        new_score = chance(m_grid, depth + 1)

        if new_score >= max_score:
            max_score = new_score
            best_direction = m

    return best_direction, max_score

def chance(grid, depth = 0):
    empty_c = empty_cells(grid)
    num_empty = len(empty_c)

    # If number of empty cells are large, it doesn't need to consider precisely
    if num_empty >= 6 and depth >= 3:
        return evaluation(grid, num_empty)

    # if Number of empty cells are small, it should consider precisely
    if num_empty >= 0 and depth >= 5:
        return evaluation(grid, num_empty)

    if num_empty == 0:
        _, max_score = maximize(grid, depth + 1)
        return max_score

    score_sum = 0

    ## In empty cells, put tile 2 or 4 and calulate the performance of board
    for x, y in empty_c:
        for i in [2, 4]:
            i_grid = deepcopy(grid)
            i_grid[y][x] = i

            _, max_score = maximize(i_grid, depth + 1)

            if i == 2:
                max_score *= (0.9 / num_empty)
            else:
                max_score *= (0.1 / num_empty)

        score_sum += max_score
    return score_sum
