import curses
import time

from tools.coroutine_tools import init_coroutines
from tools.curses_tools import get_canvases
from game_entities.global_variables import coroutines, TIC_TIMEOUT


def draw(canvas):
    scenario_canvas, game_canvas = get_canvases(canvas)

    game_canvas.nodelay(True)
    game_canvas.keypad(True)
    curses.curs_set(False)

    init_coroutines(game_canvas, scenario_canvas)

    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
                game_canvas.border()
                scenario_canvas.border()
            except StopIteration:
                coroutines.remove(coroutine)
        game_canvas.refresh()
        scenario_canvas.refresh()

        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
