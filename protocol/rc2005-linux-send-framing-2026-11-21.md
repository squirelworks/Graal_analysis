# January 2005 Linux RC: outgoing framing scope

Date: 2026-11-22; static review began 2026-11-21. Retained disassembly and bounded ELF data for the
32-bit Linux Remote Control titled 2005/01/24. Evidence
`RC2005-SEND-STATIC-20261121` ([index](../docs/evidence-index.tsv)).
No original process, provider, network connection or lab experiment was run. **[bin]**

The input is the January build already distinguished from its December 2005 and
January 2006 siblings in the [Batch-2 study](batch2-rc-linux-2005-2006.md).
Matching login tokens do not transfer these findings to those siblings. This pass
does not establish pristine-vendor provenance or runtime interoperability. **[bin]**

## Enqueue and initial RC message

The shared enqueue routine appends the encoded message id, the supplied body and a
line feed. A one-time flag inserts the login-key field immediately after the id,
then clears itself. For nonnegative time values, the key value is time modulo 128;
its encoded wire byte is that value plus 32. The seven-bit value is not a claim
that the encoded byte itself has only seven bits or that it is fresh randomness.
The plaintext queue requests a flush when its size exceeds 4095 bytes. **[bin]**

The RC setup names its connection `gserver`, arms that one-time flag and directly
calls the outgoing wrapper with login type 6. Its constructed body is
`GSERV024`, followed by the length-prefixed account and password fields, in that
order. The field sources are the account and password controls. This establishes
the construction and direct enqueue path, not successful authentication. **[bin]**

The NC setup separately constructs type 3 with `NCL11012` and the same field
pair. Its setup does not arm the RC key-insertion helper. Construction is not a
new observation of NC transmission: the complete indirect per-socket call routing
remains outside this result. **[bin]**

## Flush selection and cipher stepping

The connection begins in fixed zlib mode 3. That initial path writes a big-endian
two-byte compressed-body length, with no dynamic type byte and no XOR pass.
After the initial flush, the state change is conditional on the connection name:
`gserver` changes to dynamic selection; `npcserver` retains fixed mode. This
is a code-path distinction, not a demonstrated login or NC session. **[bin]**

In dynamic mode the nominal plaintext-size policy is:

- Above 4095 bytes, select the bz2 path.
- From 48 through 4095 bytes, select the zlib path.
- At most 47 bytes, try zlib and use it only if the result is smaller; otherwise
  use raw data.

The dynamic frame has a big-endian two-byte length that includes its type byte:
2 for raw, 4 for zlib or 6 for bz2. The selected frame body must pass a size guard
of 1 through 65534 bytes. Raw-body copying is bounded by a global copy cap before
the plaintext queue is cleared. The nominal selection policy therefore does not
guarantee arbitrary-size or complete plaintext-queue delivery. Compression-helper
failure and peer acceptance were not tested here. **[bin]**

The outgoing cipher state is distinct from the receive state. For a dynamic raw
body, the XOR loop advances once per four-byte group present, including a partial
last group, capped at twelve groups. For dynamic compressed bodies it advances
once per **complete** four-byte group, capped at four; a trailing partial group
is not processed by that loop. These are independently read send-side branches,
not an assumption of receive/send symmetry. **[bin]**

Framed bytes enter a separate buffered socket-send queue. A short positive socket
write removes only the written prefix and retains the remainder. Neither this
branch read nor the frame construction is a runtime delivery result. **[bin]**

## Upload override

The outgoing override treats message 93 separately. Its nominal declared length
is body size plus the message-id byte and final line feed, capped by the override's
length limit before id-50 encoding. It then forwards message 93 to the shared
enqueue routine. Other bodies containing a line
feed take a diagnostic/rejection path. This identifies the override's construction;
the full indirect dispatch and per-socket message census remain unproven. **[bin]**

## Limits and G301

Some call sites use indirect callback dispatch. The adjacent receive/send pointers
in retained data are not enough to resolve every caller's routing, and this pass
does not claim a complete constant or computed outgoing-id set. In particular it
does **not** establish that this build never sends id 65. The
[online-RC-list note](rc-list-online.md) and Batch-2 string comparison must retain
that distinction. The already documented receive cases do not supply missing
send behavior. **[bin][doc]**

- [x] Read the shared enqueue, initial RC construction and flush/cipher branches
  from the retained January 2005 input.
- [ ] Complete indirect per-socket outgoing-call routing and the constant/computed
  id census before making a whole-build id-65 absence claim.
- [ ] Validate the resulting normal RC/NC wire behavior separately; no runtime
  acceptance is supplied by this static pass.
