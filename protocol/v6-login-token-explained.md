# Where a Graal 6.11 client's login token comes from

Date: 2026-11-11. A plain-language account, written for readers who are curious about how this was worked out but who do not read protocol notes for fun. The technical claims carry the usual source tags in the footnotes, and the notes they point to hold the detail.

## The puzzle

When a Graal client connects to a game server, the very first thing it says is a short password-like word, eight characters long, called the version token. It works like a secret handshake. The server reads it and decides which "dialect" of the protocol the client speaks. For twenty years of Graal clients that word was baked into the program. A 2.x client says `GNW…`, a 3.x to 6.03 client says `G3D…`, and the rest of the word is a date stamp for the build[^tokens].

The newest desktop clients we have studied, Windows 6.113 and Mac 6.111, broke that pattern. A capture of the Windows client showed it opening with `GNP1905C`[^cap]. Yet when we searched the program for those eight characters, in plain form or scrambled, they were not there[^nostr]. The obvious guess was that the client *computes* the token somehow, perhaps from its version number. The digits `1905` do not come from `6.113` by any rule we could find, and that question stayed open in the reference manual[^manual].

The answer turned out to be simpler and more interesting: the client does not make the token at all. The server tells the client what to say.

## How the client gets its instructions

Before a 6.11 client touches the game server, it phones home for a set of instructions. The sequence goes like this[^conn]:

1. The client tries a secure (HTTPS) connection to a "connector" web server and checks the server's certificate against a list built into the program.
2. It then asks that web server for a file called `conf.gs` over plain HTTP. The request carries an encrypted description of the client (its platform, version and build date).
3. The web server answers with a small encrypted script. The client loads it under the name `StartScript_Connector` and runs it.
4. That script, not the client, opens the connection to the game server and decides what to send.

So the program you download is in a sense only half a client. The other half, the part that knows how to start a conversation with the game server, arrives fresh from the server every time you log in.

## What the reply looks like

The `conf.gs` reply we studied is 5,154 bytes long, and it comes in two labelled pieces. First comes a four-byte number saying "the next piece is 256 bytes", then those 256 bytes. Then comes a second four-byte number saying "the next piece is 4,890 bytes", then the 4,890 bytes of encrypted script. That is 4 + 256 + 4 + 4,890 = 5,154 bytes[^layout].

The 256-byte piece is a digital signature. The company that runs the servers holds a secret key (an RSA key, 2,048 bits long), and the client carries the matching public key inside it. To sign, the server first boils the 4,890-byte script down to a 32-byte fingerprint with SHA-256, a standard function that turns any input into a fixed-size digest, so that changing even one bit of the input changes the fingerprint completely. Then the server seals that fingerprint with its secret key. The client unseals the signature with the public key, computes the fingerprint of the script itself, and compares the two. If they match, the script really came from the holder of the secret key and was not changed on the way[^sig].

One small detail is unusual. The common standard for RSA signatures wraps the fingerprint in a short label that says "this is a SHA-256 fingerprint" before sealing it. Graal's signature seals the bare 32-byte fingerprint with no label[^sig]. It is no less secure for that, but it is a detail anyone who wants to check these signatures with off-the-shelf tools has to know about.

The order matters too. The client checks the signature *before* it decrypts and runs the script. A reply that fails the check is never run[^sig].

## What the script says

Once decrypted, the connector script is short and readable. In the part that matters here it does three things, in this order[^script]:

- `setProtocol("EILLLT")` sets the shape of every packet header that follows. Each letter is one byte of header: `E` says how the body is compressed, `I` is a running packet counter, the three `L`s hold the packet length, and `T` is the packet type. That gives a six-byte header, which matches the six bytes seen right after the token in the capture[^hdr].
- `sendRaw("GNP1905C")` sends the eight characters exactly as written, with no header and no packet type in front of them.
- `setEncryptionOut(…)` turns on encryption for everything the client sends afterwards, with a key given in the script. (We leave the key itself out of this note on purpose.)

That is the whole answer. The token is a literal string, written into the server's script by whoever wrote that script. The client does not compute it, convert it, or look it up. It sends what the script tells it to send[^script].

## How we know

Two independent checks, on two different machines and operating systems, point to the same answer.

The first was a replay. A Mac OS X 10.7 ("Lion") virtual machine, with no internet, ran an unmodified Mac 6.111 client, and a small lab web server handed it a previously captured `conf.gs` reply. The client checked the signature, accepted it, decrypted the script and ran it. Its memory was then saved to a file, and the decrypted script, with `setProtocol("EILLLT")` followed by `sendRaw("GNP1905C")`, could be read straight out of it[^lion].

The second was a trace of the running Windows 6.113 client in a debugger. The token was absent from the client in every form a program could store it: not as plain text, not scrambled, not as separate characters put together at run time. The only related thing baked into the program is the *name* `StartScript_Connector`, the label it gives the script it is about to receive[^wintrace].

Together they rule out the "the client converts something into the token" idea. A token that is not in the program, and that turns up word for word inside a script the program downloads, comes from the script.

## The older clients really did convert something

The question "how is the conversion done?" was a fair one, because older clients do something that looks like it. A Windows 6.03r7 client stores its token inside the program, but not in plain sight. It keeps eight scrambled bytes, and a small routine unscrambles each byte using the string's length and the byte's position, then turns the result into capitals. What comes out is the client's own `G3D…` token (for example `G3D0311C`), which it then sends[^scramble]. The same kind of unscrambler hides other short strings in the 6.x clients, such as host names and ports, so that a simple text search of the program does not find them[^hidden].

That unscrambling is the only real "conversion" in the story, and it belongs to the older path, where the token is built into the client. The 6.11 path has no such step, because the token was never in the client to begin with.

## What this means if you want to change the token

If the server's script decides the token, could anyone make a stock client say something else by serving their own `conf.gs`? Not easily, and that is the point of the signature. A changed script no longer matches the signature, and making a new valid signature needs the server operator's secret key, which we do not have and would not expect to. A lab server that wants a stock 6.11 client to use a different token has two options. It can replay a genuine signed reply unchanged, which means the client says exactly what that reply says. Or it can modify a copy of the client so that it trusts a key the lab controls instead[^conseq].

## What this covers, and what it does not

This is a result for the **6.x desktop clients**: Mac 6.111 and Windows 6.113, the newest builds of the version-6 line we have. The replay used one captured reply, so strictly it shows what *that* reply says. Another server, or the same server on another day, could hand out a different script with a different token, and the client would send that instead.

It does **not** yet cover the version-7 "Worlds" builds. Those take a different login path, store no token either, and announce themselves to web servers as `Graal/6.76` or `Graal/6.77`. They have not been traced the same way, so nothing here should be read as a claim about them[^v7].

## Open points

- [ ] Trace a v7 "Worlds" build's login the same way, to see whether its token also comes from a server-supplied script.
- [ ] Check whether `GNP1905C` follows the old DDMMY date-stamp shape (it would read as 19 May 2012). Because the server chooses the value, that would say something about the script's author, not about the client **[inf]**.

## Notes

[^tokens]: [login-tokens-3x-7x.md](login-tokens-3x-7x.md), "The token itself"; [version-tokens.md](../client-internals/version-tokens.md).
[^cap]: [v6113-list-capture.md](v6113-list-capture.md) **[cap]**.
[^nostr]: [v6113-hello.md](v6113-hello.md), "The eight characters"; [v6037-hello-diff.md](v6037-hello-diff.md), "Login token" **[bin]**.
[^manual]: Manual §2.10.5, [manual/02-protocol/10-server-defined.md](../manual/02-protocol/10-server-defined.md).
[^conn]: [v6x-clients.md](v6x-clients.md), "6.11 Mac: the connector and a server-defined protocol" and "The connector request in a lab run" **[bin][cap]**.
[^layout]: Byte layout of one captured `conf.gs` reply, read in the 2026-11-11 Lion lab run (owner-held record). The reply itself, the request's `p=` value and the connector host are not published **[lab]**.
[^sig]: Same lab run; the 256-byte block verified as an RSA-2048 signature over the bare SHA-256 digest of the 4,890-byte payload, against the public signing key embedded in the 6.111 client, and the client verified it before running the script **[lab][bin]**.
[^script]: Decrypted connector script read from the 6.111 client's memory in the same lab run **[lab]**. The script methods themselves are listed in [v6x-clients.md](v6x-clients.md), "What the script controls" **[bin]**.
[^hdr]: [v6113-hello.md](v6113-hello.md), "The six bytes after the token"; manual §2.10.3 **[bin][cap]**.
[^lion]: Mac OS X 10.7.5 guest, unmodified Mac 6.11r1 (`Graal/6.111`), loopback lab responder serving a replayed reply, RAM dump after the script ran; 2026-11-11, owner-held record **[lab]**.
[^wintrace]: Debugger trace of the running Windows 6.113 client, 2026-11-11, owner-held record **[lab]**; agrees with the static reading in [unpacked-6113-wire.md](unpacked-6113-wire.md) **[bin]**.
[^scramble]: [v6037-hello-diff.md](v6037-hello-diff.md), "Login token"; [login-tokens-3x-7x.md](login-tokens-3x-7x.md), "The token itself" **[bin]**.
[^hidden]: [v6x-clients.md](v6x-clients.md), the build notes at the top **[bin]**.
[^conseq]: Follows from the signature check described above **[inf]**. No modified client was built for this note.
[^v7]: [v7x-protocol.md](v7x-protocol.md); [v7-graal3d-identity-and-builds.md](v7-graal3d-identity-and-builds.md).

## Bibliography

- Graal_analysis notes: `protocol/login-tokens-3x-7x.md`, `v6x-clients.md`, `v6113-hello.md`, `v6113-list-capture.md`, `v6037-hello-diff.md`, `unpacked-6113-wire.md`, `v7x-protocol.md`, `v7-graal3d-identity-and-builds.md`; `client-internals/version-tokens.md`; `manual/02-protocol/10-server-defined.md`.
- Owner-held lab records of 2026-11-11: the Lion replay of a captured `conf.gs` reply to Mac 6.111 with a memory dump, and a debugger trace of Windows 6.113. Not published; the plain-behaviour results are above.
- NIST FIPS 180-4, *Secure Hash Standard* (SHA-256).
- RFC 8017, *PKCS #1: RSA Cryptography Specifications Version 2.2*, section 9.2 (the `DigestInfo` encoding that Graal's signature leaves out).
