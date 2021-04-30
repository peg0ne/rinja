#!/bin/bash
pip3 install PyQt5
pip3 install pynput
THISDIR=$(dirname "$0")
CONFIGPATH="$HOME/.config/rinja"
BASETEXT="{\"colors\": {\"highlight\":\"#333333\"}, \"remember\": []}"

mkdir "$CONFIGPATH"
cat "$CONFIGPATH/rinja.json"
echo "$BASETEXT" > "$CONFIGPATH/rinja.json"
chmod u+x "$THISDIR/rinja.py"
ln -s "$THISDIR/rinja.py" "$HOME/.local/bin/rinja"

