import curses
import time
def initboard():
    return [[0 for x in range(10)] for y in range(20)]

def set_coord(array, x, y, value):
    array[y][x] = value

def get_coord(array, x, y):
    return array[y][x]

a = initboard()
set_coord(a, 4, 0, "A")


def main(stdscr):
    stdscr.nodelay(True)
    def trydraw(y,x,char):
        try:
            stdscr.addstr(y, x * 2, char)
        except curses.error:
            pass

    def renderboard():
        stdscr.clear()  
        for y, row in enumerate(a):
            for x, cell in enumerate(row):
                if cell == 0:
                    pass
                elif cell == "A":
                    if y + 1 < 20:
                        set_coord(a, x, y, 0)
                        set_coord(a, x, (y + 1), "B")
                    else:
                        trydraw(y,x,"A")
                    
                else:
                    set_coord(a, x, y, "A")
                    trydraw(y,x,"A")

    while True:
        renderboard()
        key = stdscr.getch()
        time.sleep(.1)
        if key == ord("q"):
            break
        stdscr.refresh()

curses.wrapper(main)