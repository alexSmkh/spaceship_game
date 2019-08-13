import asyncio
import curses
from tools.curses_tools import draw_frame, get_frame_size
from tools.utils import get_animations

EXPLOSION_FRAMES = get_animations('explosion')


class Explosion:

    def __init__(self, center_row, center_column):
        self.center_row = center_row
        self.center_column = center_column
        self.corner_row = None
        self.corner_column = None
        self.states = EXPLOSION_FRAMES

    async def explode(self, canvas):
        rows, columns = get_frame_size(self.states[0])
        self.corner_row = self.center_row - rows / 2
        self.corner_column = self.center_column - columns / 2

        curses.beep()
        for state in self.states:
            draw_frame(canvas, self.corner_row, self.corner_column, state)

            await asyncio.sleep(0)
            draw_frame(canvas, self.corner_row, self.corner_column, state, True)
            await asyncio.sleep(0)
