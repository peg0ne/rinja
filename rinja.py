#!/usr/bin/env python3
import os
import sys
import json

from time import time

from pynput import keyboard

from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget

config_path = f'{os.getenv("HOME")}/.config/rinja'
with open(f'{config_path}/rinja.json', "r") as config_file:
    config = json.load(config_file)
    colors = config['colors']
    arg_rememeber = config['remember']

t = time()
is_alt: bool = False

app = QApplication(sys.argv)


lab = QLabel('')
inp = QLineEdit('')


def write_remember():
    with open(f'{config_path}/rinja.json', "w") as config_file:
        config['remember'] = arg_rememeber
        json.dump(config, config_file)


def remember(arg):
    if arg not in arg_rememeber:
        arg_rememeber.append(arg)
        write_remember()


def remove_remember():
    arg = check_similar(inp.text())
    if arg in arg_rememeber:
        arg_rememeber.remove(arg)
        write_remember()
    check_similar(inp.text())


def check_similar(arg):
    arg_rememeber.sort()
    for r in arg_rememeber:
        if r.startswith(arg) and r != arg:
            lab.setText(
                f'<h1 style="text-align: center;">{arg}|<span style="color: {colors["highlight"]}">{r[len(arg):]}</span></h1>')
            return r
    else:
        lab.setText(
            f'<h1 style="text-align: center;">{arg}|</h1>')


def auto_complete():
    global is_alt
    arg = check_similar(inp.text())
    if arg is not None:
        if is_alt:
            run_it()
        else:
            inp.setText(arg)
            lab.setText(f'<h1 style="text-align: center;">{arg}|</h1>')
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


def on_release(key):
    global is_alt
    try:
        if key == keyboard.Key.alt:
            is_alt = False
    except:
        pass


def on_press(key):
    global is_alt
    try:
        if key == keyboard.Key.esc:
            app.exit()
        elif key == keyboard.Key.alt:
            is_alt = True
        elif key == keyboard.Key.delete:
            remove_remember()
    except:
        pass


inp.textEdited[str].connect(check_similar)
inp.returnPressed.connect(auto_complete)
inp.setGeometry(0, 0, 0, 0)

lab.setGeometry(0, 0, 500, 200)

window = QWidget()
lab.setParent(window)
inp.setParent(window)

qtRectangle = window.frameGeometry()
centerPoint = QDesktopWidget().availableGeometry().center()
qtRectangle.moveCenter(centerPoint)
window.move(qtRectangle.topLeft())

window.setWindowTitle('Rinja')
window.setGeometry(0, 0, 500, 200)
qtRectangle = window.frameGeometry()
centerPoint = QDesktopWidget().availableGeometry().center()
qtRectangle.moveCenter(centerPoint)
window.move(qtRectangle.topLeft())
window.show()

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
app.focusChanged.connect(lost_focus)
sys.exit(app.exec_())