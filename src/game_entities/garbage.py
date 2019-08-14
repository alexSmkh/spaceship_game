import asyncio
import random

from game_entities.explosion import Explosion
from game_entities import global_variables
from game_entities.obstacle import Obstacle
from game_entities.scenario import get_garbage_delay_tics
from tools.async_sleep import sleep
from tools.curses_tools import draw_frame, get_frame_size


class Garbage:

    def __init__(self, row, column, frame):
        self.row = row
        self.column = column
        self.frame = frame

    async def fly_garbage(self, canvas, speed=0.5):
        """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
        rows_number, columns_number = canvas.getmaxyx()

        self.column = max(self.column, 0)
        self.column = min(self.column, columns_number - 1)
        self.row = 0

        rows_size, columns_size = get_frame_size(self.frame)
        obstacle = Obstacle(self.row, self.column, rows_size, columns_size)
        global_variables.obstacles.append(obstacle)
        while self.row < rows_number:
            draw_frame(canvas, self.row, self.column, self.frame)
            if obstacle in global_variables.obstacles_in_last_collisions:
                draw_frame(
                    canvas, self.row, self.column, self.frame, negative=True
                )
                global_variables.obstacles.remove(obstacle)

                explosion = Explosion(
                    self.row + rows_size / 2,
                    self.column + columns_size / 2
                )
                await explosion.explode(canvas)
                return
            await asyncio.sleep(0)
            draw_frame(canvas, self.row, self.column, self.frame, negative=True)
            self.row += speed
            obstacle.row += speed
        global_variables.obstacles.remove(obstacle)


async def fill_orbit_with_garbage(canvas, garbage_frames):
    rows_number, columns_number = canvas.getmaxyx()
    while True:
        if global_variables.year < 1961:
            await asyncio.sleep(0)
            continue
        await sleep(get_garbage_delay_tics(global_variables.year))
        garbage_frame = random.choice(garbage_frames)
        rows_animation_frame, columns_animation_frame = get_frame_size(
            garbage_frame)
        column = random.randint(0, columns_number - columns_animation_frame)

        garbage = Garbage(0, column, garbage_frame)
        global_variables.coroutines.append(garbage.fly_garbage(canvas))
        await asyncio.sleep(0)
