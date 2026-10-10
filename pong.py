import curses
import time
def draw(stdscr, x, y, char):
    try:
        stdscr.addstr(y, x, char)
    except:
        pass

# and guess who just realized curses cant do asynchronous key inputs...
# damn...

def main(stdscr):
    ballx, bally = 0, 0
    xs, ys = 1,1
    height, width = stdscr.getmaxyx()
    height, width = height - 1, width - 1
    pongay = 0
    pongby = height

    while True:
        stdscr.clear()
        draw(stdscr, ballx, bally, "o")

        draw(stdscr, 0, pongay, "|")
        draw(stdscr, 0, pongay - 1, "|")
        draw(stdscr, 0, pongay - 2, "|")
        draw(stdscr, 0, pongay + 1, "|")
        draw(stdscr, 0, pongay + 2, "|")

        draw(stdscr, width, pongby, "|")
        draw(stdscr, width, pongby - 1, "|")
        draw(stdscr, width, pongby - 2, "|")
        draw(stdscr, width, pongby + 1, "|")
        draw(stdscr, width, pongby + 2, "|")

        ballx += xs
        bally += ys
        if ballx >= width or ballx <= 0:
            xs = -xs
            ballx += xs
        if bally >= height or bally <= 0:
            ys = -ys
            bally += ys
        
        stdscr.refresh()
        time.sleep(0.05)

curses.wrapper(main)