import tkinter
from random import randint
from itertools import product


CELL_SIDE = int(input("cell side in pixels: "))
FIELD_WIDTH = int(input("field width in tiles: "))
FIELD_HEIGHT = int(input("field height in tiles: "))
MASTER = tkinter.Tk()
MASTER.title("2048 tkinter ripoff")
CANVAS = tkinter.Canvas(MASTER, bg="white", width=FIELD_WIDTH * CELL_SIDE + 1, height=FIELD_HEIGHT * CELL_SIDE + 1,
                        bd=0, highlightthickness=0)


def rgb(parts) -> str:
    color = "#"
    for part in parts:
        part = hex(part)[2:]
        if len(part) == 1:
            color += '0'
        color += part
    return color


COLORS = list(product(range(63, 256, 64), range(63, 256, 64), range(63, 256, 64)))
COLORS.sort(key=lambda x: -sum(x))
COLORS = (None,) + tuple(map(rgb, COLORS))

tiles = [[0 for y in range(FIELD_HEIGHT)] for x in range(FIELD_WIDTH)]
ids = [[(None, None) for y in range(FIELD_HEIGHT)] for x in range(FIELD_WIDTH)]
free_tiles = FIELD_WIDTH * FIELD_HEIGHT


def delete_tile(x: int, y: int) -> None:
    tiles[x][y] = 0
    CANVAS.delete(*ids[x][y])
    ids[x][y] = (None, None)


def set_tile(x: int, y: int, tile_type: int) -> None:
    delete_tile(x, y)
    tiles[x][y] = tile_type
    cx = x * CELL_SIDE
    cy = y * CELL_SIDE
    ids[x][y] = (CANVAS.create_rectangle(cx, cy, cx + CELL_SIDE, cy + CELL_SIDE, fill=COLORS[tile_type]),
                 CANVAS.create_text(cx + CELL_SIDE // 2, cy + CELL_SIDE // 2, text=str(2 ** tile_type), font="courier"))


def create_random() -> None:
    global free_tiles
    place_delay = randint(1, free_tiles)
    for x in range(FIELD_WIDTH):
        for y in range(FIELD_HEIGHT):
            if not tiles[x][y]:
                place_delay -= 1
                if not place_delay:
                    set_tile(x, y, 1 if randint(0, 10) else 2)
                    free_tiles -= 1
                    return


def step(event: tkinter.Event) -> None:
    global free_tiles
    if event.keysym == "Left":
        for y in range(FIELD_HEIGHT):
            last = 0
            while last < FIELD_WIDTH and not tiles[last][y]:
                last += 1
            if last != FIELD_WIDTH:
                set_tile(0, y, tiles[last][y])
                if last:
                    delete_tile(last, y)
                last = 0
                for x in range(1, FIELD_WIDTH):
                    if tiles[x][y]:
                        if tiles[last][y] == tiles[x][y]:
                            set_tile(last, y, tiles[last][y] + 1)
                            delete_tile(x, y)
                            free_tiles += 1
                        else:
                            last += 1
                            set_tile(last, y, tiles[x][y])
                            if last != x:
                                delete_tile(x, y)
    elif event.keysym == "Right":
        for y in range(FIELD_HEIGHT):
            last = FIELD_WIDTH - 1
            while last > -1 and not tiles[last][y]:
                last -= 1
            if last != -1:
                set_tile(FIELD_WIDTH - 1, y, tiles[last][y])
                if last != FIELD_WIDTH - 1:
                    delete_tile(last, y)
                last = FIELD_WIDTH - 1
                for x in range(FIELD_WIDTH - 2, -1, -1):
                    if tiles[x][y]:
                        if tiles[last][y] == tiles[x][y]:
                            set_tile(last, y, tiles[last][y] + 1)
                            delete_tile(x, y)
                            free_tiles += 1
                        else:
                            last -= 1
                            set_tile(last, y, tiles[x][y])
                            if last != x:
                                delete_tile(x, y)
    elif event.keysym == "Up":
        for x in range(FIELD_WIDTH):
            last = 0
            while last < FIELD_HEIGHT and not tiles[x][last]:
                last += 1
            if last != FIELD_HEIGHT:
                set_tile(x, 0, tiles[x][last])
                if last:
                    delete_tile(x, last)
                last = 0
                for y in range(1, FIELD_HEIGHT):
                    if tiles[x][y]:
                        if tiles[x][last] == tiles[x][y]:
                            set_tile(x, last, tiles[x][last] + 1)
                            delete_tile(x, y)
                            free_tiles += 1
                        else:
                            last += 1
                            set_tile(x, last, tiles[x][y])
                            if last != y:
                                delete_tile(x, y)
    elif event.keysym == "Down":
        for x in range(FIELD_WIDTH):
            last = FIELD_HEIGHT - 1
            while last > -1 and not tiles[x][last]:
                last -= 1
            if last != -1:
                set_tile(x, FIELD_HEIGHT - 1, tiles[x][last])
                if last != FIELD_HEIGHT - 1:
                    delete_tile(x, last)
                last = FIELD_HEIGHT - 1
                for y in range(FIELD_HEIGHT - 2, -1, -1):
                    if tiles[x][y]:
                        if tiles[x][last] == tiles[x][y]:
                            set_tile(x, last, tiles[x][last] + 1)
                            delete_tile(x, y)
                            free_tiles += 1
                        else:
                            last -= 1
                            set_tile(x, last, tiles[x][y])
                            if last != y:
                                delete_tile(x, y)
    else:
        return
    
    if (free_tiles):
        create_random()


def main() -> None:
    MASTER.bind("<KeyPress>", step)
    CANVAS.pack()
    MASTER.mainloop()


if __name__ == "__main__":
    main()
