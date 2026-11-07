#!/bin/bash
# Start a 1998-2000 Delphi Graal beta under Wine so its arrow keys work.
#
#   run_delphi_beta.sh /path/to/5thgraal [display]
#
# The betas read the keyboard through DelphiX TDXInput (DirectInput). They set
# a keyboard data format with one object over a 256-byte buffer, and Wine fills
# only listed objects, so the arrow keys never arrive. Disabling Wine's dinput
# makes DelphiX fall back to GetKeyboardState, which xdotool keydown reaches.
#
# Needs: wine (with wine32), Xvfb, openbox, xdotool.
# Send keys with: xdotool windowactivate <win>; xdotool windowfocus <win>;
#                 xdotool keydown Right; ...; xdotool keyup Right
set -e
dir=${1:?game folder with Graal.exe}
export DISPLAY=${2:-:5}
export WINEPREFIX=${WINEPREFIX:-$HOME/.wine-graal-beta}
export WINEDEBUG=${WINEDEBUG:--all}

if ! xdpyinfo >/dev/null 2>&1; then
  Xvfb "$DISPLAY" -screen 0 1600x800x24 >/dev/null 2>&1 &
  sleep 2
fi
# A window manager on this display lets the game window become active.
xprop -root _NET_SUPPORTING_WM_CHECK 2>/dev/null | grep -q 'window id' ||
  { openbox >/dev/null 2>&1 & sleep 1; }

if [ ! -d "$WINEPREFIX" ]; then
  wineboot -i >/dev/null 2>&1
  # A virtual desktop lets the game window take focus.
  wine reg add 'HKCU\Software\Wine\Explorer' /v Desktop /d Default /f >/dev/null 2>&1
  wine reg add 'HKCU\Software\Wine\Explorer\Desktops' /v Default /d 1024x768 /f >/dev/null 2>&1
  wineserver -w
fi

cd "$dir"
WINEDLLOVERRIDES="dinput=d" exec wine Graal.exe
