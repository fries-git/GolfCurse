import curses
import math
import time
import random

# RIGHT = 0
# LEFT = 1
# UP = 2
# DOWN = 3

def main(stdscr):
    stdscr.keypad(True)
    stdscr.timeout(0)
    while True:
        state = "playing"
        
        height, width = stdscr.getmaxyx()
        snakedir = 0

        applex, appley = height + 4, width
        stdscr.clear()
        length = 3

        snakex = width/2
        snakey = height/2

        snakecoords = []

        stdscr.nodelay(True)

        def moveapple():
            nonlocal applex, appley
            applex = random.randint(1, width - 1)
            appley = random.randint(1, height - 1)

        moveapple()

        def movesnakehead(x,y):
            nonlocal length, state
            nonlocal snakex, snakey
            snakecoords.append((snakex,snakey))
            if len(snakecoords) > length:
                snakecoords.pop(0)
            snakex = int(snakex + x)
            snakey = int(snakey + y)

            if (snakex, snakey) == (applex, appley):
                length += 1
                moveapple()

            if (snakex, snakey) in snakecoords:
                state = "lose"

            if snakex < 1 or snakex > (width - 1):
                state = "lose"
            if snakey < 1 or snakey > (height - 1):
                state = "lose"
            
        def movesnake():
            nonlocal snakedir
            key = stdscr.getch()
            if curses.KEY_RIGHT == key:
                if not snakedir == 1:
                    snakedir = 0
            if curses.KEY_LEFT == key:
                if not snakedir == 0:
                    snakedir = 1
            if curses.KEY_UP == key:
                if not snakedir == 3:
                    snakedir = 2
            if curses.KEY_DOWN == key:
                if not snakedir == 2:
                    snakedir = 3

            if snakedir == 0:
                movesnakehead(1,0)
            if snakedir == 1:
                movesnakehead(-1,0)
            if snakedir == 2:
                movesnakehead(0,-1)
            if snakedir == 3:
                movesnakehead(0, 1)

        def addchar(y,x,char):
            try:
                stdscr.addstr(int(y),int(x), char)
            except curses.error:
                pass
        box_win = curses.newwin(height, width, 0, 0)
        while state == "playing":
            stdscr.erase()
            stdscr.box()

            addchar(snakey, snakex, "H")

            for coord in snakecoords:
                addchar(coord[1], coord[0], "o")

            addchar(1, 1, str(length))
            addchar(appley, applex, "a")
            stdscr.noutrefresh()
            curses.doupdate()

            movesnake()
            time.sleep(0.05)
        
curses.wrapper(main)