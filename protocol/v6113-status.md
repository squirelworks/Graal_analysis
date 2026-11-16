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
