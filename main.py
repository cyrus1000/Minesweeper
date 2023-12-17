import pygame
import sys
from cell import Cell
from calcs import measure_distance
import random

""" This is the main file you work on for the project"""

pygame.init()
pygame.font.init()
SCREEN_MIN_SIZE = 750
amount_of_cells = 16  # Can be made to autoadjust after % of ur screen
ROWS = 16
COLUMNS = 16  # The amount of cells is equal in rows and columns, 16x16 (LOCKED)
bomb_chance = 0.1  # Change to prefered value or use default 0.25
revealed = False
value = 0

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
    # This is a good base to go3 from (think about it thoroughly before you code!! We want to create 16x16 list with each object being a cell):
    bomb = round(bomb_chance * (ROWS * COLUMNS))
    mine_location = random.sample(range(ROWS * COLUMNS), bomb)
    count = 0
    for a_row in range(ROWS):
        row = []
        for a_column in range(COLUMNS):
            count = count + 1
            if count in mine_location:
                value = -1
            else:
                value = 0
            my_cell = Cell(
                a_row * CELL_SIZE,
                a_column * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
                ROWS,
                COLUMNS,
                revealed,
                value,
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
            if cell.revealed and cell.value == 0:
                font = pygame.font.SysFont(None, 30)
                text = font.render(str(cell.value), True, WHITE)
                text_rect = text.get_rect(
                    center=(cell.x + CELL_SIZE // 2, cell.y + CELL_SIZE // 2)
                )
                screen.blit(text, text_rect)

    # pass


def draw():
    """This function handles all the drawings to the screen, such as drawing rectangles, objects etc"""
    draw_cells()


def count_mines(row, col):
    count = 0
    for i in range(max(0, row - 1), min(row + 2, ROWS)):
        for j in range(max(0, col - 1), min(col + 2, COLUMNS)):
            if cells[row][col] == -1:
                count = count + 1
    return count


def reveal_empty_cells(row, col):
    for i in range(max(0, row - 1), min(row + 2, ROWS)):
        for j in range(max(0, col - 1), min(col + 2, COLUMNS)):
            # print(f"Checking cell ({i}, {j})")
            if cells[i][j].value == 0 and not cells[i][j].revealed:
                cells[i][j].revealed = True
                cells[i][j].value = count_mines(i, j)
                pygame.draw.rect(
                    screen,
                    (0, 255, 0),  # Change color based on value
                    (
                        cells[i][j].x,
                        cells[i][j].y,
                        cells[i][j].width,
                        cells[i][j].height,
                    ),
                    cells[i][j].cell_thickness,
                    cells[i][j].value,
                )
                # print(f"Empty cell found at ({i}, {j})")
                if cells[i][j] == 0:
                    print(f"Recursively revealing empty cells from ({i}, {j})")
                    reveal_empty_cells(i, j)


def event_handler(event, screen):
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

        if cells[row][col].value == -1:
            print("Game Over!")
            pygame.quit()
            sys.exit()
        elif cells[row][col].value == 0 and not cells[row][col].revealed:
            cells[row][col].revealed = True
            reveal_empty_cells(row, col)
            pygame.display.flip()
            pygame.display.update()
            print("reveal trying")
        else:
            cells[row][col].revealed = True


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
            event_handler(event, screen)
            pygame.display.flip()
        draw()
        pygame.display.flip()

    terminate_program()


if __name__ == "__main__":
    main()
