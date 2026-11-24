# Gen-6 server→client `0xfc` padding (closed)

Date: 2026-11-16. Tags: **[cap]** / **[lab]** for held stock server→client key blocks; **[inf]** where client→server remains operator-key-bound.

Leads-only. **No keys, no block bytes, no hosts or paths** in this note. Extends [`v611-outgoing-cipher.md`](v611-outgoing-cipher.md) and the connector-script §4c layout.

## Already settled (prior lab)

- Clear outer `0xfd` wraps an inner `0xfc` with a **256-byte** high-entropy body (one RSA-2048 block), then the encrypted stream. EILLLT framing. **[lab][cap]**
- After raw decrypt, plaintext fields are: cipher type, then length-prefixed key, then length-prefixed IV, with Graal **value+32** length bytes. Observed stock sessions use type **1** (RC4), key length **16**, IV length **16**. **[lab]**
- AES (type **2**) was not chosen on the stock connector paths held here. **[lab][cap]**

## Padding closed (server→client)

Raw RSA decrypt of held stock **server→client** `0xfc` bodies (multiple 6.113-era session dumps) yields an encryption-block encoding that starts with **`00 02`**, then a nonzero padding string, then a **`00`** separator, then the cipher-type / key / IV payload above. That is **PKCS#1 v1.5 type-2** (encryption) padding. **[cap][lab]**

| Block class | EM starts `00 02`? | Nonzero PS + `00` sep? | Payload shape (no secrets) |
| --- | --- | --- | --- |
| Stock server→client (held sessions) | **yes** | **yes** | type **1**, keylen **16**, ivlen **16** |
| Stock client→server vs the client parse key | no (garbage) | n/a | Expected: wrapped to the **operator** public key, not the parse key |

So: **server→client** padding is closed as PKCS#1 v1.5 type-2. **Client→server**
still needs the operator private key (unheld here). **G335** (2026-11-24) closes
that board item as an **honest partial**: C→S envelope settled; EM padding still
blocked. See [`gen6-c2s-0xfc-padding.md`](gen6-c2s-0xfc-padding.md). **[cap][lab][inf]**

Connector **signatures** (a different object) use PKCS#1 v1.5 **type 1** over a bare digest — same family name, not the session-key encrypt padding. **[bin][lab]**

## Still open

- Exact client→server encoding-message padding once an operator private key is available in lab (never publish the key) — tracked under G335 partial. **[lab]**
- Whether any stock connector path ever selects AES type 2. **[lab]**
