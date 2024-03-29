SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas. Erase text instead of drawing if negative=True is specified."""

    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def get_frame_size(text):
    """Calculate size of multiline text fragment. Returns pair (rows number, colums number)"""
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


def get_possible_coordinates(canvas, row, column, animation):
    canvas_rows, canvas_columns = canvas.getmaxyx()
    border = 1
    frame_rows, frame_columns = get_frame_size(animation)
    max_row = canvas_rows - border - frame_rows
    max_column = canvas_columns - border - frame_columns

    if row < border:
        row = border
    elif row > max_row:
        row = max_row

    if column < border:
        column = border
    elif column > max_column:
        column = max_column

    return row, column


def get_canvases(canvas):
    max_row, max_column = canvas.getmaxyx()
    scenario_canvas_height = 3
    scenario_canvas = canvas.derwin(
        scenario_canvas_height,
        max_column,
        max_row - scenario_canvas_height,
        0
    )
    game_canvas = canvas.derwin(
        max_row - scenario_canvas_height,
        max_column,
        0,
        0
    )
    return scenario_canvas, game_canvas


