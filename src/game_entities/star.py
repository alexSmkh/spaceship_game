import curses
import random

from tools.async_sleep import sleep


class Star:

    def __init__(self, row, column, star_type=None):
        self.star_type = random.choice(['*', '.', '+', ':']) \
            if star_type is None else star_type
        self.row = row
        self.column = column

    async def blink(self, canvas, delay):
        canvas.addstr(self.row, self.column, self.star_type, curses.A_DIM)
        await sleep(delay)

        while True:
            canvas.addstr(self.row, self.column, self.star_type, curses.A_DIM)
            await sleep(20)

            canvas.addstr(self.row, self.column, self.star_type,)
            await sleep(10)

            canvas.addstr(self.row, self.column, self.star_type, curses.A_BOLD)
            await sleep(7)

            canvas.addstr(self.row, self.column, self.star_type,)
            await sleep(10)