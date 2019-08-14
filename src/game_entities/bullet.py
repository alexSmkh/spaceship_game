import asyncio
import curses

from game_entities.obstacle import has_collision
from game_entities import global_variables


class Bullet:

    def __init__(self, row, column):
        self.row = row
        self.column = column

    async def fly(self, canvas, rows_speed=-2, columns_speed=0):
        canvas.addstr(round(self.row), round(self.column), '*')
        await asyncio.sleep(0)

        canvas.addstr(round(self.row), round(self.column), 'O')
        await asyncio.sleep(0)

        canvas.addstr(round(self.row), round(self.column), ' ')

        self.row += rows_speed
        self.column += columns_speed

        symbol = '-' if columns_speed else '|'

        rows, columns = canvas.getmaxyx()
        max_row, max_column = rows - 1, columns - 1

        curses.beep()

        while 1 < self.row < max_row and 0 < self.column < max_column:
            canvas.addstr(round(self.row), round(self.column), symbol)
            for obstacle in global_variables.obstacles:
                is_collision = has_collision(
                    (obstacle.row, obstacle.column),
                    (obstacle.rows_size, obstacle.columns_size),
                    (self.row, self.column)
                )
                if is_collision:
                    global_variables.obstacles_in_last_collisions.append(obstacle)
                    canvas.addstr(round(self.row), round(self.column), ' ')
                    return

            await asyncio.sleep(0)
            canvas.addstr(round(self.row), round(self.column), ' ')
            self.row += rows_speed
            self.column += columns_speed
