# PLO 109 — HTTP(S) file download (`PLO_HTTPDOWNLOAD`)

Date: 2026-11-16

Server → client id **109** tells the client to fetch a file over HTTP(S)
and store it under a local name with a given modification time. It is a
**file redirect**, not an in-band file body (contrast `PLO_FILE` / large-file
ids).

Tags: **[bin]** · **[inf]** for the 6.11 native name fit. Earlier write-up:
`unknown-ids-2026-11-06.md` §PLO 109; receive-set notes in `v6x-clients.md`.

## Layout

| Field | Wire | Role |
|---|---|---|
| mod time | `i5` (five 7-bit groups) | Stored with the download |
| A | `c`-length string | Local name the file is stored under (or redirected from) |
| B | `c`-length string | URL fetched over HTTP(S) |

**[bin]** (6.03r7 reader): B is parsed as an `http://` or `https://` URL
(host and path). The client finds or creates an HTTP connection object
named from host/port/path, starts the fetch, marks the download, stores A
and the time, and tells the file manager.

GServer layouts that omit the local-name string are **one string short**
of what the stock client reads. **[bin]** (`packet-ids.md`,
`unknown-ids-2026-11-06.md`).

## Name

| Label | Role |
|---|---|
| `PLO_HTTPDOWNLOAD` | Preferred (gs2lib / Seihai suite since 2026-11-11) |
| `PLO_DOWNLOADURL` | Seihai name until 2026-11-11; still fine as a gloss |
| Native (6.11) | Fits `setfileredirect(u,s,s)` **[inf]** |

## Who handles it **[bin]**

| Build | 109 |
|---|---|
| **5.24r4 → 6.03r7** (incl. 6.01) | Handled (time + two strings → file layer) |
| **5.12 and older**, **4.x** | No receive case |
| **1.39–2.310** | No receive case |

Others Work scoped the lead as “v6 only.” That matches the builds they
opened; our chain is **wider**: first handler at **5.24r4**, not only 6.x.
Do not send 109 to a profile whose `plo` set omits it (same rule as other
late ids).

## Others Work / Bible fold — first-string scheme check (B5)

**Claim (lead only):** before the download starts, the **first** string is
checked for a URL scheme (`://` or an encoded form).

| Piece | Our stance |
|---|---|
| B is the URL and is scheme-parsed (`http` / `https`) | **Confirmed** **[bin]** |
| A is the local / redirect name | **Preferred reading** **[bin]** (high layout; medium on A’s exact file-manager role) |
| A is *also* scheme-checked as if it were a URL | **Unconfirmed.** Could be true on some builds without contradicting “A = local name”; not yet separated from B’s scheme parse in our notes. |

Do **not** flip A and B on the wire to chase the lead. Re-read stock
5.24r4 / 6.03r7 if a lab needs the scheme check pinned to A vs B.

## Confidence

| Claim | Level |
|---|---|
| Layout `i5` + two strings | high |
| B fetched over HTTP(S) | high |
| Handled 5.24r4–6.03r7; not 5.12/4.x | high |
| Exact file-manager role of A | medium |
| First-string scheme-check (Others Work B5) | open / lead |

## Open (stock re-read / loopback — not Share)

1. Pin whether any scheme check runs on **A**, on **B**, or both (B5).
2. Loopback **L**: send 109 with a lab HTTP responder; confirm store-as-A
   and mod-time behaviour on 5.24r4 and 6.03r7.
3. Whether transitional 5.24 builds match 6.03r7’s HTTP object naming.

## Implications for Seihai

- Keep the id named **`PLO_HTTPDOWNLOAD`**.
- Layout when sending: `GINT5` mod time, local name, URL (both strings).
- **Profile-gate:** only to builds that list 109 (5.24r4+ / v6 in our
  tables). Never to 4.x or 5.12.
- Still optional on this path until a feature needs file redirects.
