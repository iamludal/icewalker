from json.decoder import JSONDecodeError
from Game import Game, GameState
import pygame

# Constants declarations
CELL_SIZE = 60
BORDER = 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (175, 240, 240)
GRAY = (50, 180, 180)
LEO = pygame.image.load("../images/weinberg.png")
NOE = pygame.image.load("../images/noe.png")
EW = pygame.image.load("../images/ew.png")
MEFT = pygame.image.load("../images/meftali.png")
LEO = pygame.transform.scale(LEO, (CELL_SIZE, CELL_SIZE))
NOE = pygame.transform.scale(NOE, (CELL_SIZE, CELL_SIZE))
EW = pygame.transform.scale(EW, (CELL_SIZE, CELL_SIZE))
MEFT = pygame.transform.scale(MEFT, (CELL_SIZE, CELL_SIZE))
PROF = ["E. Wegrzynowski", "L. Noé", "L. Weinberg", "S. Meftali"]
IMG = [EW, NOE, LEO, MEFT]
KEY_DIRECTIONS = {273: 'N', 274: 'S', 275: 'E', 276: 'W'}


def render_final_cell(win, color, pos):
    """ Render the final cell into the window

    :param win: (pygame.Surface) the window in which to render the final cell
    :param color: (tuple) the fill color of the final cell
    :param pos: (tuple) the final cell's coordinates : (x, y)
    :UC: len(color) == 3 and all(0 <= i <= 255 for i in color)
         len(pos) == 2 and all(0 <= i for i in pos)
    """
    x, y = pos
    pygame.draw.rect(win, color,
                     (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))


def render_wall(win, color, direction, pos):
    """ Render a wall in the window

    :param win: (pygame.Surface) the window in which to render the wall
    :param color: (tuple) the fill color of the wall
    :param direction: (str) the direction of the wall
    :param pos: (tuple) the wall's coordinates: (x, y)
    :UC: direction in {'E', 'S'}
         len(color) == 3 and all(0 <= i <= 255 for i in color)
         len(pos) == 2 and all(0 <= i for i in pos)
    """
    x, y = pos

    if direction == 'S':
        width = CELL_SIZE
        height = BORDER
        x = x*CELL_SIZE
        y = (y+1)*CELL_SIZE

    elif direction == 'E':
        width = BORDER
        height = CELL_SIZE
        x = (x+1)*CELL_SIZE
        y = y*CELL_SIZE

    pygame.draw.rect(win, color, (x, y, width, height))


def render_player(win, player):
    """ Render a player in the window

    :param win: (pygame.Surface) the window in which to render the player
    :param player: (Player) the player to render
    :UC: None
    """
    x, y = player.get_coordinates()
    n = player.get_n()
    win.blit(IMG[n], (x*CELL_SIZE + BORDER, y*CELL_SIZE + BORDER))


def draw_main_surface(win, color, dimensions):
    """ Draw the main surface in the window

    :param win: (pygame.Surface) the window in which to draw the surface
    :param color: (tuple) the color of the surface
    :param dimensions: (tuple) the dimensions of the surface
    :UC: len(color) == 3 and all(0 <= i <= 255 for i in color)
         len(dimensions) == 2 and all(0 <= i for i in dimensions)
    """
    width, height = dimensions

    pygame.draw.rect(win, color, (BORDER, BORDER,
                                  width*CELL_SIZE - BORDER*2,
                                  height*CELL_SIZE - BORDER*2))


def render(win, grid):
    """ Render the grid[grid] of the game in the pygame window[win]

    :param win: (pygame.Surface) the pygame window in which you render the grid
    :param grid: (Grid) the gruid to render
    :UC: None
    """
    width, height = grid.get_width(), grid.get_height()

    win.fill(BLACK)
    draw_main_surface(win, WHITE, (width, height))

    for x in range(width):
        for y in range(height):
            cell = grid.get_cell(x, y)
            walls = cell.get_walls()

            if cell.is_final_cell():
                render_final_cell(win, CYAN, (x, y))

            if not cell.is_empty():
                player = cell.get_content()
                render_player(win, player)

            for wall in walls:
                render_wall(win, BLACK, wall, (x, y))

    pygame.display.update()


def load_file(filename):
    """ Load a game configuration from a JSON file

    :param filename: (str) the path of the file to open
    :return: (dict) the data of the configuration
    :UC: filename.endswith(".json")
    """
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        exit("The file doesn't exist.")
    except JSONDecodeError:
        exit("The file couldn't be decoded.")


def display_winning_screen(win):
    """ Display the winning screen in the window

    :param win: (pygame.Surface) the window in which to render the end screen
    """
    width, height = pygame.display.get_surface().get_size()
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('You win!', True, BLACK)
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 2)

    win.fill(WHITE)
    win.blit(text, textRect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def select_player(n):
    """ Set the pygame window title to the selected player

    :param n: (int) the number of the selected player
    :UC: 0 <= n < len(PROF)
    """
    pygame.display.set_caption("You selected: " + PROF[n])


def handle_click_event(grid, initial_number):
    """ Return the number of the player we clicked on, otherwise the
    number of the player currently selected

    :param grid: (Grid) the grid of the game
    :param initial_number (int) the currently selected player
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    x, y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
    cell = grid.get_cell(x, y)

    if not cell.is_empty():
        number = cell.get_content().get_n()
        select_player(number)
        return number
    else:
        return initial_number


def main():
    """ main function of this module
    """
    pygame.init()

    try:
        filename = sys.argv[0]
    except IndexError:
        exit("You should enter a filename")

    data = load_file(filename)
    width, height = data['dimensions']['width'], data['dimensions']['height']
    x, y = data["players"]["main"]

    game = Game(filename)
    grid = game.get_grid()
    win = pygame.display.set_mode((width*CELL_SIZE, height*CELL_SIZE))
    selected = 0  # default selected player
    select_player(selected)
    render(win, grid)

    while game.get_state() != GameState.winning:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                selected = handle_click_event(grid, selected)

            elif event.type == pygame.KEYUP and event.key in KEY_DIRECTIONS:
                game.next_step(selected, KEY_DIRECTIONS[event.key])
                render(win, grid)

            # QUIT
            elif event.type == pygame.QUIT:
                pygame.quit()

    display_winning_screen(win)


if __name__ == "__main__":
    import sys
    import json
    sys.argv.pop(0)
    main()
