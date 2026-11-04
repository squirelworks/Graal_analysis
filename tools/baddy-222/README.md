# baddy-222

Two small tools for the 2.22 baddy notes (`client-internals/baddies-222.md`, `server-notes/baddies-serverside.md`). Neither stores any game data: they read your own files when you run them.

## gen_ganis.py

Writes GANI files that draw a built-in baddy the way the 2.22 client does, from the `arrays.dat` of your own install (arrays 20, 22 and 24) and the baddy's image.

    python gen_ganis.py path/to/arrays.dat out/ --image baddygray.png --prefix baddy

Files: `baddy-walk`, `-stand`, `-look1`, `-look3`, `-hurt`, `-aim`, `-die` and `-gone`, four directions each. The worked script `server-notes/baddies/graysoldier-222.gs1` uses these names.

## check_capture.py

Checks a decoded 2.22 baddy capture (one message per line, `C>S f210 +20790ms BADDYPROPS len12 <hex>`) against the step rules in the spec: counters per mode, the counter a mode starts with, hunt step sizes, knockback lengths, and the `PLI_BADDYHURT` encoding.

    python check_capture.py lan-222kill-baddy.txt lan-222d-baddyprops.txt

It prints one line per rule with pass and fail counts and exits non-zero when anything failed. The captures are in the project files, not in this repository.
