# Who stores baddies and chests in three 2.1 images

Date: 2026-11-15. Static read of the level-file reader in the public 2.1.0.0 image, in Graal 2002 ver7, and in Graal 2002 v22. Nothing was run. A follow-up read compared the selected binary record loops in ver8, ver9, ver10 and ver13. No packet was read.

The record shapes are the ones already in the manual: a baddy is three raw bytes and a `\`-separated tail, and it stops when the line is shorter than three bytes or the first byte is at least 128; a chest is four byte-minus-32 values. This note is only which of the examined images store them.

| Image | Baddy records | Chest records |
| --- | --- | --- |
| public 2.1.0.0 | stored for every line that passes the length and first-byte tests. No flag test in that loop | stored for `GR-V1.01`, `GR-V1.02` and `GR-V1.03`. No flag test in that loop |
| v22 | the same lines are stored only when two flag bytes are both clear. Either flag set skips the store and still consumes the line | the same four-field records, under the same two flags |
| ver7 | the scan consumes the lines and does not construct a record | the scan consumes the lines and does not construct a record |

**[bin]**

Receipt. The images read were the public 2.1.0.0 image, Graal 2002 ver7, and Graal 2002 v22. On v22 the two store guards are two flag bytes, both clear, identified in the follow-up below. ver7 consumes the lines and does not construct records. This is a file reader. It is not network acceptance. **[bin]**

The earlier section also accepts `GR-V1.00`. A fresh comparison against `GR-V1.01`–`GR-V1.03` gates the chest section in all three selected readers, so `GR-V1.00` skips it. The v22 storage flags are checked after entry to that section. **[bin]**

In the examined ver8, ver9, ver10 and ver13 images, the normal binary reader advances through baddy lines of at least three bytes whose first byte is below 128 without constructing or inserting baddy records. For `GR-V1.01`–`GR-V1.03`, it reads chest lines until an empty line or `#` without constructing or inserting chest records. Both loops match the selected ver7 reader. This follow-up does not cover the `GR-V1.00` path in those four builds, NW files or runtime behavior. **[bin]**

## v22 storage modes

In the examined v22 reader, the two bytes are the Kingdoms and New World mode flags. The dispatch table leads to separate handlers that set the respective bytes. The baddy and chest loops test those same bytes before storing records. With either flag set, the reader consumes the lines without storing those records. This is a static result for the selected binary reader. **[bin]**

## Open

- [x] Name the two v22 flag bytes. See the storage-mode comparison above.
- [x] Separate the `GR-V1.00` chest test from the flag the previous section leaves. See the selected-reader comparison above.
- [x] Read the same loops in ver8, ver9, ver10 and ver13. See the follow-up comparison above.
