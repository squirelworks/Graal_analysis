# Remaining trainer reads

Date: 2026-11-01. Static read of the four samples the behaviour note left open. No recovered PE was executed. A copy of the digger image was handed to UPX, which refused it. The caps-lock packer was not run. AutoD, Prayer, Graal Load, the water tools, and the walker are not re-opened here.

`[bin]` is a value read out of the image, the form, or the readme. `[inf]` is a reading of that evidence.

## AFK Scroll Bot `[bin]`

Visual Basic 6, not packed. The form timer interval is 100 milliseconds. The slider is labelled Wait Time. Its saved block is the slider's own range (a ten, a five, and ones among the fields). No control is named for a shift, and the readme does not give one. The default phrase is `Scroll Text Here`.

The start procedure reads one control value and multiplies it by ten before storing a countdown. Each tick subtracts one. While the countdown is still at least one, the tick does not type. The only numeric control is that slider, and the readme says it is a number of seconds. Ten ticks of a 100 millisecond timer is one second. `[inf]`

Once the countdown has finished, every tick does this to the phrase:

- take the length minus one, from the end
- take one character from the start
- join those pieces with the long piece first
- write the result back over the phrase
- pass it to the runtime's send-keys call

The shift is one character: the first character moves to the end. It is in the timer procedure. It is not in the form and not in the readme. `scroll_phrase` in `reference_macros.py` replays that join. A one-character phrase stays as it is.

Immediately before send-keys, the constant 13 is passed to the runtime's text helper. That is the carriage return that submits the chat line. `[inf]` The status line is rebuilt as `Sent `, the tick count, and ` AFK Messages`. That counter is not the shift.

## Graal Text Sender `[bin]`

Visual Basic 6, not packed. "Graal Text Sender" v1.3.5 on the form. The form timer interval is 100 milliseconds. The resource directory holds an icon and a version block. The version block names the product and the file version `1.03.0005`. It does not name a key. There is no other resource.

The image declares `GetAsyncKeyState` and has a resolver stub for it. Nothing in the image calls that stub. The declare next to the name holds the library and a cache slot, not a virtual-key constant. The form strings are the mode titles, the timer prompts, and the about line. None of them names a key.

The key tested by the key-state check is not in the resources, and there is no call that would show it.

What the image does call is window lookup, and a send path that sets the window text and then posts key-down and key-up for Return. That submits a line. It is not the polled key.

## capslock `[bin]`

The executable beside the readme. Ten sections, one of them the packer's. UPX does not recognize it. The code section is effectively random. The packer section is not.

The stub saves registers and jumps to a loop that adds a constant to a backward run of dwords. After that loop the bytes are not straight-line code. Relative calls that would leave the stub land on addresses that are not code. The stub does not call through the import table.

The import table lists the packer's loader trio plus `keybd_event`, `GetKeyboardType`, a registry query, and small COM and GDI helpers. `keybd_event` is not called from the stub. A version string says the program turns the caps-lock key on and off. The readme says the same, and that the command line accepts on or off. No socket wording appears.

The body stays packed. The stub was not executed to unpack it.

## Digger `[bin]`

The zip was read again. The local headers are the howto, then the executable. The howto inflates completely: six numbered steps, equip a shovel, stand on grass, focus the client, click ok. No key and no wait. The executable's deflate stream ends after 36111 bytes. The local header declares 41893 uncompressed bytes. The central directory is a single entry, named for the executable, declaring 44013 uncompressed bytes and pointing at the start of the file. Both declarations are larger than what inflated. The inflated checksum matches neither header.

UPX reports an invalid overlay and will not unpack the partial image. The packed section is short of its declared size, and the resource section is entirely past the end of the file. The import directory is past the end as well.

The surviving bytes contain `AutoIt` and a broken v2.63 splash fragment, plus smashed pieces of the runtime's own words: a fragment of its key-name list, the name of its key-delay command, and the script-path token. Those are not a script. The script-start marker is absent. `Sleep` is absent. There is no chosen key and no wait count. They are not invented from the fragments.

## Not in this note

The miner archive was not downloaded. It is the one the Drive abuse flag blocks.
