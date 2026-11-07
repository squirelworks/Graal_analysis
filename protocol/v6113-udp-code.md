# UDP code in unpacked 6.1.1.3

Date: 2026-11-07. Static read of the unpacked 6.1.1.3 listing, set against the two capture notes. Nothing was run. Tags: **[bin]** this listing · **[cap]** the capture notes.

The captures did not show Graal UDP on the game port. That does not mean the listing has no UDP code. It does.

## What is in the image

A socket opener takes a flag. With the flag clear it opens a stream socket and connects, and the connected state is the one that raises `onConnect`. With the flag set it opens a datagram socket, binds it, and marks the socket ready to send with `sendto`. **[bin]**

The only caller of the datagram opener is the script method whose failure text is "Binding of port". The game connect function, the one that ends in the connected state, does not call it. **[bin]**

A datagram socket's receive path raises `onReceiveUDPData`. The description string is "received UDP data". That callback is not on the TCP connect path. **[bin]**

## Against the captures

`protocol/v6113-list-capture.md` is TCP only. `protocol/v6113-udp.md` finds no client datagram that shares a remote with the TCP 14900 sessions, and no datagram on UDP 14901. The listing agrees that the connect path which speaks the `GNP1905C` hello does not open the datagram socket. The datagram opener remains available to script. **[bin][cap]** (`protocol/v6113-list-capture.md#what-the-capture-shows`, `protocol/v6113-udp.md#what-this-capture-shows`)
