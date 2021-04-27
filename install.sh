#!/bin/bash
pip3 install PyQt5
pip3 install pynput
CONFIGPATH="$HOME/.config/ninja"
BASETEXT="{'colors': {'highlight':'#333333'}, 'remember': []}"

mk dir "$CONFIGPATH"
cat "$CONFIGPATH/ninja.json"
echo "$BASETEXT" > "$CONFIGPATH/ninja.json"
chmod u+x "ninja.py"
ln -s "ninja.py" "$HOME/.local/bin/ninja"

