#!/bin/sh
# kx2.sh DISP CMD ... : xdotool into the largest visible window on :DISP (focused first).
#   rep N KEY   : KEY N times, 20 ms apart
#   hold KEY S  : key down, wait S seconds, key up
#   anything else is passed to xdotool (key, type, keydown, keyup)
D=$1; shift; export DISPLAY=:$D
W=$(xdotool search --onlyvisible --name . 2>/dev/null | while read w; do eval $(xdotool getwindowgeometry --shell $w); echo "$((WIDTH*HEIGHT)) $w"; done | sort -n | tail -1 | cut -d" " -f2)
[ -n "$W" ] && { xdotool windowactivate --sync $W 2>/dev/null || xdotool windowfocus $W; }
case "$1" in
  rep) exec xdotool key --delay 20 --repeat "$2" "$3";;
  hold) xdotool keydown "$2"; sleep "$3"; exec xdotool keyup "$2";;
  type) shift; exec xdotool type --delay 40 "$@";;
  *) exec xdotool "$@";;
esac
