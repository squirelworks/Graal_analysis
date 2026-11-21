# Batch-2 Linux RC ladder (GSERV024 → GSERV025)

Date: 2026-11-16

Three already-unpacked Linux i386 Remote Control executables from the 2026-11-14 Batch-2 set were string-compared on a lab host. This note places them on the existing RC lineage without re-deriving packet tables. Tags: **[bin]** · **[inf]**. Evidence id: `BATCH2-RC-LINUX-20261116`.

Related: `protocol/rc-list-online.md`, `manual/07-rc-nc.md`, `tools/remotecontrol-lineage.md` (if present).

## Builds

| Title string | Login token | Notes |
|---|---|---|
| `Remote Control Linux 2005/01/24` | `GSERV024` | GTK staff client between the 2004 Delphi `GSERV024` set and RC2 2.05 |
| `Remote Control 2005/12/09` | `GSERV024` | Same token; larger image |
| `Remote Control 2006/01/20` | `GSERV025` | Token bump; still pre-RC2 2.05 (2006/12/20) in the lineage table |

All three are dynamically linked, stripped ELFs. The January 2005 build is the Linux GTK RC that `rc-list-online.md` already flagged as unpacked with receive-side ids elsewhere; Batch-2 is the tidy evidence pack (packed tarball + unpacked binary + checksums). **[bin]**

## What changes between the three

**2005/01/24 → 2005/12/09 (still `GSERV024`)**

- zlib symbols appear (`zlibVersion`, `zlibCompileFlags`).
- Script MIME type `text/x-graalscript`.
- UI copy `Ignore Mass PMs if client is on`.
- Extra editor / auto-indent / accounts-list surface in the string set. **[bin]**

**2005/12/09 → 2006/01/20 (`GSERV025`)**

- Token string becomes `GSERV025`.
- Ban-history and staff-activity related UI strings (`Ban History`, `getbanhistory`, `getstaffactivity`, `Edit Access`).
- `Allow Global PMs` / buddy-tracking prefs.
- Chat font-size preference.
- Compiler stamp `GCC: (GNU) 4.0.3 … (Debian 4.0.2-5)`. **[bin]**

This string-comparison pass did not read the three builds' outgoing call sites and therefore
 does not establish whether they send id 65 (`PLI_RC_LISTRCS`). A later
 [January 2005 framing read](rc2005-linux-send-framing-2026-11-21.md) supplies a bounded send-side
 result, but the complete outgoing-id census remains open; the other two builds do not inherit
 it from their tokens. **[bin][doc]**

## Seihai / suite feed

- Keep accepting `GSERV024` and `GSERV025` on the RC login path.
- Prefer the player-list empty-level rule for “admins online”, not id 65.
- Use the December 2005 / January 2006 builds when testing script-editor MIME and mass-PM ignore options; the January 2005 Linux build is the thinner baseline.

No addresses, decompile dumps or private pack paths are published here.
