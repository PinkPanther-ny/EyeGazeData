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

screen_width = 1920
screen_height = 1080
last_take_time = 0
take_photo_interval = 0.1


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
    global last_take_time, take_photo_interval
    if time.time() - last_take_time > take_photo_interval:
        last_take_time = time.time()

        print(f"Current {get_mouse_loc()}\t", end='')
        _, frame = camera.read()
        filename = f"{output_dir}/{get_mouse_loc()}_{get_random_id()}.jpg"
        cv2.imwrite(filename, frame)

        print("Saved!")


def capture():
    take_photo()


def exit_app():
    os._exit(0)


def task():
    while True:
        data = mouse.get_position()
        label1.place(relx=float(data[0] / screen_width), rely=float(data[1] / screen_height), anchor='center')
        time.sleep(1 / 120)


if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    output_dir = 'images'
    os.makedirs(output_dir, exist_ok=True)

    root = tk.Tk()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-alpha", 1)
    root.title("EyeGaze")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.config(bg='#FFFFFF')
    ico = ImageTk.PhotoImage(Image.open(resource_path('ico.ico')))
    root.iconphoto(False, ico)
    root.wm_attributes('-fullscreen', 'True')
    root.wm_attributes("-alpha", 0.7)

    label1 = tk.Label(root, text=f'X', fg='blue', font=('helvetica', 16, 'bold'), justify=tk.CENTER)
    set_click_through(label1.winfo_id())

    Thread(target=task).start()

    keyboard.add_hotkey('SPACE', capture)
    keyboard.add_hotkey('ESC', exit_app)

    root.mainloop()
