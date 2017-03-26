import tkinter
from random import randint


WIDTH = 500
HEIGHT = 500
MASTER = tkinter.Tk()
MASTER.title("Buttons")
CANVAS = tkinter.Canvas(MASTER, bg="white", width=WIDTH, height=HEIGHT)

current = None


def random_color() -> str:
    s = '#'
    for part in (randint(0, 255), randint(0, 255), randint(0, 255)):
        part = hex(part)[2:]

        if len(part) == 1:
            s += '0'

        s += part

    return s


def create_new(event: tkinter.Event = None) -> None:
    global current

    CANVAS.delete(current)

    x = randint(2, WIDTH - 8)
    y = randint(2, HEIGHT - 8)
    width = randint(10, WIDTH + 1 - x)
    height = randint(10, HEIGHT + 1 - y)
    color = random_color()

    if randint(0, 1):
        current = CANVAS.create_rectangle(x, y, x + width, y + height, fill=color)
    else:
        current = CANVAS.create_oval(x, y, x + width, y + height, fill=color)

    CANVAS.tag_bind(current, "<Button-1>", create_new)


def main() -> None:
    create_new()
    CANVAS.pack()
    MASTER.mainloop()


if __name__ == '__main__':
    main()