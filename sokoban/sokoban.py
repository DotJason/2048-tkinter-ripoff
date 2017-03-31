from sys import argv
import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename


PATH = argv[0]
try:
    PATH = PATH[:PATH.rindex('/')]
except ValueError:
    PATH = ""

CELL_SIDE = int(input("cell side in pixels: "))
field_width = int(input("field width in tiles: "))
field_height = int(input("field height in tiles: "))
screen_width = CELL_SIDE * field_width
screen_height = CELL_SIDE * field_height

MASTER = tkinter.Tk()
MENU = tkinter.Menu(MASTER)
FILE = tkinter.Menu(MENU, tearoff=0)
CANVAS_FRAME = FRAME = tkinter.Frame(MASTER, bd=10, relief="ridge")
CANVAS = tkinter.Canvas(CANVAS_FRAME, bg="white", width=screen_width, height=screen_height, bd=0, highlightthickness=0)
FRAME = tkinter.LabelFrame(MASTER, text="Menu", bd=10)
FILE_LABEL = tkinter.Label(FRAME, text="None", bd=10, relief="ridge")
TILE_LIST = tkinter.Listbox(FRAME, exportselection=0, highlightthickness=0, bd=10, relief="ridge")
VICTORY = tkinter.Label(MASTER, text="")

TILES = ["white", "black", "brown", "blue", "green", "red", "blue"]

tile_map = [[0 for y in range(field_height)] for x in range(field_width)]
id_map = [[None for y in range(field_height)] for x in range(field_width)]
current_file = ""
player_x = None
player_y = None
targets = 0


def set_tile(x: int, y: int, tile: int) -> None:
    global player_x, player_y, targets

    CANVAS.delete(id_map[x][y])

    cx = CELL_SIDE * x
    cy = CELL_SIDE * y

    color = TILES[tile]
    id_map[x][y] = CANVAS.create_rectangle(cx, cy, cx + CELL_SIDE - 1, cy + CELL_SIDE - 1, fill=color, outline=color)

    if tile == 3 or tile == 6:
        if player_x != None:
            if tile_map[player_x][player_y] == 6:
                set_tile(player_x, player_y, 4)
            else:
                set_tile(player_x, player_y, 0)
        player_x = x
        player_y = y
    elif tile_map[x][y] == 3:
        player_x = player_y = None

    if tile == 4 and tile_map[x][y] != 6 or tile == 6 and tile_map[x][y] != 4:
        targets += 1
        if targets == 1:
            VICTORY.config(text="")
    elif tile_map[x][y] == 4 and tile != 6 or tile_map[x][y] == 6 and tile != 4:
        targets -= 1
        if targets == 0:
            VICTORY.config(text="Victory!")

    tile_map[x][y] = tile


def open_file() -> None:
    global current_file, field_width, field_height, screen_width, screen_height, tile_map, id_map

    temp = askopenfilename(title="Open level", initialdir=PATH)
    if temp:
        current_file = temp
        FILE_LABEL.config(text=current_file)

        with open(current_file) as file:
            field_width = 0
            field_height = 0
            for line in file:
                field_height = max(field_height, len(line.split()))
                field_width += 1

        screen_width = CELL_SIDE * field_width
        screen_height = CELL_SIDE * field_height
        CANVAS.config(width=screen_width, height=screen_height)

        tile_map = [[0 for y in range(field_height)] for x in range(field_width)]
        id_map = [[None for y in range(field_height)] for x in range(field_width)]

        with open(current_file) as file:
            x = 0
            for line in file:
                y = 0
                for tile in line.split():
                    set_tile(x, y, int(tile))
                    y += 1
                x += 1


def save_file() -> None:
    if current_file:
        with open(current_file, "w") as file:
            for line in tile_map:
                file.write(' '.join(map(str, line)) + '\n')


def save_file_as() -> None:
    global current_file

    temp = asksaveasfilename(title="Save level as", defaultextension=".sok", initialfile=current_file)
    if temp:
        current_file = temp
        FILE_LABEL.config(text=current_file)

        with open(current_file, "w") as file:
            for line in tile_map:
                file.write(' '.join(map(str, line)) + '\n')


def edit(event: tkinter.Event) -> None:
    if 0 <= event.x < screen_width and 0 <= event.y < screen_height:
        x = event.x // CELL_SIDE
        y = event.y // CELL_SIDE

        set_tile(x, y, TILE_LIST.curselection()[0])


def step(event: tkinter.Event) -> None:
    key = event.keysym
    if key == "Up":
        if player_y > 0:
            n = tile_map[player_x][player_y - 1]
            if n != 1:
                if n == 4:
                    set_tile(player_x, player_y - 1, 6)
                elif n % 3 == 2:
                    if player_y > 1:
                        if tile_map[player_x][player_y - 2] == 0:
                            set_tile(player_x, player_y - 1, 1 + n)
                            set_tile(player_x, player_y - 1, 2)
                        elif tile_map[player_x][player_y - 2] == 4:
                            set_tile(player_x, player_y - 1, 1 + n)
                            set_tile(player_x, player_y - 1, 5)
                else:
                    set_tile(player_x, player_y - 1, 3)
    elif key == "Down":
        if player_y < field_height - 1:
            n = tile_map[player_x][player_y + 1]
            if n != 1:
                if n == 4:
                    set_tile(player_x, player_y + 1, 6)
                elif n % 3 == 2:
                    if player_y < field_height - 2:
                        if tile_map[player_x][player_y + 2] == 0:
                            set_tile(player_x, player_y + 1, 1 + n)
                            set_tile(player_x, player_y + 1, 2)
                        elif tile_map[player_x][player_y + 2] == 4:
                            set_tile(player_x, player_y + 1, 1 + n)
                            set_tile(player_x, player_y + 1, 5)
                else:
                    set_tile(player_x, player_y + 1, 3)
    elif key == "Left":
        if player_x > 0:
            n = tile_map[player_x - 1][player_y]
            if n != 1:
                if n == 4:
                    set_tile(player_x - 1, player_y, 6)
                elif n % 3 == 2:
                    if player_x > 1:
                        if tile_map[player_x - 2][player_y] == 0:
                            set_tile(player_x - 1, player_y, 1 + n)
                            set_tile(player_x - 1, player_y, 2)
                        elif tile_map[player_x - 2][player_y] == 4:
                            set_tile(player_x - 1, player_y, 1 + n)
                            set_tile(player_x - 1, player_y, 5)
                else:
                    set_tile(player_x - 1, player_y, 3)
    elif key == "Right":
        if player_x < field_width - 1:
            n = tile_map[player_x + 1][player_y]
            if n != 1:
                if n == 4:
                    set_tile(player_x + 1, player_y, 6)
                elif n % 3 == 2:
                    if player_x < field_width - 2:
                        if tile_map[player_x + 2][player_y] == 0:
                            set_tile(player_x + 1, player_y, 1 + n)
                            set_tile(player_x + 1, player_y, 2)
                        elif tile_map[player_x + 2][player_y] == 4:
                            set_tile(player_x + 1, player_y, 1 + n)
                            set_tile(player_x + 1, player_y, 5)
                else:
                    set_tile(player_x + 1, player_y, 3)


def edit_mode() -> None:
    TILE_LIST.config(state="normal")

    CANVAS.config(cursor="pencil")

    MASTER.unbind("<Key>")
    CANVAS.bind("<Button-1>", edit)
    CANVAS.bind("<B1-Motion>", edit)


def play_mode() -> None:
    TILE_LIST.config(state="disabled")

    CANVAS.config(cursor="arrow")

    CANVAS.unbind("<Button-1>")
    CANVAS.unbind("<B1-Motion>")
    MASTER.bind("<Key>", step)


EDIT = tkinter.Button(FRAME, text="Edit", command=edit_mode)
PLAY = tkinter.Button(FRAME, text="Play", command=play_mode)


def main() -> None:
    FILE.add_command(label="Open", command=open_file)
    FILE.add_command(label="Save", command=save_file)
    FILE.add_command(label="Save as", command=save_file_as)
    FILE.add_command(label="Exit", command=exit)
    MENU.add_cascade(label="File", menu=FILE)
    MASTER.config(menu=MENU)

    TILE_LIST.insert("end", "Empty", "Wall", "Box", "Player", "Target")
    TILE_LIST.select_set(0)

    MASTER.title("Sokoban")
    CANVAS_FRAME.grid(row=0, column=0)
    CANVAS.pack()
    FRAME.grid(row=1, column=0)
    FILE_LABEL.grid(row=0, column=0, columnspan=2)
    EDIT.grid(row=1, column=0)
    PLAY.grid(row=1, column=1)
    TILE_LIST.grid(row=2, column=0, columnspan=2)
    VICTORY.grid(row=2, column=0)

    MASTER.mainloop()


if __name__ == '__main__':
    main()
