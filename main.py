import os
import random
import sys
import tkinter as tk

import cv2
import keyboard
import shortuuid
import win32con
import win32gui
import winsound
from PIL import ImageTk, Image


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
        styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        styles = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
    except Exception as e:
        print(e)


def get_loc(label):
    data = label.place_info()
    return f"{round(float(data['relx']), 3)}_{round(float(data['rely']), 3)}"


def take_photo(label):
    ret, frame = camera.read()
    filename = f"{output_dir}/{get_loc(label)}_{get_random_id()}.jpg"
    cv2.imwrite(filename, frame)
    print("Saved!")


def capture():
    take_photo(label1)

    print(f"Current {get_loc(label1)}\t", end='')
    winsound.MessageBeep(winsound.MB_ICONHAND)


def capture_and_update_loc():
    take_photo(label1)

    label1.place(relx=random.random(), rely=random.random(), anchor='center')
    print(f"Current {get_loc(label1)}\t", end='')

    winsound.MessageBeep(winsound.MB_OK)


def exit_app():
    root.quit()
    root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    # Make the root window always on top
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-alpha", 1)
    # Turn off the window shadow
    # root.wm_attributes("-transparentcolor", "#000000")
    title = "AutoClick"
    root.title(title)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.config(bg='#FFFFFF')

    ico = ImageTk.PhotoImage(Image.open(resource_path('ico.ico')))
    root.iconphoto(False, ico)

    # Hide the root window drag bar and close button
    # root.overrideredirect(1)
    root.wm_attributes('-fullscreen', 'True')

    label1 = tk.Label(root, text=f'X', fg='blue', font=('helvetica', 16, 'bold'), justify=tk.CENTER)
    label1.place(relx=random.random(), rely=random.random(), anchor='center')

    set_click_through(label1.winfo_id())
    root.wm_attributes("-alpha", 0.7)

    camera = cv2.VideoCapture(0)
    output_dir = 'images'
    os.makedirs(output_dir, exist_ok=True)
    print(f"Current {get_loc(label1)}", end='')

    keyboard.add_hotkey('SPACE', capture_and_update_loc)
    keyboard.add_hotkey(',', capture)
    keyboard.add_hotkey('ESC', exit_app)

    root.mainloop()
