from tkdev4 import DevWindow


window = DevWindow()


def set_size(width: int, height: int):
    window.geometry(f"{str(width)}x{str(height)}")


def set_pos(x: int, y: int):
    window.geometry(f"+{str(x)}+{str(y)}")


def set_title(title: str):
    window.title(title)


def run_window():
    window.mainloop()


def destory_window():
    window.destroy()


def quit_window():
    window.quit()


set_title("Hello")
run_window()