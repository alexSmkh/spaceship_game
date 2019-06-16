import curses
from tools import get_star_coroutines
from tools import get_fire_animation_coroutine
from tools import get_spaceship_animation_coroutine


TIC_TIMEOUT = 0.1


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)

    all_coroutines = get_star_coroutines(canvas)
    all_coroutines.append(get_fire_animation_coroutine(canvas))
    all_coroutines.append(get_spaceship_animation_coroutine(canvas))

    while True:
        for coroutine in all_coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                all_coroutines.remove(coroutine)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
