import random

from game_entities.garbage import fill_orbit_with_garbage
from game_entities.global_variables import coroutines
from game_entities.scenario import time_tracker, show_game_year, \
    show_game_events
from game_entities.star import Star
from game_entities.spaceship import Spaceship
from tools.utils import get_animations


def get_spaceship_coroutines(canvas):
    max_row, max_column = canvas.getmaxyx()
    start_row = max_row / 2
    start_column = max_column / 2 - 2
    spaceship = Spaceship(start_row, start_column)
    return spaceship.animate(), spaceship.run(canvas)


def get_star_coordinates(canvas):
    border_width = 2
    number_of_stars = 100
    max_row, max_column = canvas.getmaxyx()
    star_coordinates = list()
    while len(star_coordinates) <= number_of_stars:
        column = random.randint(
            border_width,
            max_column - border_width
        )
        row = random.randint(
            border_width,
            max_row - border_width
        )
        if (row, column) in star_coordinates:
            continue
        star_coordinates.append((row, column))
    return star_coordinates


def get_star_coroutines(canvas):
    star_coroutines = list()
    star_coordinates = get_star_coordinates(canvas)

    for row, column in star_coordinates:
        star = Star(row, column)
        star_coroutines.append(star.blink(canvas, random.randint(1, 30)))
    return star_coroutines


def get_fill_orbit_with_garbage_coroutine(canvas):
    garbage_frames = get_animations('garbage')
    return fill_orbit_with_garbage(canvas, garbage_frames)


def init_coroutines(game_canvas, scenario_canvas):
    coroutines.extend(get_star_coroutines(game_canvas))
    coroutines.extend(get_spaceship_coroutines(game_canvas))
    coroutines.append(get_fill_orbit_with_garbage_coroutine(game_canvas))
    coroutines.append(time_tracker())
    coroutines.append(show_game_year(scenario_canvas))
    coroutines.append(show_game_events(scenario_canvas))
