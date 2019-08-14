import asyncio

from tools.async_sleep import sleep
from tools.curses_tools import draw_frame, get_frame_size
from tools.utils import get_animations
from game_entities import global_variables as const

PHRASES = {
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}


async def time_tracker():
    while True:
        await sleep(15)
        const.year += 1


async def show_game_year(canvas):
    _, max_column = canvas.getmaxyx()
    row = 1
    column = 5
    while True:
        draw_frame(
            canvas,
            row,
            column,
            f'Current year - {const.year}'
        )
        last_year = const.year
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, f'Current year - {last_year}', True)


async def show_game_events(canvas):
    description_of_last_event = str()
    _, max_column = canvas.getmaxyx()
    row = 1
    column = None
    padding_right = 6

    while True:
        if const.year in PHRASES:
            if description_of_last_event:
                draw_frame(
                    canvas,
                    row,
                    column,
                    description_of_last_event,
                    True
                )

            year_of_last_event = const.year
            description_of_last_event = \
                f'Last space event: {PHRASES[year_of_last_event]}'
            _, columns_size = get_frame_size(description_of_last_event)
            column = max_column - columns_size - padding_right
            draw_frame(
                canvas,
                row,
                column,
                description_of_last_event
            )
        await asyncio.sleep(0)


async def show_game_over(canvas):
    text = get_animations('game_over')[0]
    rows_size, column_size = get_frame_size(text)
    row_center, column_center = map(lambda x: x // 2, canvas.getmaxyx())
    row = row_center - rows_size // 2
    column = column_center - column_size // 2
    while True:
        draw_frame(canvas, row, column, text)
        await asyncio.sleep(0)


def get_garbage_delay_tics(year):
    if year < 1961:
        return None
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2
