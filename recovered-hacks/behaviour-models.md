# Trainer behaviour models

Date: 2026-11-01. Static read of the trainer images. Copies were unpacked with UPX where the packer was intact. No recovered PE was executed. No window was focused, and nothing was sent to a client.

These notes are the observable loops: which key, how many times, how long it waits, and whether it looks at a window title. `[bin]` is what was read out of the image or its bundled text. `[inf]` is a reading of that evidence, not a second measurement.

An earlier static pass already named AutoD, AutoIdle, AutoS, WaterGet v1.1, Random Walker, and the caps-lock utility. Those loops were read again here. They match. The new reads are Graal Load, the two AFK bots, Prayer and its helper, the window-retitle tool, Water Get v1.0, and the text sender. Digger is still truncated. The miner archive was not downloaded.

`reference_macros.py` is a table of the loops below. A unit test replays the table in this process. It does not open a socket, call a window API, or start a program.

## What a server can see

Every sample below types into a classic client window, or writes text into one. None of them speaks the game protocol itself. A world checker sees the resulting actions: dig, use, walk, chat. The gaps below are the client-side waits, not a server cooldown.

## AutoD `[bin]`

Yes/no box. No exits. A second box says it was made in 2001 and to stop it from the tray. Then, forever: sleep 1 millisecond, send `d`. No window check. No chat.

## AutoS `[bin]`

Three lines. Repeat forever, send the two characters `s#`, end the repeat. The script sets no key delay and no sleep, and it does not look at a window.

## AutoIdle `[bin]`

No sleep and no window check. One pass sends 48 arrow taps, then goes back to the start. The pass is left, right, six times; one left and three rights; left, left, left, right, right, right, four times; then left, right, five times. The exact list is `AUTOIDLE_KEYS` in the reference module.

## Graal Auto Key `[bin]`

This is the program the other RpgWarrior tools call "the key". It does not send a game key.

A box says the operator has 5 seconds to focus the client. The script then sleeps 2 seconds (the box text and the sleep disagree). It reads the active window's title and renames that window to `Graal Auto`, then exits.

Tools that look for `Graal Auto` do nothing useful until this has run. WaterGet v1.1 does not look for that title.

## WaterGet v1.1 `[bin]`

Ok/cancel box, author named in the box. Cancel exits. The script sets the key delay to 300 milliseconds and loops: send Down twice, send `a`, sleep 2000 milliseconds. It does not check a window title. The bundled howto is the operator's setup (water can, facing down on a source, client focused), not an extra key.

## WaterGet v1.0 `[bin]`

Different loop from v1.1. It requires the window titled `Graal Auto`.

After the ready box it asks for two idle directions (the prompts' examples are Left and Right), tells the operator to equip a water can, and waits for `Graal Auto`. One pass, only while that window is active:

- key delay 100 milliseconds
- send `S`, sleep 1000 milliseconds, nineteen times
- sleep 2000 milliseconds
- key delay 50 milliseconds
- send the first direction twice, sleep 500 milliseconds
- send the second direction twice, sleep 500 milliseconds

If the window is not active it shows a waiting box, sleeps 1000 milliseconds, and resumes when the window is active. If the window was never renamed, it says to use the key first and exits.

## Random Walker `[bin]`

Looks for a top-level window titled `Graal Auto`. A box says to focus it; the script sleeps 2000 milliseconds and exits with "use the key first" if that window is not active. An ok/cancel box uses the same wording as the water tool. Cancel exits.

The loop sets the key delay to 200 milliseconds and draws an integer from 0 through 5. Zero sends nothing. 1 is Up five times, 2 is Down five times, 3 is Left five times, 4 is Right five times, 5 is `S` five times. Between those checks, if the window is not active, it shows a waiting box and sleeps 1000 milliseconds.

## Prayer `[bin]`

The script body was recovered. It is not still encrypted. The package is two macros.

`Graal Prayer` requires `Graal Auto`, same 2 second focus wait and "use the key first" exit as the walker. It asks for three operator strings. The prompts' examples are a prayer-weapon shortcut `R`, a naginata shortcut `E`, and an idle direction `LEFT`.

One pass, while `Graal Auto` is active:

1. Key delay 100. Send Tab.
2. Key delay 0. Three times: send the chat text `/use_skill praying` and Enter, then sleep 2000 milliseconds.
3. Sleep 500. Key delay 100. Send Tab. Sleep 500.
4. Send the naginata shortcut. Sleep 1000.
5. Start the helper in the `data` folder next to the script.
6. Key delay 0. Send the idle direction once.
7. Key delay 100. Send `s` ten times.
8. Sleep 500. Send the prayer-weapon shortcut. Sleep 500. Send Right. Sleep 500. Send the idle direction twice. Sleep 1000.

The same waiting box and 1000 millisecond sleep apply when the window is not active.

The helper (`data.exe`) sets the key delay to 100, sends Up ten times, and exits. It does not check a window. `[bin]`

## Graal Load `[bin]`

VB6, title "Graal Load". The form label says to put the text files beside the program and to type `load<file.txt>` in the client. The example on the label is `load<bomb.txt>`.

The program enumerates windows and reads their text. For each line of the chosen file it writes that line into the target window, sends the Return key down (no key-up in that loop), and sleeps 150 milliseconds. It does not open a socket.

The bundled `bomb.txt` is 164 lines: appearance lines, a phrase typed out one fragment per line, a countdown from 100 down to 0, then `!!BOOM!!` and more appearance lines. That file is chat and costume text. The loader's timing does not depend on the words.

## AFK Bot `[bin]`

VB6. The only imported runtime is the VB runtime, so the keystrokes go to whichever window the operator focused. The form timer interval is 3000 milliseconds. The readme says the operator has 3 seconds after Start to click the client chat box, or the bot turns itself off, and that it then types three phrases, one every 3 seconds, down the list.

The three default phrase boxes are `I am AFK`, `I am using an AFK Bot`, and `AFK Bot created by Zorg`. `[inf]` The readme's "down the list" is the order those boxes are filled, top to bottom as the operator sees them. The image stores the three strings; it does not store a sentence that says which box is first.

## AFK Scroll Bot `[bin]`

Same author, same focus rule, different timer. The form timer interval is 100 milliseconds. A slider is labelled Wait Time. The readme says that slider is how many seconds the operator has to click the chat bar before typing starts, and that the bot then scrolls one phrase across chat. The default phrase box is `Scroll Text Here`.

`[inf]` The 100 millisecond timer is the scroll tick. The per-character shift is not a string in the image, so the reference table does not invent one. The start wait is whatever the operator set on the slider; the image does not fix that number.

## Graal Text Sender `[bin]`

VB6, "Graal Text Sender" v1.3.5. The form timer interval is 100 milliseconds. The operator types the phrase and can set a timer per mode. No default phrase is stored.

Modes on the form: Word Scroller, Middle In-Out Letters, Word Stay, Two Words Repeat, Letter by Letter To-Alls, Letter by Letter Shout Outs. Word Stay has a message button and no timer button. The others have both. Each mode has On and Off.

The program looks up a window, and the client-name token is one of the strings it carries. It can send keys and send a window message. `GetAsyncKeyState` is present. `[inf]` Which key it polls was not recovered; there is no phrase list or log path beside it, so this pass does not treat it as a key logger.

The reference table does not include a GTS loop. The phrase and the per-mode wait are whatever the operator typed.

## Not recovered

- **Digger.** The zip's compressed stream ends early. The surviving image is a partial UPX file (36111 bytes written, 41893 declared). The script block is not in the surviving bytes. The howto, which did survive, says to equip a shovel, stand on grass, focus the client, and click ok. It does not name the key or the wait. `[bin]`
- **Miner.** Not downloaded. The archive is the one the Drive abuse flag blocks.
- **Caps-lock utility and the Win32 listserver.** Already described. Not opened again.
