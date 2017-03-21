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
    ex = event.x
    ey = event.y
    for i in range(SQUARES, -1, -1):
        x = ex - ex % 2 ** i
        y = ey - ey % 2 ** i
        CANVAS.create_rectangle(x, y, x + 2 ** i, y + 2 ** i, fill=color(i * 25))


def main() -> None:
    MASTER.bind("<Motion>", step)
    CANVAS.pack()
    MASTER.mainloop()


if __name__ == "__main__":
    main()
