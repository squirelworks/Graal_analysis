# Named (non-guest) logins for real 5.24r4 and 6.03r7 in a lab

Date: 2026-11-14. A lab run with real clients, plus a static read of the 6.03r7 Linux client's script-function table. Tags: **[lab]**, **[bin]**.

## The problem

Real 5.24r4 and 6.03r7 log in to the Login gserver as `guest`. After the `serverwarp` they reach the world as `guest` too. GServer-v2 treats a guest account as load-only, so flags the player gets are never written to an account file. That meant a lab could not check whether script-set player flags are saved (seihai-gserver-v2 #75). **[lab]**

## The method

The client has script functions that set the account name and password it uses for its next connection. A clientside GS2 weapon on the lab Login gserver calls them before the warp to the world.

The Login gserver needs this server option:

```
default_scriptengine_client = gs2
```

A `//#GS2` line after `//#CLIENTSIDE` inside the weapon was not honoured, so the option is needed. **[lab]**

The weapon is listed in the Login gserver's `(defaultaccount).txt`, so every guest receives it:

```
GRAWP001
REALNAME -acctX
IMAGE
SCRIPT
//#CLIENTSIDE
function onCreated() {
  adventure_setaccountname("<ACCOUNT>");
  adventure_setpassword("<PASSWORD>");
  echo("acctX set");
}
SCRIPTEND
```

The order of the login flow:

1. The client logs in to Login as `guest` and receives its weapons. `onCreated` runs as each weapon arrives.
2. The player enters the Login start level. A level NPC there runs `if (playerenters) { serverwarp <WORLD>; }`.
3. The client reconnects to `<WORLD>`, and its login packet now carries `<ACCOUNT>`.

No delay was needed: on both clients, the weapon's `onCreated` ran before the reconnect. The client caches weapon scripts by name, so give the weapon a new name each time you change its script. **[lab]**

## 5.24r4 and 6.03r7

| | 5.24r4 (`G3D15010`, Windows, under Wine) | 6.03r7 (`G3D0511C`, Linux) |
|---|---|---|
| Setters run, no "not found" errors | yes | yes |
| World login under `<ACCOUNT>` | yes | yes |
| `getloginaccountname()` after the setter | not tested | still `guest` |

Only the 6.03r7 table was decoded (see below). 5.24r4 accepted the same names unchanged. Two 5.24r4 clients set to the same account get the gserver's usual "Attempted double login" and a reconnect loop. That is normal behaviour, not a fault in the method. **[lab]**

The 3.x Torque-style call `Adventure.setAccountName(...)` does not exist on 6.03r7. The client reports `Function Adventure.setAccountName not found`. The underscore form is the one that works. For the 3.x tables, see `torque/304-adventure.md`. **[lab]**

## What the server sees

- On Login, both clients log in as `guest`.
- On the world, the login line reads `New login: <ACCOUNT> [New Client (2.22+)] [G3D15010 (5.24)]` or `... [G3D0511C (6.037 (Linux))]`.
- The lab world ran in localhost mode, which logs that it accepted `<ACCOUNT>` without listserver verification. So the password was not checked. A world that verifies accounts through a listserver was not tried.

**[lab]**

The account file was written fresh before each login and saved at logout. The weapon `GS1Test` is translated GS1 that runs `set gs1flag; setstring gs1str,hello; unset gs1old;` every second.

```
before                after (both clients)
NAME <ACCOUNT>        ...
WEAPON -gr_movement   FLAG gs1str=hello
WEAPON GS1Test        FLAG gs1flag
FLAG gs1old           (no gs1old)
```

Server: seihai-gserver-v2 `seihai` at `4991f9d8`, which contains #76. That build has no NPC-server and was built with packet logging. In the same run:
- `-gr_movement` sent 0 `gr.x`/`gr.y`/`gr.z` writes a second, standing still and walking.
- The repeated `GS1Test` writes (68 on 5.24r4, 150 on 6.03r7) got one `PLO_FLAGSET`/`PLO_FLAGDEL` echo each.

**[lab]**

## How 6.03r7 stores its script-function names

The Linux 6.03r7 client keeps its engine-provided script functions in one table. Each entry holds:

- the name;
- the return type;
- an argument signature (`s` string, `i` int, `d` double, `b` bool, `o` object, `X` variable);
- the handler.

Lookup ignores case. **[bin]**

The names are stored obfuscated. For a name of length *n*, the stored byte at position *i* is about (244 − 4·(c + *i*) − *n*) mod 256, where *c* is the character. Two consequences:

- Names that share a prefix store that prefix the same way, offset only by their length.
- After about the 12th character the low two bits drift.

To decode, round (244 − 4·*i* − *n* − byte) mod 256 down to a multiple of 4 and divide by 4. That gives the character mod 64. Of the four candidates, pick the lowercase letter, `_` or digit. Because the result is only known mod 64, a decoded `q` can be a digit: from known names (`lay2`, `say2`, `openurl2`) it is probably `2`. **[bin]**

The key was found by fitting stored = (k·c + cᵢ) mod 256 per position against known GS2 builtin names of the same length (`abs`, `random`, `findweapon`, `keydown` and so on). k = −4 with cᵢ = 244 − 4*i* won clearly. The table's ordinary builtins then decode to real names, for example: `addtiledef`, `callweapon`, `disabledefmovement`, `findnpcbyid`, `freezeplayer`, `getkeycode`, `hitobjects`, `keydown2`, `loadmap`, `onwall2`, `opengraalurl`, `requesttext`, `sendtorc`, `setshootparams`, `triggeraction`, `updateboard`, `wraptext`, `worldx`. **[bin]**

Client-side names that look useful (argument signature in brackets):

- Account: `adventure_setaccountname(s)`, `adventure_setpassword(s)`, `adventure_setnickname(s)`, `getloginaccountname()`, `adventure_geteditnickname()`, `adventure_geteditaccountnames()`
- Connection: `adventure_reconnect()`, `adventure_openserverlist()`, `isofflinemode()`
- Options and window: `adventure_savegraaloptions()`, `adventure_setgraalcontrolrecreate(b)`, `adventure_setfullscreen(b)`, `isfullscreenmode()`
- Chat and PMs: `adventure_setchat(s)`, `adventure_openexternalpm(o)`, `adventure_openexternaloptions()`
- Input: `adventure_invokekeyevent(i,i,s,i)`, `adventure_invokemouseevent(i,i,d,d,i,b)`
- Files: `adventure_requestfiledeletion(s)`, `adventure_requestfolderdeletion(s)`, `adventure_requestfilerename(s,s)`, `adventure_requestfilesmove(s,s)`, `adventure_uploadfile(s)`
- Install: `adventure_getwindowlist()`, `adventure_getinstallationpath()`, `adventure_installgraal(s,b,b)`, `adventure_addmenulink(s,s,s)`, `adventure_adddesktopicon(s,s,s)`

Only the two account setters were exercised. The other names are a static read. **[bin]**

## Limits

- The password was not checked, because the world ran in localhost mode.
- `getloginaccountname()` was not tried on 5.24r4.
- The 5.24r4 table was not decoded; only the names above were called on it.
- No pcap was taken. The evidence is the world gserver's packet log, its console, the client consoles and the account files from before and after. The lab account names in those logs are owner-held and not published.
