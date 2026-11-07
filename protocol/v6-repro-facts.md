# Field order, chat arguments and bind events in unpacked 6.x

Date: 2026-11-07. Static read of the unpacked 6.0.3.7 and 6.1.1.3 listings. Nothing was run. Tags: **[bin]**.

`protocol/v6113-hello.md` already has the token, the `I` / `L` / `T` / `E` letters, and when `E` is 0, zlib or bzip2. This page is the part that note does not spell out: the order the header is filled, the id-50 prefix, what `onToall` is given, and the bind events.

## How a setprotocol header is filled

`setprotocol` stores the template length as the header length and finds each of `I`, `L`, `T` and `E`. The width is how many times that letter is repeated, capped at 4, written big-endian. A numbered send is refused until both `L` and `T` were found. The header is cleared to zero first, so a template byte that is not one of those four letters stays zero.

On a numbered send the fields are written in this order:

1. `T`, the packet id.
2. `I`, the counter, when the template has `I`. The counter starts at 1 and then increases by one.
3. `E`. The zlib threshold is 48 bytes and the bzip2 threshold is 4096 bytes, as the hello note says. Block size 5 is the value passed to the bzip2 compressor.
4. `L`, the header length plus the body length after that compression.

If the compressor returns nothing, `E` is written again as 0 and the original body is what goes out. **[bin]**

`sendraw` is the send whose id is −1. It appends the caller's bytes and does not write a header, an id, or a new counter value. `senddata` is the numbered send. **[bin]**

## Ids 93 and 163 on the generation-5 path

While 6.1.1.3 is still on the generation-5 framer, a send of id 93 or id 163 first sends id 50. The body of that id 50 is a three-byte length of the original body length plus 2, capped at the raw-data cap, each byte stored as a seven-bit group plus 32. The original packet is then written as id plus 32, the body, and a newline. Those two ids skip the newline refusal. Every other generation-5 send that contains a newline is refused with "Illegal characters in the outgoing data". A buffer whose length reaches 4096 bytes is flushed. **[bin]**

The 6.0.3.7 send function has the same newline refusal, and it skips that refusal for ids 93 and 163. It does not itself send the id 50 prefix. Where 6.0.3.7 would add that prefix: not found. **[bin]**

## What onToall is given

The event is registered with parameter letters `o` then `s`. The description begins "received a toall message: player obj". The rest of that sentence is truncated in the listing. **[bin]**

The function that feeds the event, when the body is longer than two bytes, reads the first byte and the second byte as an id: (first minus 32) times 128, plus (second minus 32). The third byte has to be at least 32. Its value minus 32 is the number of text bytes, and those bytes start at the fourth byte. It then pushes `onToall` with the player object for that id and that text. A body of two bytes or fewer does not push the event. No compiled caller of this function was found, and no PLO id is assigned to it. **[bin]**

## Bind events

The script method that logs "Binding of port " has no plaintext name in the image. The name: not found. When its allow check fails it logs that text plus the port and does not open a socket. When the open succeeds it raises `onBind`, described as "the bind() call was successful", with an empty parameter list. When the open fails it raises `onBindFailed`, whose description begins "the bind() call failed, wrong port", also with an empty parameter list. The rest of that sentence is truncated. **[bin]**

`onReceiveUDPData` is registered with parameter letters `s`, `s`, `i`. The description begins "received UDP data: data, sender ip". The rest is truncated. **[bin]**

## Before the connector script runs

6.1.1.3 looks up `StartScript_Connector`. If that object is missing it looks up `StartScript_Fail`. If `onCreated` exists on the object, and the call's SSL argument is set, it writes `scriptip`, then `scriptsslcipher`, then `scriptsslsubject`, then `scriptsslissuer`, and then runs the script. The login bytes that script sends: not found. The Mac 6.11 note's `con.png`, `con.gs` and `conf.gs` names are not plaintext in this Windows image, so that fetch order was not found here. **[bin]** (`protocol/v6x-clients.md#connector-request`)
