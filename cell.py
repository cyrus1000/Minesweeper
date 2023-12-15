import pygame
import random


class Cell:
    """This file contains the cell class representing each square in the game"""

    def __init__(self, x, y, width, height, rows, columns, bomb_chance):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0, 64, 0)  # RGB color
        self.cell_thickness = 2
        self.neighbouring_bombs = 0
        self.selected = False
        self.rows = rows
        self.columns = columns
        self.grid = [[0] * self.columns for _ in range(self.rows)]

        self.cell_center = (
            self.x + self.width // 2,
            self.y + self.width // 2,
        )  # useful for drawing
        self.bomb = round(bomb_chance * (rows * columns))
        self.mine_location = random.sample(range(self.rows * self.columns), self.bomb)
        for loc in self.mine_location:
            row, col = divmod(loc, self.columns)
            self.grid[row][col] = -1

    def draw(self, screen):
        """This method is called in the main.py files draw_cells fkn"""
        # Hint: Should draw each cell, i.e something to do with pygame.draw.rect
        # Later on in the assignment it will do more as well such as drawing X for bombs or writing digits
        # Important: Remember that pygame starts with (0,0) coordinate in upper left corner!
        # pass
        pygame.draw.rect(
            screen,
            "red",
            (self.x, self.y, self.width, self.height),
            self.cell_thickness,
        )
