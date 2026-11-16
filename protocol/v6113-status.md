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

A classic Gen5 server that answers only `G3D…` login does not speak this stream after the hello. **[cap][inf]** (`v6113-list-capture.md`)

## 6.037 is not 6.113

Same late-Windows shell family (Themida / WinLicense packed `OG_Graal`-style
stubs), different cores. **[bin]** (`packed-6037.md`, `packed-6113.md`,
`themida-pack.md`, `v6037-hello-diff.md`)

| | Windows 6.037 | Windows 6.113 |
| --- | --- | --- |
| Login identity | Compiled-in Gen5 token `G3D0311C` (stored scrambled, sent as id 5) | Connector script supplies `GNP1905C` via `sendRaw` |
| First hop | Game connect to a compiled-in Login host (`HOST:PORT` lab form; no `conf.gs`) | Signed `conf.gs` connector reply, then script-driven connect |
| On-disk license file | None (hosts compiled in), same as other late 6.0x | None; connector host path, not `license.graal` |
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
   `connector-script.md` Open. **[lab]**
3. **Open: live `conf.gs` harness.** A loopback connector responder plus a
   stock (or lab-redirected) 6.113 past the clear hello, with first encrypted
   frames captured against a lab game sink. Existing Mac 6.111 offline replay
   and Windows live memory reads already settle the cipher story; they do not
   replace a Windows 6.113 loopback harness note. Do not wait on that harness
   to keep the settled table above. **[lab]**
4. **Clean fully-unpacked 6.113 image vs the existing unpacked-6113 notes.**
   Packed game exe remains a Themida shell in the stock listing; a lab unpack
   dump (private) may sharpen leftovers, but must not put digests, paths or
   decompile text on git. Method only until a dump exists. **[bin]**
5. **First Login / play replies a 6.113 client needs after decrypt** compared
   with 6.037 — still the open half of #510. Needs the harness in (3). **[lab]**
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
