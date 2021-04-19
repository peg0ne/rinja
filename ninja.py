#!/usr/bin/env python3
import os
import sys
import json

from time import time

from pynput import keyboard

from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget

config_path = f'{os.getenv("HOME")}/.config/ninja'
with open(f'{config_path}/ninja.json', "r") as config_file:
    config = json.load(config_file)
    colors = config['colors']
    arg_rememeber = config['remember']

is_alt = False
t = time()


app = QApplication(sys.argv)
scr = app.desktop().screenGeometry()

wid = scr.width()
hei = scr.height()

lab = QLabel('')
inp = QLineEdit('')


def write_remember():
    with open(f'{config_path}/ninja.json', "w") as config_file:
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
    for r in arg_rememeber:
        if r.startswith(arg) and r != arg:
            lab.setText(
                f'<h1 style="text-align: center;">{arg}<span style="color: {colors["highlight"]}">{r[len(arg):]}</span></h1>')
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

window.setWindowTitle('Ninja')
window.setGeometry(int(wid), int(hei / 2), 500, 200)
window.show()

listener = keyboard.Listener(on_press=on_press)
listener.start()
app.focusChanged.connect(lost_focus)
sys.exit(app.exec_())
