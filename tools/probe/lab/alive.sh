#!/bin/sh
# alive.sh DISP NAME : "NAME alive" while a Windows client process (an .exe other than Wine's own
# services) runs inside this lab's network namespace ($FZ/ns.pid), else "NAME CLIENT-GONE";
# "+ERRDLG" when Wine's crash dialog is up on DISP.
X="env DISPLAY=:$1 xdotool"; e=""
[ -n "$($X search --onlyvisible --name 'Program Error' 2>/dev/null | head -1)" ] && e="+ERRDLG"
N=$(readlink /proc/$(cat ${FZ:-$HOME/fz12}/ns.pid)/ns/net); a=""
for p in $(pgrep -f '[A-Za-z0-9_]\.exe'); do
  [ "$(readlink /proc/$p/ns/net 2>/dev/null)" = "$N" ] || continue
  tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null | grep -q -i -E 'winedevice|services|plugplay|explorer|rpcss|sethost|svchost|tabtip|winedbg' && continue
  a=1; break
done
if [ -n "$a" ]; then echo "$2 alive$e"; else echo "$2 CLIENT-GONE$e"; fi
