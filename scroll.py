import tkinter
from random import randint


CELL_SIDE = int(input("cell side in pixels: "))
SCREEN_WIDTH = int(input("field width in cells: "))
SCREEN_HEIGHT = int(input("field height in cells: "))
MASTER = tkinter.Tk()
MASTER.title("Scrolling in the deep")
CANVAS = tkinter.Canvas(MASTER, bg="white", width=CELL_SIDE * SCREEN_WIDTH, height=CELL_SIDE * SCREEN_HEIGHT)
CANVAS.pack()


def color(r, g, b) -> str:
    s = "#"
    for part in (r, g, b):
        h = hex(part)[2:]
        if len(h) == 1:
            s += '0'
        s += h

    return s


WIDTH = int(input("map width in cells: "))
HEIGHT = int(input("map height in cells: "))
tile_map = [[None for y in range(HEIGHT)] for x in range(WIDTH)]

tile_map[0][0] = randint(0, 255), randint(0, 255), randint(0, 255)
for x in range(1, WIDTH):
    tile_map[x][0] = tuple(map(lambda x: (x + randint(-10, 10)) % 256, tile_map[x - 1][0]))

for y in range(1, HEIGHT):
    tile_map[0][y] = tuple(map(lambda x: (x + randint(-10, 10)) % 256, tile_map[0][y - 1]))

for x in range(1, WIDTH):
    for y in range(1, HEIGHT):
        tile_map[x][y] = tuple(map(lambda x, y: ((x + y) // 2 + randint(-10, 10)) % 256,
                               tile_map[x - 1][y], tile_map[x][y - 1]))

for x in range(WIDTH):
    for y in range(HEIGHT):
        tile_map[x][y] = color(*tile_map[x][y])

FIELD_WIDTH = CELL_SIDE * WIDTH - CELL_SIDE * SCREEN_WIDTH
FIELD_HEIGHT = CELL_SIDE * HEIGHT - CELL_SIDE * SCREEN_HEIGHT

x_current = 0
y_current = 0
x_relative = 0
y_relative = 0


def render() -> None:
    CANVAS.delete("all")

    leftmost = x_relative // CELL_SIDE
    upmost = y_relative // CELL_SIDE
    x_span = x_relative % CELL_SIDE
    y_span = y_relative % CELL_SIDE

    for x in range(SCREEN_WIDTH + 1):
        for y in range(SCREEN_HEIGHT + 1):
            x_corner = x * CELL_SIDE - x_span
            y_corner = y * CELL_SIDE - y_span

            CANVAS.create_rectangle(x_corner, y_corner, x_corner + CELL_SIDE, y_corner + CELL_SIDE,
                                    fill=tile_map[x + leftmost][y + upmost])


def capture(event: tkinter.Event) -> None:
    global x_current, y_current

    x_current = event.x
    y_current = event.y


def scroll(event: tkinter.Event) -> None:
    global x_current, y_current, x_relative, y_relative

    x = event.x - x_current
    y = event.y - y_current

    if 0 <= x_relative - x < FIELD_WIDTH:
        x_relative -= x
    if 0 <= y_relative - y < FIELD_HEIGHT:
        y_relative -= y

    x_current = event.x
    y_current = event.y

    render()



def main() -> None:
    render()
    CANVAS.bind("<Button-1>", capture)
    CANVAS.bind("<B1-Motion>", scroll)
    MASTER.mainloop()


if __name__ == '__main__':
    main()