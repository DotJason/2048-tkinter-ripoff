import tkinter


class Canvas(tkinter.Canvas):
    def create_button(self, *args, **kw) -> int:
        x, y, cx, cy = args
        text = kw["text"]
        command = kw["command"]

        button_id = self.create_rectangle(x, y, cx, cy, fill="white")
        self.create_text(x + (cx - x) // 2, y + (cy - y) // 2, text=text, state="disabled")

        self.tag_bind(button_id, "<Button-1>", command)

        return button_id


WIDTH = 500
HEIGHT = 500
MASTER = tkinter.Tk()
MASTER.title("Canvas buttons")
CANVAS = Canvas(MASTER, bg="white", width=WIDTH, height=HEIGHT)


def create_new(event: tkinter.Event) -> None:
    CANVAS.create_button(event.x - 50, event.y - 50, event.x + 50, event.y + 50, text="test", command=create_new)


def main() -> None:
    test = CANVAS.create_button(100, 100, 200, 200, text="test", command=create_new)

    CANVAS.pack()
    MASTER.mainloop()


if __name__ == '__main__':
    main()