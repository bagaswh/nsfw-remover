import math
import curses
import time
from utils import clear_console, print_c


def parse_time(ms):
    units = {
        "days": math.trunc(ms / (1000 * 60 * 60 * 24)),
        "hours": math.trunc(ms / (1000 * 60 * 60)),
        "minutes": math.trunc(ms / (1000 * 60) % 60),
        "seconds": math.trunc(ms / (1000) % 60)
    }

    str = ""
    for key, val in units.items():
        if val > 0:
            str += f"{val} {key} "

    return str


class Estimator:
    def __init__(self):
        self.stdscr = curses.initscr()

        self.total_time = 0
        self.data_count = 0

    def print_c(self, x, y, str):
        self.stdscr.addstr(y, x, str, curses.A_REVERSE)

    def refresh_c(self):
        self.stdscr.clrtoeol()
        self.stdscr.refresh()

    def estimate(self, start, end, current_frame_num, frames_count):
        runtime = end - start
        self.total_time += runtime
        self.data_count += 1
        mean = self.total_time / self.data_count

        self.print_c(0, 0, f"avg processing time: {round(mean, 1)} s")

        frames_delta = frames_count - current_frame_num
        return frames_delta * mean * 1000

    def log_progress(self, start, end, current_frame_num, frames_count):
        percentage = round(current_frame_num / frames_count * 100, 2)
        esimation = self.estimate(start, end, current_frame_num, frames_count)
        self.print_c(0, 1, f"{percentage}% -- "
                     f"{current_frame_num}/{frames_count} frames processed | "
                     f"time remaining: {parse_time(esimation)}")
        self.refresh_c()
