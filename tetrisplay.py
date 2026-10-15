import sys

_ROWS = 10
_COLUMNS = 5
_INTERVAL = 0.3
_BLANK = ""
_BLOCK = "\u2588\u2588"
import time
import random

colours = ["", "red", "blue", "yellow", "green", "black", "orange"]
current_dropping_block = [-1, -1, ""]
draw_block = False
game_over = False

def clear_the_terminal():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def build_clean_grid():
    """Reset the tetris grid to empty."""
    random.seed()
    return [[_BLANK for i in range(_ROWS)] for i in range(_COLUMNS)]


def drop_block(grid):
    if current_dropping_block[1] + 1 >= _ROWS:
        grid[current_dropping_block[0]][current_dropping_block[1]] = current_dropping_block[2]
        current_dropping_block[0] = -1
        current_dropping_block[1] = -1
    elif grid[current_dropping_block[0]][current_dropping_block[1] + 1] != _BLANK:
        grid[current_dropping_block[0]][current_dropping_block[1]] = current_dropping_block[2]
        current_dropping_block[0] = -1
        current_dropping_block[1] = -1
    else:
        current_dropping_block[1] += 1

    check_for_game_over(grid)
    if current_dropping_block[0] == -1:
        random_column = get_random_column(grid)
        current_dropping_block[0] = random_column
        current_dropping_block[1] = 0
        current_dropping_block[2] = colours[random.randint(1, 6)]
    return grid

def get_random_column(grid):
    global game_over
    while not game_over:
        column = random.randint(0, _COLUMNS - 1)
        if grid[column][0] != _BLOCK:
            return column
    return -1

def check_for_game_over(grid):
    block_num = 0
    global game_over
    for c in range(_COLUMNS):
        if grid[c][0] == _BLOCK:
            block_num += 1
    if block_num == _COLUMNS:
        game_over = True
        return True
    game_over = False
    return False

def check_for_filled_row(grid):
    numBlocks = 0
    for x in range(_ROWS):
        for y in range(_COLUMNS):
            if grid[y][x] != _BLANK:
                numBlocks += 1
            if numBlocks == _COLUMNS:
                remove_column(x, y, grid)
                move_down_rows(x, y, grid)
        numBlocks = 0

def remove_column(x, y, grid):
    for c in range(_COLUMNS):
        grid[c][x] = _BLANK

def move_down_rows(x, y, grid):
    for c in range(_COLUMNS):
        for r in range(x, 0, -1):
            grid[c][r] = grid[c][r - 1]
        grid[c][0] = _BLANK


def move_block(grid, direction):
    if -1 < current_dropping_block[0] + direction < _COLUMNS:
        if grid[current_dropping_block[0] + direction][current_dropping_block[1]] != _BLOCK:
            current_dropping_block[0] += direction


def display_grid(grid):
    the_columns = tuple(range(0, _COLUMNS))
    the_rows = tuple(range(0, _ROWS))
    for r in the_rows:
        print("|", sep="", end="")
        for c in the_columns:
            if r == current_dropping_block[1] and c == current_dropping_block[0] and draw_block:
                print(_BLOCK, "|", sep="", end="")
            else:
                print(grid[c][r], "|", sep="", end="")
        print()


def show_dropping_block(grid):
    global draw_block
    if current_dropping_block[1] != -1:
        draw_block = True
        display_grid(grid)
        time.sleep(_INTERVAL)
        clear_the_terminal()
        draw_block = False
        display_grid(grid)
        time.sleep(_INTERVAL)
        clear_the_terminal()

def check_cell_state(x, y, grid):
    if current_dropping_block[0] == x and current_dropping_block[1] == y:
        return current_dropping_block[2]
    else:
        return grid[x][y]