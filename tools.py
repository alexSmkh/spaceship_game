import os
from random import randint, choice
from async_animations import blink, fire, animate_spaceship


def load_file(path):
    with open(path, 'r') as file_handler:
        animation_file = file_handler.read()
    return animation_file


def get_spaceship_animations():
    path_to_animations = [
        os.path.join(os.getcwd(), 'animations/rocket_frame_1.txt'),
        os.path.join(os.getcwd(), 'animations/rocket_frame_2.txt'),
    ]
    animations = [
        load_file(path_to_animation) for path_to_animation in path_to_animations
    ]
    return animations


def get_spaceship_animation_coroutine(canvas):
    spaceship_animations = get_spaceship_animations()
    canvas_height, canvas_width = canvas.getmaxyx()
    start_row = canvas_height / 2
    start_column = canvas_width / 2 - 2
    return animate_spaceship(
        canvas,
        start_row,
        start_column,
        spaceship_animations
    )


def get_star_coordinates(canvas):
    border_width = 2
    amount_of_stars = 100
    canvas_height, canvas_width = canvas.getmaxyx()
    star_coordinates = []
    while len(star_coordinates) <= amount_of_stars:
        x_coordinate = randint(
            border_width,
            canvas_width - border_width
        )
        y_coordinate = randint(
            border_width,
            canvas_height - border_width
        )
        if (y_coordinate, x_coordinate) in star_coordinates:
            continue
        star_coordinates.append((y_coordinate, x_coordinate))
    return star_coordinates


def get_star_coroutines(canvas):
    star_types = ['*', '.', '+', ':']
    star_coroutines = []
    star_coordinates = get_star_coordinates(canvas)

    for y_coordinate, x_coordinate in star_coordinates:
        star_coroutine = blink(
            canvas,
            y_coordinate,
            x_coordinate,
            randint(1, 30),
            symbol=choice(star_types)
        )
        star_coroutines.append(star_coroutine)
    return star_coroutines


def get_fire_animation_coroutine(canvas):
    canvas_height, canvas_width = canvas.getmaxyx()
    start_moving_y = canvas_height / 2
    start_moving_x = canvas_width / 2
    return fire(canvas, start_moving_y, start_moving_x)