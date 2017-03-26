import tkinter
from random import randint


CELL_SIDE = int(input("cell side in pixels: "))
FIELD_WIDTH = int(input("field width in cells: "))
FIELD_HEIGHT = int(input("field height in cells: "))
MASTER = tkinter.Tk()
MASTER.title("In the deep")
CANVAS = tkinter.Canvas(MASTER, bg="white", width=CELL_SIDE * FIELD_WIDTH + 1, height=CELL_SIDE * FIELD_HEIGHT + 1)
CANVAS.pack()

SCATTER = int(input("color funkieness: "))


def color_scatter(n: int) -> int:
    return n + randint(max(-SCATTER, -n), min(SCATTER, 255 - n))


def color(r, g, b) -> str:
    s = "#"
    for part in (r, g, b):
        h = hex(part)[2:]
        if len(h) == 1:
            s += '0'
        s += h

    return s


def main() -> None:
    tile_map = [[None for y in range(FIELD_HEIGHT)] for x in range(FIELD_WIDTH)]
    tile_map[0][0] = (randint(0, 255), randint(0, 255), randint(0, 255))

    for x in range(1, FIELD_WIDTH):
        tile_map[x][0] = tuple(map(color_scatter, tile_map[x - 1][0]))

    for y in range(1, FIELD_HEIGHT):
        tile_map[0][y] = tuple(map(color_scatter, tile_map[0][y - 1]))

    for x in range(1, FIELD_WIDTH):
        for y in range(1, FIELD_HEIGHT):
            tile_map[x][y] = tuple(map(color_scatter,
                                       ((p + q) // 2 for p, q in zip(tile_map[x - 1][y], tile_map[x][y - 1]))))

    for x in range(FIELD_WIDTH):
        for y in range(FIELD_HEIGHT):
            cx = 2 + x * CELL_SIDE
            cy = 2 + y * CELL_SIDE

            cur = color(*tile_map[x][y])
            CANVAS.create_rectangle(cx, cy, cx + CELL_SIDE, cy + CELL_SIDE, fill=cur, outline=cur)

    MASTER.mainloop()


if __name__ == '__main__':
    main()
