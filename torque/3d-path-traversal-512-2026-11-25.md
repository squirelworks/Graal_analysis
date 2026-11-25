# 5.12 path-traversal safety of server-sent file names (2026-11-25)

Lab: the real 5.12 client under Wine on Mesa llvmpipe, against our own push
gserver on loopback (never a third-party server). Question (T3D-112): can a
hostile server make the client write a downloaded terrain texture **outside**
its own folders by giving it a hostile file name? Behaviour only; markers and
scans stay in the lab kit. **[lab][cap]**

## Method

For each hostile name, the name was put first in `heights.info` and a marker
`evil.png` was planted so the server would return a body for it, then the
client's tree, the Wine `drive_c`, and `/tmp` were scanned after the run for
any file written outside the client's own `levels3d` tree.

## Result — no escape

For every name the server delivered a body for, **5.12 stripped the whole
directory part and saved the file under its basename (`evil.png`) inside its
own `levels3d\images`.** No file landed outside the client's `levels3d` tree
in any case. Names tried:

- `../evil.png`, `../../evil.png`, `..\..\evil.png`, `a/../../evil.png`
- `C:\evil.png`, `/tmp/evil.png`, `Z:\evil.png`
- `\\host\share\evil.png` (UNC)
- `sub\deep\evil.png`, `./evil.png`

The Windows device names (`CON`, `NUL`, `PRN`, `COM1`), a trailing-dot name,
and a >4000-character name were not served (no matching file on the server),
so the client wrote nothing: no device node was created, and the long name is
still skipped (matching the tier-2b finding).

## Conclusion

A hostile server **cannot** make 5.12 write a downloaded terrain texture
outside its own folders through the file name: the client sanitises to the
basename and confines the write to `levels3d\images`. Clean result — no
traversal escape, nothing to flag as a security hole.

The decisive point is client-side. Our own gserver's file lookup happens to
be by basename (so it returned the marker for the path-bearing names and
nothing for the absolute/device forms), but the client received bytes
*labelled* with the full traversal path and still confined the write under
its own basename. A server that echoed the full path would not change the
outcome, because the client does not honour the directory part.
