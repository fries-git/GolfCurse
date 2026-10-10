import curses
import time
import random

# Goofing around, pretty much just testing for making plinko.

def init(stdscr):
    height, width = stdscr.getmaxyx()
    return [[0 for x in range(width - 2)] for y in range(height - 2)]

def draw(stdscr, grid):
    stdscr.box()

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 1:
                try:
                    stdscr.addch(y + 1, x + 1, "S")
                except:
                    pass

def movesand(grid, gx, gy):
    for y in range(len(grid) - 2, -1, -1):
        for x, cell in enumerate(grid[y]):
            if cell == 1:
                rand = random.randint(0,1)
                try:
                    if rand == 1:
                        if grid[y + gy][x] == 0:
                            grid[y + gy][x] = 1
                            grid[y][x] = 0
                        elif grid[y + gy][x + 1] == 0:
                            grid[y + gy][x + 1] = 1
                            grid[y][x] = 0
                        elif grid[y + gy][x - 1] == 0:
                            grid[y + gy][x - 1] = 1
                            grid[y][x] = 0
                    else:
                        if grid[y + gy][x] == 0:
                            grid[y + gy][x] = 1
                            grid[y][x] = 0
                        elif grid[y + gy][x - 1] == 0:
                            grid[y + gy][x - 1] = 1
                            grid[y][x] = 0
                        elif grid[y + gy][x + 1] == 0:
                            grid[y + gy][x + 1] = 1
                            grid[y][x] = 0
                except:
                    pass


def main(stdscr):
    grid = init(stdscr)
    stdscr.nodelay(True)
    while True:
        gforcex, gforcey = 0,1
        key = stdscr.getch()
        height, width = stdscr.getmaxyx()
        if key in (curses.KEY_ENTER, 10, 13):
            grid[0][len(grid[0]) // 2] = 1
            grid[0][(len(grid[0]) // 2) + 1] = 1
            grid[0][(len(grid[0]) // 2) - 1] = 1
        else:
            gforcex, gforcey = 0,1
            #time.sleep(0.05)
        stdscr.clear()
        movesand(grid, gforcex, gforcey)
        draw(stdscr, grid)
        stdscr.refresh()
        

curses.wrapper(main)