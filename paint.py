import tkinter
import tkinter.colorchooser


MASTER = tkinter.Tk()
MASTER.title("Paint")
CANVAS = tkinter.Canvas(MASTER, bg="white", width=500, height=500)

objects = []
last = None
tool = CANVAS.create_line
color = "black"
start_x = 0
start_y = 0


def lock(event: tkinter.Event) -> None:
    global start_x, start_y

    start_x = event.x
    start_y = event.y


def move(event: tkinter.Event) -> None:
    global last

    CANVAS.delete(last)
    last = tool(start_x, start_y, event.x, event.y, fill=color)


def release(event: tkinter.Event) -> None:
    CANVAS.delete(last)
    objects.append(tool(start_x, start_y, event.x, event.y, fill=color))


def undo() -> None:
    if objects:
        CANVAS.delete(objects.pop())


def clear() -> None:
    CANVAS.delete("all")
    objects = []


def choose_color() -> None:
    global color

    temp = tkinter.colorchooser.askcolor()[1]
    if temp:
        color = temp


def line() -> None:
    global tool

    tool = CANVAS.create_line


def rect() -> None:
    global tool

    tool = CANVAS.create_rectangle


def oval() -> None:
    global tool

    tool = CANVAS.create_oval


UNDO = tkinter.Button(MASTER, text="undo", command=undo)
CLEAR = tkinter.Button(MASTER, text="clear", command=clear)
COLOR = tkinter.Button(MASTER, text="color", command=choose_color)
LINE = tkinter.Button(MASTER, text="line", command=line)
RECT = tkinter.Button(MASTER, text="rectangle", command=rect)
OVAL = tkinter.Button(MASTER, text="oval", command=oval)


def main() -> None:
    CANVAS.bind("<Button-1>", lock)
    CANVAS.bind("<B1-Motion>", move)
    CANVAS.bind("<ButtonRelease-1>", release)

    CANVAS.grid(row=0, column=0, columnspan=8)
    UNDO.grid(row=1, column=0)
    CLEAR.grid(row=1, column=1)
    COLOR.grid(row=1, column=2)
    LINE.grid(row=1, column=5)
    RECT.grid(row=1, column=6)
    OVAL.grid(row=1, column=7)
    MASTER.mainloop()


if __name__ == '__main__':
    main()
