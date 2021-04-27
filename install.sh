#!/bin/bash
pip3 install PyQt5
pip3 install pynput
THISDIR=$(dirname "$0")
CONFIGPATH="$HOME/.config/ninja"
BASETEXT="{\"colors\": {\"highlight\":\"#333333\"}, \"remember\": []}"

mkdir "$CONFIGPATH"
cat "$CONFIGPATH/ninja.json"
echo "$BASETEXT" > "$CONFIGPATH/ninja.json"
chmod u+x "$THISDIR/ninja.py"
ln -s "$THISDIR/ninja.py" "$HOME/.local/bin/ninja"

