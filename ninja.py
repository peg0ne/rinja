#!/usr/bin/env python3
import os
import sys

from time import time

from pynput import keyboard

from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget

config_path = f'{os.getenv("HOME")}/.config/ninja/ninja.conf'
color = open(config_path, "r").read()

is_alt = False
t = time()
arg_rememeber = []


app = QApplication(sys.argv)
scr = app.desktop().screenGeometry()

wid = scr.width()
hei = scr.height()

lab = QLabel('')
inp = QLineEdit('')


def remember(arg):
    if arg not in arg_rememeber:
        arg_rememeber.append(arg)


def check_similar(arg):
    for r in arg_rememeber:
        if r.startswith(arg) and r != arg:
            lab.setText(
                f'<h1 style="text-align: center;">{arg}<span style="color: {color}">{r[len(arg):]}</span></h1>')
            return r
    else:
        lab.setText(
            f'<h1 style="text-align: center;">{arg}</h1>')


def auto_complete(is_alt=False):
    arg = check_similar(inp.text())
    if arg is not None:
        if is_alt:
            inp.setText(arg)
            lab.setText(f'<h1 style="text-align: center;">{arg}</h1>')
        else:
            run_it()
    else:
        run_it()


def run_it():
    args = inp.text()
    remember(args)
    print(args)
    inp.clear()
    lab.clear()
    os.system(f"setsid {args} &")


def lost_focus():
    if time() >= (t + 1):
        app.exit()


def on_press(key):
    try:
        if key == keyboard.Key.esc:
            app.exit()
        elif key == keyboard.Key.alt:
            auto_complete(True)
    except:
        pass


inp.textEdited[str].connect(check_similar)
inp.returnPressed.connect(auto_complete)
inp.setGeometry(0, 0, 0, 0)

lab.setGeometry(0, 0, 500, 200)

window = QWidget()
lab.setParent(window)
inp.setParent(window)

window.setWindowTitle('Ninja')
window.setGeometry(int(wid), int(hei / 2), 500, 200)
window.show()

listener = keyboard.Listener(on_press=on_press)
listener.start()
app.focusChanged.connect(lost_focus)
sys.exit(app.exec_())
