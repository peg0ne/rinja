#!/usr/bin/env python3
import os
import sys
import json

from time import time

from pynput import keyboard

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget

H1_CENTER = '<h1 style="text-align: center;">'

config_path = f'{os.getenv("HOME")}/.config/rinja'
with open(f'{config_path}/rinja.json', "r") as config_file:
    config = json.load(config_file)
    colors = config['colors']
    rect = config['rect']
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
    arg = format_args()
    if arg in arg_rememeber:
        arg_rememeber.remove(arg)
        write_remember()
    format_args()


def format_text(r=None):
    arg = inp.text()
    cursor_pos = inp.cursorPosition()
    if r == None:
        return f'{H1_CENTER}{arg[:cursor_pos]}|{arg[cursor_pos:]}</h1>'
    else:
        return f'{H1_CENTER}{arg[:cursor_pos]}|{arg[cursor_pos:]}<span style="color: {colors["highlight"]}">{r[len(arg):]}</span></h1>'


def format_args():
    arg = inp.text()
    arg_rememeber.sort()
    for r in arg_rememeber:
        if r.startswith(arg) and r != arg:
            lab.setText(format_text(r))
            return r
    else:
        lab.setText(
            format_text())


def auto_complete():
    global is_alt
    arg = format_args()
    cursor_pos = inp.cursorPosition()
    if arg is not None:
        if is_alt:
            run_it()
        else:
            inp.setText(arg)
            inp.setCursorPosition(len(arg))
            cursor_pos = inp.cursorPosition()
            lab.setText(format_text())
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


inp.textEdited[str].connect(format_args)
inp.returnPressed.connect(auto_complete)
inp.cursorPositionChanged.connect(format_args)
inp.setGeometry(0, 0, 0, 0)
lab.setStyleSheet(f'color: {colors["foreground"]};')

lab.setGeometry(0, 0, rect['width'], rect['height'])
lab.setStyleSheet(f'background-color: {colors["background"]};')

window = QWidget()
lab.setParent(window)
inp.setParent(window)

qtRectangle = window.frameGeometry()
centerPoint = QDesktopWidget().availableGeometry().center()
qtRectangle.moveCenter(centerPoint)
window.move(qtRectangle.topLeft())

window.setWindowTitle('Rinja')
window.setGeometry(0, 0, rect['width'], rect['height'])
qtRectangle = window.frameGeometry()
centerPoint = QDesktopWidget().availableGeometry().center()
qtRectangle.moveCenter(centerPoint)
window.move(qtRectangle.topLeft())
window.setWindowFlags(Qt.WindowStaysOnTopHint)
window.show()

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
app.focusChanged.connect(lost_focus)
sys.exit(app.exec_())
