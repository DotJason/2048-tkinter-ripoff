import tkinter

SQUARES = 9

MASTER = tkinter.Tk()
MASTER.title("Squares")
CANVAS = tkinter.Canvas(MASTER, bg="white", width = 2 ** SQUARES, height = 2 ** SQUARES)


def color(h: int) -> str:
    if h < 16:
        return '#' + ('0' + hex(h)[2:]) * 3
    return '#' + hex(h)[2:] * 3


def step(event: tkinter.Event) -> None:
    CANVAS.delete("all")
    ex = event.x - 2
    ey = event.y - 2
    for i in range(SQUARES, -1, -1):
        x = 2 + ex - ex % 2 ** i
        y = 2 + ey - ey % 2 ** i
        CANVAS.create_rectangle(x, y, x + 2 ** i - 1, y + 2 ** i - 1, fill=color(i * 28))


def main() -> None:
    MASTER.bind("<Motion>", step)
    CANVAS.pack()
    MASTER.mainloop()


if __name__ == "__main__":
    main()
