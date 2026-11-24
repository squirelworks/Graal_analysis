# 6.1.1.3 / `GNP1905C` connector path — status

Date: 2026-11-16.

Status hub for research-list side track **#44** / assigned lead **6.1.1.3
cipher** / issues [#397](https://github.com/squirelworks/Graal_analysis/issues/397)
and [#510](https://github.com/squirelworks/Graal_analysis/issues/510). This note
does not re-prove the cipher path. It states what our own notes already settle,
and where not to re-open work.

Tags: **[bin]** · **[lab]** · **[cap]** · **[inf]** where marked. Own words only.
Third-party REA corpora are leads, not proof, and are not copied here.

## Settled (do not re-chase as primary work)

| Topic | Status | Where |
| --- | --- | --- |
| Clear hello `GNP1905C` | Settled **[cap][bin]** | Script `sendRaw` literal; not a compiled-in client string. `v6113-hello.md`, `v6-login-token-explained.md` |
| Outgoing post-hello cipher | Settled **[lab][cap]** | Clear prefix ends at stream offset **287**; then plain RC4, 16-byte session key, headers encrypted. `v611-outgoing-cipher.md`, `connector-script.md` §4 |
| Server→client key | Settled **[lab]** | Server clear `0xfc` RSA-wrapped; client unwraps with the RSA private key from `setEncryptionParseKey`. No `setEncryptionIn` on the login path. `connector-script.md` §4c |
| `EILLLT` framing | Settled **[lab][cap]** | Outer `0xfd` / inner `0xfc` for the key exchange; then ciphered `EILLLT` bundles. Same notes |
| Connector fetch shape | Settled **[bin][cap][lab]** | HTTPS to the connector host first, then plain HTTP `conf.gs?p=…`; fail → `StartScript_Fail` / connect error. `connector-script.md` §1–§6, `v6x-clients.md` |
| GRESCR01 + PLO 197 (held corpus) | Settled for structure **[cap]** | Bit-reversed DES; per-script session keys on the wire; **19** official bodies: four-segment container, counts only. Keys and bodies stay off git. `gs2-official-bytecode-6113.md` |
| Prop parse path on 6.113 | Settled **[bin]** | Script methods `tclient_setplayerprops` / `tclient_setotherplayerprops` / `tclient_setnpcprops` / `tclient_setbaddyprops` feed the same native parsers 6.037 calls from its packet switch. Field-byte diffs between the two images were not compared. `v5-props.md`, `v6037-hello-diff.md` |
| Prop wire → slot join | Settled **[lab][bin]** | Live Mac new-protocol map: wire 9→slot 1 `setplayerprops`; wires 2/3/8→unnamed prop slots. Joined note: `v6113-receive-handlers-props.md` |
| Live Windows connector still served (2026-11-16) | Settled **[lab]** | Stock 6.113 writes `GRESCR01` `StartScript_Connector` before Login UI; Login chrome then downloads. `v6113-live-connector-2026-11-16.md` |
| Live Windows `HOST:14900` handshake reconfirm (2026-11-16) | Settled **[cap]** | Official 6.113 again: clear `GNP1905C` + zlib `EILLLT`/`0xfd` (`LLL=279`), RC4 from offset **287**, three answered sessions + one unanswered SYN; stayed on `HOST:14900` after Login; no keys. `v6113-live-handshake-2026-11-16.md` |

A classic Gen5 server that answers only `G3D…` login does not speak this stream after the hello. **[cap][inf]** (`v6113-list-capture.md`)

## 6.037 is not 6.113

Same late-Windows shell family (Themida / WinLicense packed `OG_Graal`-style
stubs), different cores. **[bin]** (`packed-6037.md`, `packed-6113.md`,
`themida-pack.md`, `v6037-hello-diff.md`)

| | Windows 6.037 | Windows 6.113 |
| --- | --- | --- |
| Login identity | Compiled-in Gen5 token `G3D0311C` (stored scrambled, sent as id 5) | Connector script supplies `GNP1905C` via `sendRaw` |
| First hop | Game connect to a compiled-in Login host (`HOST:PORT` lab form; no `conf.gs`) | Signed `conf.gs` connector reply, then script-driven connect |
| On-disk license file | None (hosts compiled in), same as other late 6.0x | Not universal: one lab tree has an 8-line host/port list; connector `conf.gs` still gates Login (`v6113-live-connector-2026-11-16.md`) |
| After hello | Classic Gen5 framing / cipher | Clear token + one clear key frame, then RC4 from offset 287 |
| Prop intake | Native packet switch → parsers | Script `tclient_set*props` → same native parsers |

Do not treat a working 6.037 Gen5 lab stack as a fidelity stand-in for 6.113.
**[bin][inf]**

## Still open

1. **Login-step argument order after the cipher.** Names on 6.113 are known
   (`connectToGameServer`, `setLoginAccount`, `getPassword`,
   `sendLoginNewProtocol` / `sendPasswordAndIDs`); bytecode argument order is
   not. `connector-script.md` Open. **[lab]**
2. **What `?p=` binds** beyond “this launch’s request” for the signature.
   Sharpened: the `?p=` request is **byte-identical across fresh launches**
   of a build (no per-launch nonce; it encodes only game/platform/version/
   build), so for 6.113 the request binds nothing per launch — any per-launch
   binding, if it exists, is inside the decrypted script, not the request.
   `v6113-login-lab-method.md`, `connector-script.md` Open. **[lab]**
3. **Loopback `conf.gs` harness (G248) — answered 2026-11-24.** Live Windows
   6.113 still fetches a connector and reaches Login UI
   (`v6113-live-connector-2026-11-16.md`). Official post-Login traffic on
   `HOST:14900` reconfirms the clear hello and RC4-from-287 cut without keys
   (`v6113-live-handshake-2026-11-16.md`). The loopback responder + mutator
   harness is in `../tools/connfuzz/` (`conf-gs-fuzzing.md`): **Phase A**
   container fuzz against stock 6.113 fails closed on every one-field mutation
   (no crash/hang/accept). **Phase B** / first encrypted frames on a
   lab-signed stock path are **blocked** — trust-anchor swap is a NO-GO on the
   packed client (`v6113-login-lab-2026-11-19.md`, `conf-gs-fuzzing.md`), and
   session-key recovery is stopped. Mac 6.111 offline replay and the clean-room
   repro already settle the cipher story for lab work; do not wait on a stock
   accept. Two-gate order (classic login/list, then signed connector) remains
   as previously measured. **[lab]**
4. **Clean fully-unpacked 6.113 image vs the existing unpacked-6113 notes.**
   Packed game exe remains a Themida shell in the stock listing; a lab unpack
   dump (private) may sharpen leftovers, but must not put digests, paths or
   decompile text on git. Method only until a dump exists. **[bin]**
5. **First Login / play replies a 6.113 client needs after decrypt** compared
   with 6.037 — still the open half of #510. Needs an accepted connector
   script (genuine reply or clean-room repro); stock lab-signed path is
   blocked per (3). **[lab]**
6. **7.x script delta** (token / template / cipher vs 6.11) — needs a 7.x
   reply decrypted for its own launch. `connector-script.md` Open. **[lab]**

## Implications for labs and Seihai

- A lab that serves only Gen5 `G3D0311C` will see `GNP1905C` and then ciphertext
  it cannot read without the connector key material. **[cap][inf]**
- A lab that replays a genuine signed `conf.gs` can drive the stock hello and
  key frames; it still cannot decrypt a stock client’s post-287 stream without
  the operator private key that matches the script’s public wrap key.
  `connector-script.md` §4c. **[lab][inf]**
- gcr `graal-6.1.1.3-GNP1905C` stopping at the clear hello without a lab
  connector path is expected, not a Gen5 framing bug. **[inf]**
- Keep GRESCR keys, cache bodies, `?p=` blobs and connector hosts out of the
  repository. Counts and structure only (`gs2-official-bytecode-6113.md`).

## Non-goals here

- Re-deriving bit-reversed DES or publishing key tables.
- Copying third-party GLauncher decomp or Others-work NOTES into this repo.
- Public-server captures (needs a separate owner OK).
- Competing with gameplay track work for lab capacity.
