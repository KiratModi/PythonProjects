import curses
from curses import wrapper

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    stdscr.clear()
    stdscr.addstr("Hello world!")
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
