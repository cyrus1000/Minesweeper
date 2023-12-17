import pygame
import sys
from cell import Cell
from calcs import measure_distance

""" This is the main file you work on for the project"""

pygame.init()
pygame.font.init()
SCREEN_MIN_SIZE = 500
amount_of_cells = 10  # Can be made to autoadjust after % of ur screen
ROWS = 10
COLUMNS = 10  # The amount of cells is equal in rows and columns, 16x16 (LOCKED)
bomb_chance = 0.25  # Change to prefered value or use default 0.25

CELL_SIZE = SCREEN_MIN_SIZE // amount_of_cells  # how large can each cell be?
READJUSTED_SIZE = CELL_SIZE * amount_of_cells
CELL_WIDTH = CELL_HEIGHT = CELL_SIZE  # Probably not needed, just use cell_size

SCREEN_WIDTH, SCREEN_HEIGHT = READJUSTED_SIZE, READJUSTED_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)

pygame.display.set_caption("MineSweeper")

cells = []


def create_cells():
    """This function is meant to initialy generate all the cells and create the boundaries"""
    # This is a good base to go from (think about it thoroughly before you code!! We want to create 16x16 list with each object being a cell):


    for a_row in range(ROWS):
        row = []
        for a_column in range(COLUMNS):
            my_cell = Cell(
                a_row * CELL_SIZE,
                a_column * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
                ROWS,
                COLUMNS,
                bomb_chance,
            )
            row.append(my_cell)
    
        cells.append(row)

# pass


def draw_cells():
    """In this function we want to draw each cell, i.e call upon each cells .draw() method!"""
    # Hint: take inspiration from the forloop in create_cells to loop over all the cells

    # for a_row in range(amount_of_cells):
    #   row = []
    for a_row in cells:
        for cell in a_row:
            cell.draw(screen)

    # pass


def draw():
    """This function handles all the drawings to the screen, such as drawing rectangles, objects etc"""
    draw_cells()


def count_mines(row, col):
    count = 0
    for i in range(max(0, row - 1), min(row + 2, ROWS)):
        for j in range(max(0, col - 1), min(col + 2, COLUMNS)):
            if cells[row][col].grid[i][j] == -1:
                count += 1
    return count


def reveal_empty_cells(row, col):
    for i in range(max(0, row - 1), min(row + 2, ROWS)):
        for j in range(max(0, col - 1), min(col + 2, COLUMNS)):
            if cells[row][col].grid[i][j] == 0:
                cells[row][col].grid[i][j] = count_mines(i, j)
                if cells[row][col].grid[i][j] == 0:
                    reveal_empty_cells(i, j)


def event_handler(event):
    """This function handles all events in the program"""

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    elif (
        event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
    ):  # Left mouse button
        x, y = event.pos
        col = x // CELL_SIZE
        row = y // CELL_SIZE

        if cells[row][col].grid[row][col] == -1:
            print("Game Over!")
            pygame.quit()
            sys.exit()
        elif cells[row][col].grid[row][col] == 0:
            cells[row][col].grid[row][col] = count_mines(row, col)
            reveal_empty_cells(row, col)
            pygame.display.flip()
            pygame.display.update()
        else:
            cells[row][col].grid[row][col] = count_mines(row, col)


def run_setup():
    """This function is meant to run all code that is neccesary to setup the app, happends only once"""
    create_cells()


def terminate_program():
    """Functionality to call on whenever you want to terminate the program"""
    pygame.quit()
    sys.exit()


def main():
    run_setup()
    # print(my_cell.grid)
    draw()

    while True:
        for event in pygame.event.get():
            event_handler(event)

            # draw()
        pygame.display.flip()
        pygame.display.update()

    terminate_program()


if __name__ == "__main__":
    main()
