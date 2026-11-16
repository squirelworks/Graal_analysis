# Android Classic chat and dispatch versus desktop 6.x

Date: 2026-11-16. Comparison from held notes only: the Android Classic 1.8 engine reading (`VX-ANDROID-20261109`) against published desktop chat and 6.x dispatch notes. No new binary open and no mobile capture. Evidence `ANDROID-PROTO-VS6X-20261116`. **[bin][doc]**

## Android side (held)

From [client-internals/android-classic.md](../client-internals/android-classic.md#global-chat):

- Outgoing chat uses a **reconfigurable** handler table. On the ordinary route the text is cut to **220 stored bytes**, a one-byte prefix equal to `stored_length + 32` is written, the text follows, and the result goes to the transport. A special route raises a local event; a disabled route sends nothing. The prefix is **not** a fixed message id. The limit is bytes, not characters. **[bin]**
- Incoming messages index a **256-entry** handler table by an unsigned command byte. Some handlers run at once and others are queued. Which command maps to which handler, and the outer framing / compression / encryption, were not recovered in that reading. **[bin]**

## Desktop 6.x / classic side (published)

- Local chat on the classic/2.x server path is **not** a free-standing message id: it is `PLPROP_CURCHAT` (12) inside `PLI_PLAYERPROPS`, with `toall:` as the exception that becomes `PLI_TOALL` (6) (max 200 bytes on 2.05). **[doc]** ([chat-pm-rc.md](chat-pm-rc.md))
- Unpacked 6.1.1.3 delivers another player's line as the script event `onToall` on the TCP path; a fixed PLO number for that chat line was not found in the image. **[bin]** ([v6113-chat.md](v6113-chat.md))
- Gen-5 style packets elsewhere in the desktop line commonly use `id + 32` bodies and length-prefixed strings as `count + 32` ([v4x-clients.md](v4x-clients.md), classic login notes). That is the same **offset-32** length-prefix family the Android chat builder uses for its text field, not proof that Android chat is `PLPROP_CURCHAT` or any named PLI. **[doc][inf]**

## What matches and what does not

| Topic | Android Classic (held) | Desktop 6.x / classic (published) | Claim |
| --- | --- | --- | --- |
| Outgoing player chat shape | `len+32` + up to 220 bytes; reconfigurable route; prefix not a fixed id | Local chat usually inside player props; toall is its own id | **Different object model**; shared only the offset-32 string length habit |
| Inbound dispatch | 256 slots by unsigned command byte; immediate vs queued | Script/native handler tables; 6.1.1.3 chat id not fixed in image | **Same table width family**; Android command map unread |
| Chat byte caps | 220 stored bytes on the ordinary Android route | 2.05 toall max 200 bytes; CURCHAT not re-stated here as 220 | Do not equate the caps without a capture |
| Version token in login | Unread ([boundary](../client-internals/android-login-token-boundary.md)) | Desktop tokens catalogued separately | No transfer |

## Mobile-only / unread

- Whether any inbound command bytes are Android-only (touch, store, or host events) is **unread**: the table exists, the filled slots were not listed. **[bin]**
- Outer framing around the Android transport (length words, compression, encryption generation) is **unread** in the held study. Desktop gen-5 framing must not be assumed. **[bin][inf]**
- iOS Classic+ login helpers also use a `length + 32` one-byte prefix on a short path ([classic-113-login-construction.md](../client-internals/classic-113-login-construction.md)). That is a framing resemblance for login fields on iOS, not an Android token and not a chat id. **[bin]**

## Use

Servers and clients that already speak classic `PLPROP_CURCHAT` / `PLI_TOALL` cannot treat the Android ordinary chat builder as the same packet without a connect reading. The next static or EmulatorHelper pass should recover the inbound command map and the login/token construction; this note only bounds what the held chat/dispatch facts already imply versus 6.x.
