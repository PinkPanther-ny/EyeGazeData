import os
import sys
import time
import tkinter as tk
from threading import Thread

import cv2
import keyboard
import mouse
import shortuuid
import win32con
import win32gui
from PIL import ImageTk, Image

from sync import sync

screen_width = 1920
screen_height = 1080
take_photo_interval = 0.1

_last_take_time = 0


def get_random_id():
    return shortuuid.uuid().lower()[:6]


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def set_click_through(hwnd):
    try:
        styles = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
    except Exception as e:
        print(e)


def get_mouse_loc():
    data = mouse.get_position()
    return f"{round(float(data[0] / screen_width), 3)}_{round(float(data[1] / screen_height), 3)}"


def take_photo():
    global _last_take_time, take_photo_interval
    if time.time() - _last_take_time > take_photo_interval:
        _last_take_time = time.time()

        print(f"Current {get_mouse_loc()}\t", end='')
        _, frame = camera.read()
        filename = f"{output_dir}/{get_mouse_loc()}_{get_random_id()}.jpg"
        cv2.imwrite(filename, frame)

        print("Saved!")


def capture():
    take_photo()


def exit_app():
    os._exit(0)


def widget_follow_mouse(widget):
    while True:
        data = mouse.get_position()
        widget.place(
            relx=float(data[0] / screen_width),
            rely=float(data[1] / screen_height),
            anchor='center',
            width=22,
            height=22
        )
        time.sleep(1 / 120)


if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    output_dir = 'images'
    os.makedirs(output_dir, exist_ok=True)


    def create_grid(event=None):
        spacing = 50
        w = c.winfo_width()  # Get current width of canvas
        h = c.winfo_height()  # Get current height of canvas
        c.delete('grid_line')  # Will only remove the grid_line

        # Creates all vertical lines at intervals of 100
        for i in range(0, w, spacing):
            c.create_line([(i, 0), (i, h)], tag='grid_line')

        # Creates all horizontal lines at intervals of 100
        for i in range(0, h, spacing):
            c.create_line([(0, i), (w, i)], tag='grid_line')


    root = tk.Tk()

    c = tk.Canvas(root, bg='#333333')
    c.pack(fill=tk.BOTH, expand=True)
    c.bind('<Configure>', create_grid)

    root.wm_attributes("-topmost", True)
    root.wm_attributes("-alpha", 1)
    root.title("EyeGaze")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.config(bg='#000000')
    ico = ImageTk.PhotoImage(Image.open(resource_path('ico.ico')))
    root.iconphoto(False, ico)
    root.wm_attributes('-fullscreen', 'True')
    root.wm_attributes("-alpha", 0.8)

    label = tk.Label(root, text=f'X', fg='blue', font=('helvetica', 16, 'bold'), justify=tk.CENTER)
    set_click_through(label.winfo_id())

    Thread(target=widget_follow_mouse, args=(label,)).start()

    keyboard.add_hotkey('SPACE', capture)
    keyboard.add_hotkey('CTRL+S', sync)
    keyboard.add_hotkey('ESC', exit_app)

    root.mainloop()
