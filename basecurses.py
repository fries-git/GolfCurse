import curses

def draw(stdscr):
    stdscr.addstr(0, 0, "a")

def main(stdscr):
    while True:
        stdscr.clear()
        draw(stdscr)
        stdscr.refresh()

curses.wrapper(main)