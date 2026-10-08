import curses
import time
import math
import random
def main(stdscr):
    global fired
    fired = False
    floorxshift = random.randint(1,100)
    def floor(a):
        return int(round(math.floor(curses.LINES - 5 - 3 * math.sin((a+floorxshift) / 15))))

    def floorslope(a):
        # See? I guess calculus was useful...
        return -0.2 * math.cos((a + floorxshift) / 15)
    
    holex = 100 
    holey = floor(holex)
    # Clear the screen
    win = False
    camx = 0
    stdscr.clear()
    a = curses.COLS
    flr = "=" * (a - 1)
    ballx, bally = 0, floor(1) - 1
    ballyvel = 0
    ballxvel = 0

    def moveball():
        global fired
        nonlocal bally, ballx, camx, ballyvel, ballxvel
        if bally == floor(ballx) - 1:
            ballxvel = ballxvel * .9
            if abs(ballxvel) < .1 and abs(ballyvel) < .1:
                fired = False
            
        ballx = ballx + ballxvel
        camx = ballx
        
        ballyvel += -.1

        bally = bally - ballyvel
        if bally >= floor(ballx) - 1:
            ballxvel += floorslope(ballx) * 0.2
            ballyvel = 0 - (ballyvel * .65 )
            if ballyvel < .1:   
                ballyvel = 0
            bally = floor(ballx) - 1

        if not fired:
            ballyvel = 0
            ballxvel = 0


    while not win:
        stdscr.clear()

        stdscr.nodelay(True)
        stdscr.keypad(True)

        for x in range(curses.COLS):
            y = floor(x + camx)
            stdscr.addch(y, x, "=")

        stdscr.addstr(math.floor(bally), 1, "•")

        stdscr.addstr(0, 0, f"Arrow keys to adjust shot X/Y power X: {ballxvel} Y: {ballyvel}")
        computex = math.floor(holex-camx)
        if computex >= 0 and computex < curses.COLS:
            stdscr.addstr(holey, computex, "H")
            stdscr.addstr(holey - 1, computex, "|")
            stdscr.addstr(holey - 2, computex, "|")
            stdscr.addstr(holey - 3, computex, "|")
            if computex - 1 >= 0 and computex - 1 < curses.COLS:
                stdscr.addstr(holey - 3, computex - 1, "<")

        if fired:
            moveball()

        stdscr.addstr(1, 0, f"Distance to hole: {str(int(abs(ballx - holex)))}")
        
        key = stdscr.getch()
        if not fired:
            if abs(ballx - holex) < 5:
                win = True
            if curses.KEY_UP == key:
                ballyvel += .05
                ballyvel = round(ballyvel, 2)
                if ballyvel > 2:
                    ballyvel = 2

            if curses.KEY_DOWN == key:
                ballyvel -= .05
                ballyvel = round(ballyvel, 2)
                if ballyvel < 0:
                    ballyvel = 0

            if curses.KEY_LEFT == key:
                ballxvel -= .05
                ballxvel = round(ballxvel, 2)
                if ballxvel < -2:
                    ballxvel = -2

            if curses.KEY_RIGHT == key:
                ballxvel += .05
                ballxvel = round(ballxvel, 2)
                if ballxvel > 2:
                    ballxvel = 2

            if key in (10, 13, curses.KEY_ENTER):
                fired = True

        stdscr.refresh()
        if fired:
            time.sleep(.1)
        else:
            time.sleep(0)

        stdscr.addstr(0, 0, "You Win! YIPPEE!!!")

curses.wrapper(main)