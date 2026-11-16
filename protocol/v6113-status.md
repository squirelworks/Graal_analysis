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
