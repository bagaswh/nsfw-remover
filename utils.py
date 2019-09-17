import pathlib
import os
import curses
from operator import itemgetter


def exists(path):
    p = pathlib.Path(path)
    return p.exists()


def clear_console():
    sysname = os.uname().sysname
    if sysname in ("Linux"):
        os.system("printf \"\033c\"")
    else:  # Windows
        os.system("cls")


def sort(predictions, reverse=True):
    return sorted(predictions, key=itemgetter(1), reverse=reverse)


def print_c(stdscr, x, y, str):
    stdscr.addstr(y, x, str, curses.A_REVERSE)


def refresh_c(stdscr):
    stdscr.refresh()
