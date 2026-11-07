# Native receive handlers, unpacked 6.1.1.3

Static read of the unpacked 6.1.1.3 listing, compared with the unpacked
6.0.3.7 listing. Nothing was run. [bin]

The script method that installs incoming handlers reads a script list of
numbers, converts each number to one byte, and walks that buffer as pairs.
The first byte of a pair is the wire id. The second byte chooses the
handler:

- 255 clears that wire id.
- 254 stores a sentinel that the caller treats as "do not call".
- 253 stores the wire id on one connection field and clears the slot.
- 252 stores the wire id on a second connection field and points the slot
  at one fixed function. That function is not one of the 95 named below.
- Any other second byte below 95 loads the native function at that index.
  A second byte of 95 or more is skipped.

The clear method zeros all 256 wire-id slots. Until a script passes pairs,
no wire id has a handler. The install method is the only caller of the
pair walk, and it builds those bytes from the script argument. It returns
without writing slots when the list has fewer than two numbers. No default
pair list is compiled into the image.

## Empty slots

Index 90 is the only empty slot. The other 94 indexes each hold a function.

## Against unpacked 6.0.3.7

The 6.0.3.7 listing has no copy of this installer: no test of the handler
byte against 252–255, and no 95-wide table of native receive functions.
6.0.3.7 still uses its fixed incoming switch. [bin] (client-internals/unpacked-6037.md)

## Packet 104

6.1.1.3 has no compiled receive case for wire id 104. The only case 104 in
the image sits in the GS2 opcode switch, beside the neighbouring GS2
opcodes. A script could still map wire id 104 onto a slot at runtime.
Nothing in the image does that.

## Slots with a method name

The name is the script method whose function is this slot, or the method
the slot tail-calls after reading a header. "One string" means the slot
takes the packet body as one length-counted string and does not read a
fixed header of biased bytes or base-128 integers. A 3-byte or 5-byte
integer is base 128, and each wire byte is the digit plus 32. A "biased
byte" is the same plus-32 storage for one byte. Byte positions are
1-based, so the first byte is byte 1.

| Index | Name | What this slot reads |
| ---: | --- | --- |
| 0 | `tclient_setserverwarp` | one string |
| 1 | `tclient_setplayerprops` | one string |
| 5 | `tclient_deleteweapon` | one string |
| 6 | `tclient_setflagdata` | one string |
| 7 | `tclient_unsetflagdata` | one string |
| 10 | `tclient_setserversignature` | biased first byte, then the method |
| 11 | `tclient_setserveroptions` | length at least 5; one 5-byte integer, then the method |
| 12 | `tclient_setadminmessage` | one string |
| 13 | `tclient_setgraal2002server` | one string |
| 14 | `tclient_setserverlisterconnect` | one string |
| 15 | `tclient_getwindowlist` | one string |
| 16 | `tclient_gethavewindow` | one string |
| 17 | `tclient_setcookie` | one string |
| 18 | `tclient_settimevar` | length at least 4, then the method |
| 19 | `tclient_downloadimagefailed` | one string |
| 20 | `tclient_downloadimagewasok` | one string |
| 21 | `tclient_downloadstart` | one string |
| 22 | `tclient_downloadsetsize` | one 5-byte integer, then the method |
| 23 | `tclient_downloadend` | one string |
| 25 | `tclient_setfileupdate` | one string |
| 29 | `tclient_setfolderlog` | one string |
| 33 | `tclient_setserverlevel` | one string |
| 34 | `tclient_setlevelfailed` | one string |
| 38 | `tclient_setregged` | one string |
| 39 | `tclient_setisghost` | biased first byte, then the method |
| 40 | `tclient_setghostmessage` | one string |
| 41 | `tclient_setghostsnear` | biased first byte, then the method |
| 42 | `tclient_setstaffguilds` | one string |
| 43 | `tclient_setstatusicons` | one string |
| 44 | `tclient_setrpgmessage` | one string |
| 45 | `tclient_readsign` | one string |
| 47 | `tclient_deleteallnpcs` | one string |
| 48 | `tclient_setlevelboard` | one string |
| 49 | `tclient_setrawboard` | one string |
| 50 | `tclient_setrawboard2` | one string |
| 51 | `tclient_setboardmodify` | one string |
| 52 | `tclient_setboardmodify2` | length at least 6 |
| 53 | `tclient_setnpclevel` | one string |
| 54 | `tclient_setisleader` | one string |
| 55 | `tclient_addlevellink` | one string |
| 61 | `tclient_deletelocalnpcs` | one string |
| 66 | `tclient_freezeplayer` | one string |
| 67 | `tclient_unfreezeplayer` | one string |
| 69 | `tclient_setlevelmodtime` | one 5-byte integer, then the method |
| 77 | `tclient_adddefaultweapon` | biased first byte, then the method |
| 92 | `tclient_setpackageend` | one string |
| 93 | `tclient_setrawlen` | one 3-byte integer, then the method |

Index 9 has a method string, but the decoded bytes contain a zero in the
middle (`tclient_setdisconne`, a zero byte, then `tmessage`). That is not
a clean name, so it is not listed above. The slot copies one string.

## Slots with no method name

These functions are in the 95-wide table and are not the function pointer
of any `tclient_*` method. Where the body calls a named method, that call
is stated. Where a fixed header was visible, it is stated. Otherwise the
field split was not recovered.

| Index | What was visible |
| ---: | --- |
| 2 | biased first byte, then a slice of the string |
| 3 | three 5-byte integers, then a slice |
| 4 | first byte and second byte, neither biased |
| 8 | first byte and second byte, neither biased |
| 24 | length at least 7; a 5-byte integer and a biased sixth byte |
| 26 | length at least 9; a biased first byte and two 5-byte integers, then `tclient_setfilekey` |
| 27 | length at least 7; a 5-byte integer and a biased sixth byte |
| 28 | a function; no fixed header |
| 30 | a function; no fixed header |
| 31 | biased first byte and biased second byte |
| 32 | biased first byte, biased second byte, and a plain third byte |
| 35 | first byte and second byte, neither biased |
| 36 | biased first byte |
| 37 | biased first byte |
| 46 | first, second and third bytes, none biased |
| 56 | one 3-byte integer, then `tclient_setnpcscript` |
| 57 | a function; no fixed header |
| 58 | one 3-byte integer |
| 59 | first, second and third bytes, none biased |
| 60 | length at least 5 |
| 62 | length at least 16 |
| 63 | first byte and second byte, neither biased |
| 64 | a function; no fixed header |
| 65 | biased first byte and biased second byte, then `tclient_pushaway` |
| 68 | six bytes, the last three biased |
| 70 | a function; no fixed header |
| 71 | a function; no fixed header |
| 72 | a function; no fixed header |
| 73 | first byte and second byte, neither biased |
| 74 | first byte and second byte, neither biased |
| 75 | biased first byte, three plain bytes, a biased byte, then `tclient_addlevelchest` |
| 76 | a plain first byte and a biased second byte |
| 78 | first byte and second byte, neither biased |
| 79 | first byte and second byte, neither biased |
| 80 | biased first byte and biased second byte, then `tclient_removebomb` |
| 81 | first byte and second byte, neither biased |
| 82 | first byte and second byte, neither biased |
| 83 | first byte and second byte, neither biased |
| 84 | length at least 5; three biased bytes |
| 85 | biased first byte and biased second byte, then `tclient_removeextra` |
| 86 | three biased bytes |
| 87 | biased first byte and biased second byte, then `tclient_removehorse` |
| 88 | biased first byte |
| 89 | three plain bytes and a biased fourth byte, then `tclient_hurtbaddy` |
| 91 | biased first byte |
| 94 | a function; no fixed header |

Several other `tclient_*` methods exist in the image and are not slots in
this table, including `tclient_setplayerprops`'s neighbours
`tclient_setweapon`, `tclient_setscript`, `tclient_setnpcprops`,
`tclient_setbaddyprops`, `tclient_setotherplayerprops`,
`tclient_settoallmsg` and `tclient_setprivatemessage`. They are script
methods. They are not entries 0–94.
