#!/bin/bash
pip3 install PyQt5
pip3 install pynput
THISDIR=$(dirname "$0")
CONFIGPATH="$HOME/.config/rinja"
BASETEXT="{\"colors\": {\"highlight\":\"#333333\",\"background\":\"#333333\",\"foreground\":\"#333333\"}, \"rect\": {\"width\": 500, \"height\": 150}, \"remember\": []}"

mkdir "$CONFIGPATH"
cat "$CONFIGPATH/rinja.json"
echo "$BASETEXT" > "$CONFIGPATH/rinja.json"
chmod u+x "$THISDIR/rinja.py"
ln -s "$THISDIR/rinja.py" "$HOME/.local/bin/rinja"

