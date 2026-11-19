#!/bin/sh
# alive.sh DISP NAME : "NAME alive" if the game window is still mapped on DISP, else "NAME CLIENT-GONE";
# "+ERRDLG" when Wine's crash dialog is up.
X="env DISPLAY=:$1 xdotool"; e=""
[ -n "$($X search --onlyvisible --name 'Program Error' 2>/dev/null | head -1)" ] && e="+ERRDLG"
if [ -n "$($X search --onlyvisible --name '^Graal' 2>/dev/null | head -1)" ]; then echo "$2 alive$e"; else echo "$2 CLIENT-GONE$e"; fi
