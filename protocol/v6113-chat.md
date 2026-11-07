# How unpacked 6.1.1.3 receives another player's chat

Date: 2026-11-07. Static read of the unpacked 6.1.1.3 listing. Nothing was run. Tags: **[bin]**.

## The arrival path

Another player's line is the script event `onToall`. The event is registered with the text "received a toall message", and the parameter text beside it names a player. Two sites in the native toall handler push that event name. **[bin]**

That handler is one of the `tclient_*` methods (`tclient_settoallmsg`). Those methods run when the TCP incoming table calls a native handler. The UDP receive callback raises `onReceiveUDPData` and does not push `onToall`. The line this image delivers to script is TCP. **[bin]**

## Which PLO

No compiled case assigns a PLO id to `onToall`. The wire id is whichever pair `setindatahandlers` installed for that handler, and that pair is not in the image. A fixed PLO number for this chat line: not found. **[bin]**

`onSendToAllChat` is the outgoing slot. It is the client sending, not the line arriving from someone else. A string "received a PM from a player" is also present. It was not traced to a wire id. **[bin]**
