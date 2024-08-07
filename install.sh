#!/bin/bash
pip3 install PyQt5
pip3 install pynput
THISDIR=$(dirname "$0")
CONFIGPATH="$HOME/.config/rinja"
BINPATH="$HOME/.local/bin"
BASETEXT="{\"colors\": {\"highlight\":\"#333333\",\"background\":\"#333333\",\"foreground\":\"#333333\"}, \"rect\": {\"width\": 500, \"height\": 150}, \"remember\": []}"

mkdir -p "$CONFIGPATH"
mkdir -p "$BINPATH"
cat "$CONFIGPATH/rinja.json"
echo "$BASETEXT" > "$CONFIGPATH/rinja.json"
chmod u+x "$THISDIR/rinja.py"
ln -r -s "$THISDIR/rinja.py" "$BINPATH/rinja"

