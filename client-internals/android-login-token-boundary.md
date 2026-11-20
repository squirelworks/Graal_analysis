# Android Classic/Era login and version-token boundary

Date: 2026-11-16. Derived from the held Android package study (`VX-ANDROID-20261109`) and the published host/engine note. No new binary open, no device, emulator or wire capture. Evidence `ANDROID-LOGIN-BOUNDARY-20261116`. **[bin][inf]**

## Scope

The [Android Classic/Era static reading](android-classic.md) covered the Java host, frame gate, collision, board, render, chat builder and Classic 1.8 GS2 machine across seven packages (Classic 1.6–2.2 and Era 1.7/2.0). It did **not** recover a game-login frame or a version-token construction. **[bin]**

The native engine libraries in those packages are **not** encrypted. Connect and token builders are therefore in scope for a later static or headless-emulator pass; their absence from the catalogue today means **unread**, not proven absent. **[bin][inf]**

## What is settled without a token value

- Package identity is by in-package version and build number (6108–6201), not by store file names. **[file]**
- The Java host loads the native engine, passes language, APK/data/storage paths, display metrics and any start-up link, then drives the native frame entry. That path is the host side of a session, not a recovered login packet. **[bin]**
- Outgoing global chat on the ordinary route uses a one-byte `stored_length + 32` prefix and a 220-byte text cap ([android-classic.md](android-classic.md#global-chat)). That framing belongs to the chat builder, not to a recovered version token. **[bin]**

## What remains open

- The exact game-login / version-token bytes (or a documented no-token family) for each of the seven packages. Catalogue grade stays **U**. **[inf]**
- Whether Android uses the same eight-character `G3D…` stamp family as the inspected iPhone apps, a different alphabet, or no on-wire token. No iOS or desktop value may be transferred. **[inf]**
- ~~Outer transport framing, compression and encryption around login and the 256-entry inbound command table ([protocol note](../protocol/android-classic-protocol-vs-6x.md)). **[bin]**~~ Read for Classic 1.8 on 2026-11-20 ([static read](static-reads-appendix-e-2026-11-20-l.md)): the 6.11 connection class, with generation-5 framing by default and the key byte after the first message's id. The login id and token come from the connector script.

## Catalogue use

Until a connect-routine or EmulatorHelper reading supplies a concrete token (or a documented `-` no-token family), keep the Android row as unresolved with source pointing here and at [android-classic.md](android-classic.md#what-was-read). Regenerating `VERSION-TOKENS.md` from the catalogue preserves that **U**.
