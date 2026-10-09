import curses
import time
import math
import random
def main(stdscr):
    global fired
    fired = False
    allowbounce = True
    floorxshift = random.randint(1,100)
    def floor(a):
        a = a + 2
        if a > 10:
            return int(round(math.floor(curses.LINES - 5 - 3 * math.sin((a+floorxshift) / 15))))
        else:
            return curses.LINES - 9
    def floortype(a):
        a = a + 2
        if floor(a) > curses.LINES - 9:
            b = math.sin((a+floorxshift)/5)
            if b <= .7:
                return ("=")
            elif b <= .9:
                return ("s")
            elif b <= 1:
                return ("w")
        else:
            return ("=")

    def floorslope(a):
        a = a + 2
        # See? I guess calculus was useful...
        return -0.2 * math.cos((a + floorxshift) / 15)

    holex = random.randint(50,500)
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
    putts = 0
    
    def init():
        nonlocal holex, holey, win, camx, ballx, bally, ballyvel, ballxvel, allowbounce, putts
        holex = random.randint(50,200)
        holey = floor(holex)
        # Clear the screen
        win = False
        camx = 0
        stdscr.clear()
        a = curses.COLS
        flr = "=" * (a - 1)
        ballx, bally = 0, floor(3) - 1
        ballyvel = 0
        ballxvel = 0
        putts = 0

    init()

    def moveball():
        global fired
        nonlocal allowbounce
        nonlocal bally, ballx, camx, ballyvel, ballxvel
        if bally == floor(ballx + 3) - 1:
            if (abs(ballx - holex)) >= 10:
                if floortype(ballx) == "=":
                    ballxvel = ballxvel * .9
                elif floortype(ballx) == "s":
                    ballxvel = ballxvel * .1
                    ballyvel = ballyvel * .8
                elif floortype(ballx) == "w":
                    ballyvel = 0
                    ballxvel = 0
                    ballx, bally = 0, floor(3) - 1
                    fired = 0
            elif (abs(ballx - holex)) >= 5:
                ballxvel = ballxvel * .7
            else:
                ballxvel = ballxvel * .05
            if abs(ballxvel) < .075 and abs(ballyvel) < .1:
                fired = False
            
        ballx = ballx + ballxvel
        camx = ballx
        
        ballyvel += -.1

        bally = bally - ballyvel
        if bally >= floor(ballx + 3) - 1:
            if abs(floorslope(ballx + 3)) >= .025:
                ballxvel += floorslope(ballx + 3) * 0.3
            if allowbounce:
                ballyvel = 0 - (ballyvel * .65 )
            if ballyvel < .1:
                allowbounce = False  
                ballyvel = 0
            bally = floor(ballx + 3) - 1

        if not fired:
            ballyvel = 0
            ballxvel = 0

    while True:
        while not win:
            stdscr.clear()

            stdscr.nodelay(True)
            stdscr.keypad(True)

            for x in range(curses.COLS):
                y = floor(x + camx)
                stdscr.addch(y, x, floortype(x + camx))

                for groundy in range(y + 1, curses.LINES):
                    if groundy < curses.LINES - 1 or x < curses.COLS - 1:
                        stdscr.addch(groundy, x, "-")
                
            if 0 <= math.floor(bally) < curses.LINES:
                stdscr.addstr(math.floor(bally), 2, "•-Ball")
            if ballx < holex:
                stdscr.addstr(2, 0, "Hole is on the right.")
            else:
                stdscr.addstr(2, 0, "Hole is on the left.")

            stdscr.addstr(0, 0, f"Arrow keys to adjust shot X/Y power X: {ballxvel} Y: {ballyvel}")
            computex = math.floor(holex-camx)
            if computex >= 0 and computex < curses.COLS:
                stdscr.addstr(holey, computex, "H")
                if holex-ballx >= 25:
                    stdscr.addstr(holey - 1, computex, "|")
                    stdscr.addstr(holey - 2, computex, "|")
                    stdscr.addstr(holey - 3, computex, "|")
                    if computex - 1 >= 0 and computex - 1 < curses.COLS:
                        stdscr.addstr(holey - 3, computex - 1, "<")
            else:
                if computex < 0:
                    stdscr.addstr(holey-1, 0, "-Hole")
                else:
                    stdscr.addstr(holey-1, curses.COLS-5, "Hole-")

            if fired:
                moveball()

            stdscr.addstr(1, 0, f"Distance to hole: {str(int(abs(ballx - holex)))}")
            
            key = stdscr.getch()
            if not fired:
                ymax = 3
                xmax = 4
                if abs(ballx - holex) <= 5:
                    win = True
                    time.sleep(2)
                    
                if curses.KEY_UP == key:
                    ballyvel += .05
                    ballyvel = round(ballyvel, 2)
                    if ballyvel > 3:
                        ballyvel = 3

                if curses.KEY_DOWN == key:
                    ballyvel -= .05
                    ballyvel = round(ballyvel, 2)
                    if ballyvel < 0:
                        ballyvel = 0

                if curses.KEY_LEFT == key:
                    ballxvel -= .05
                    ballxvel = round(ballxvel, 2)
                    if ballxvel < -xmax:
                        ballxvel = -xmax

                if curses.KEY_RIGHT == key:
                    ballxvel += .05
                    ballxvel = round(ballxvel, 2)
                    if ballxvel > xmax:
                        ballxvel = xmax

                if key in (10, 13, curses.KEY_ENTER):
                    fired = True
                    allowbounce = True
                    putts += 1

            stdscr.refresh()
            if fired:
                time.sleep(.1)
            else:
                time.sleep(0)

        while win:
            stdscr.clear()
            stdscr.addstr(0, 0, f"You Win! It took {putts} putts on a {holex} distance hole!")
            stdscr.addstr(1, 0, "Press Enter to play again!")
            stdscr.refresh()

            stdscr.nodelay(False)
            key = stdscr.getch()

            if key in (10, 13, curses.KEY_ENTER):
                win = False
                stdscr.nodelay(True)
            
            init()

curses.wrapper(main)