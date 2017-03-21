import tkinter

CELL_SIDE = int(input("cell side in pixels:"))
FIELD_WIDTH = int(input("field width in tiles:"))
FIELD_HEIGHT = int(input("field height in tiles:"))
MASTER = tkinter.Tk()
MASTER.title("Langton's ant")
CANVAS = tkinter.Canvas(MASTER, bg="white", width=FIELD_WIDTH * CELL_SIDE + 1, height=FIELD_HEIGHT * CELL_SIDE + 1)

tiles = [[[None] for y in range(FIELD_WIDTH)] for x in range(FIELD_HEIGHT)]
x = FIELD_WIDTH // 2
y = FIELD_HEIGHT // 2
direction = 0


def rgb(parts) -> str:
    color = "#"
    for part in parts:
        part = hex(part)[2:]
        if len(part) == 1:
            color += '0'
        color += part
    return color


def enable(x: int, y: int) -> None:
    cx = 2 + x * CELL_SIDE
    cy = 2 + y * CELL_SIDE
    tiles[x][y] = CANVAS.create_rectangle(cx, cy, cx + CELL_SIDE, cy + CELL_SIDE, fill="black")


def disable(x: int, y: int) -> None:
    CANVAS.delete(tiles[x][y])
    tiles[x][y] = None


def step() -> None:
    global x, y, direction

    if direction == 0:
        y = (y - 1) % FIELD_HEIGHT
    elif direction == 1:
        x = (x + 1) % FIELD_WIDTH
    elif direction == 2:
        y = (y + 1) % FIELD_HEIGHT
    else:
        x = (x - 1) % FIELD_WIDTH

    if tiles[x][y]:
        disable(x, y)
        direction = (direction + 1) % 4
    else:
        enable(x, y)
        direction = (direction - 1) % 4

    MASTER.after(1, step)


def main() -> None:
    MASTER.after(1, step)
    CANVAS.pack()
    MASTER.mainloop()


if __name__ == '__main__':
    main()