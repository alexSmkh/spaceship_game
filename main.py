import curses
from tools import get_star_coroutines
from tools import get_fire_animation_coroutine
from tools import get_spaceship_animation_coroutine

import asyncio
from tools import load_file, get_spaceship_animations
from random import randint, choice
from curses_tools import draw_frame, read_controls, get_frame_size

TIC_TIMEOUT = 0.1

#
# def check_possibility_of_movement(canvas, row, column, animation):
#     canvas_rows, canvas_columns = canvas.getmaxyx()
#     border = 1
#     frame_rows, frame_columns = get_frame_size(animation)
#     max_row = canvas_rows - border - frame_rows
#     max_column = canvas_columns - border - frame_columns
#
#     if row < border or row > max_row:
#         return False
#
#     if column <= border or column > max_column:
#         return False
#
#
#
#
# def get_star_coordinates(canvas):
#     border_width = 3
#     amount_of_stars = 50
#     canvas_height, canvas_width = canvas.getmaxyx()
#     star_coordinates = []
#     while len(star_coordinates) <= amount_of_stars:
#         x_coordinate = randint(
#             border_width,
#             canvas_width - border_width
#         )
#         y_coordinate = randint(
#             border_width,
#             canvas_height - border_width
#         )
#         if (y_coordinate, x_coordinate) in star_coordinates:
#             continue
#         star_coordinates.append((y_coordinate, x_coordinate))
#     return star_coordinates
#
#
# def get_star_coroutines(canvas):
#     star_types = ['*', '.', '+', ':']
#     star_coroutines = []
#     star_coordinates = get_star_coordinates(canvas)
#
#     for y_coordinate, x_coordinate in star_coordinates:
#         star_coroutine = blink(
#             canvas,
#             y_coordinate,
#             x_coordinate,
#             symbol=choice(star_types)
#         )
#         star_coroutines.append(star_coroutine)
#     return star_coroutines
#
#
# def get_fire_animation_coroutine(canvas):
#     canvas_height, canvas_width = canvas.getmaxyx()
#     start_moving_y = canvas_height / 2
#     start_moving_x = canvas_width / 2 + 1
#     do_firing = fire(canvas, start_moving_y, start_moving_x)
#     return do_firing

#
# def get_spaceship_animation_coroutine(canvas, animations):
#     canvas_height, canvas_width = canvas.getmaxyx()
#     start_row = canvas_height / 2
#     start_column = canvas_width / 2
#     do_flying = animate_spaceship(canvas, start_row, start_column, animations)
#     return do_flying


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)

    all_coroutines = get_star_coroutines(canvas)
    all_coroutines.append(get_fire_animation_coroutine(canvas))
    animate_spaceship_coroutine = get_spaceship_animation_coroutine(canvas)
    all_coroutines.append(animate_spaceship_coroutine)

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
