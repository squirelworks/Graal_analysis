# Who stores baddies and chests in three 2.1 images

Date: 2026-11-15. Static read of the level-file reader in the public 2.1.0.0 image, in Graal 2002 ver7, and in Graal 2002 v22. Nothing was run. ver8, ver9, ver10 and ver13 were not read. No packet was read.

The record shapes are the ones already in the manual: a baddy is three raw bytes and a `\`-separated tail, and it stops when the line is shorter than three bytes or the first byte is at least 128; a chest is four byte-minus-32 values. This note is only which of these three images stores them.

| Image | Baddy records | Chest records |
| --- | --- | --- |
| public 2.1.0.0 | stored for every line that passes the length and first-byte tests. No flag test in that loop | stored for `GR-V1.01`, `GR-V1.02` and `GR-V1.03`. No flag test in that loop |
| v22 | the same lines are stored only when two flag bytes are both clear. Either flag set skips the store and still consumes the line | the same four-field records, under the same two flags |
| ver7 | the scan consumes the lines and does not construct a record | the scan consumes the lines and does not construct a record |

**[bin]**

The chest loop is reached from the `GR-V1.01`, `GR-V1.02` and `GR-V1.03` tests. A condition flag left by the previous section was not separated from those tests, so this note does not say that `GR-V1.00` skips chests. The two v22 flag bytes were not identified. **[bin]**

## Open

- [ ] Name the two v22 flag bytes.
- [ ] Separate the `GR-V1.00` chest test from the flag the previous section leaves.
- [ ] Read the same loops in ver8, ver9, ver10 and ver13.
