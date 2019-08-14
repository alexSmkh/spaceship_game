import asyncio
import curses

from game_entities.explosion import Explosion
from game_entities.obstacle import has_collision
from game_entities.scenario import show_game_over
from tools.utils import get_animations
from tools.curses_tools import draw_frame, read_controls, get_frame_size, \
    get_possible_coordinates
from game_entities.bullet import Bullet
from game_entities import global_variables as const
from game_entities.physics import update_speed


class Spaceship:

    def __init__(self, start_row, start_column):
        self.row = start_row
        self.column = start_column
        self.row_speed = 0
        self.column_speed = 0
        self.shots = list()
        self.state = None
        self.possible_states = get_animations('spaceship')

    async def run(self, canvas):
        while True:
            draw_frame(canvas, self.row, self.column, self.state)
            previous_spaceship_state = self.state
            await asyncio.sleep(0)

            row_direction, column_direction, space = read_controls(canvas)

            if space and (const.year >= 2020):
                # -1: shift the animation to see explosion during a shot
                # 2: shift the animation to a shot was out of the gun
                new_bullet = Bullet(self.row - 1, self.column + 2)
                self.shots.append(new_bullet)
                const.coroutines.append(new_bullet.fly(canvas))
                curses.beep()

            self.row_speed, self.column_speed = update_speed(
                self.row_speed,
                self.column_speed,
                row_direction,
                column_direction
            )

            for obstacle in const.obstacles:
                is_collision = has_collision(
                    (obstacle.row, obstacle.column),
                    (obstacle.rows_size, obstacle.columns_size),
                    (self.row, self.column)
                )
                if is_collision:
                    draw_frame(
                        canvas,
                        self.row,
                        self.column,
                        previous_spaceship_state,
                        True
                    )
                    rows_size, columns_size = get_frame_size(self.state)
                    explosion = Explosion(
                        self.row + rows_size / 2,
                        self.column + rows_size / 2
                    )
                    await explosion.explode(canvas)
                    const.coroutines.append(show_game_over(canvas))
                    return

            draw_frame(canvas, self.row, self.column, previous_spaceship_state, True)
            self.row, self.column = get_possible_coordinates(
                canvas,
                self.row + self.row_speed,
                self.column + self.column_speed,
                self.state
            )

    async def animate(self):
        while True:
            for self.state in self.possible_states:
                await asyncio.sleep(0)
