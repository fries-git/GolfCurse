import curses

def draw(stdscr, x, y, char):
    stdscr.addstr(x, y, char)

def main(stdscr):
    while True:
        stdscr.clear()
        draw(stdscr)
        stdscr.refresh()

curses.wrapper(main)