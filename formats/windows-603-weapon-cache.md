# Windows 6.03 candidate: GRESCR01 header is not cache acceptance

9 November 2026. Evidence W603-CACHE-GATE-20261109. New static review of the unpacked Windows input with SHA-256 `2be6bf4bc7811bec48c6f03643e96d8e7e41e22b582860bb3bd7ab152fe11c6d`. The completed recovery has 7,607 decompiled functions and three failures. An unpacked analysis image is not automatically an original runnable distribution. No new client execution occurred in this review.

## What the inspected reader and weapon caller do

The cache reader clears its success output first. A missing key argument or a cache flag other than 1 returns an empty value immediately. It then obtains the file data, requires at least eight bytes and checks the eight-byte `GRESCR01` magic. Passing those preliminary checks does not by itself set success.

The reader removes the magic and works on the remaining stored body. If the expected CRC is nonzero, it computes CRC32 over that stored body and sets the success output from the comparison. A mismatch returns empty. This check precedes the block transformation. If the expected CRC is zero, the reader skips the comparison, can still transform/return the body, and leaves success false. Returned bytes and accepted-cache status are separate outputs.

The inspected caller constructs a weapon cache pathname under the weapon-cache directory with the `.code` extension, calls this reader, and branches on that success output. On false it dispatches script request logical ID 158 through its connection method. On true it hands the returned script bytes onward. The complete outgoing framer and every other caller were not retraced here.

## Exactly eight bytes

For the synthetic file consisting only of ASCII `GRESCR01`, the body is empty. The recovered CRC implementation returns the incoming CRC unchanged on zero bytes; its initialization path supplies zero. Therefore the empty body's CRC is zero.

- Expected CRC zero: comparison is skipped and success stays false.
- Expected CRC nonzero: comparison against zero fails and success stays false.

Thus, under the inspected weapon cache caller, a header-only file does not become an accepted cached script. With the remaining gates permitting the call, it follows the script-request path. This is a static-derived result, not a captured cache read. It does not establish all possible direct uses of the lower-level reader, class-cache behaviour or subsequent VM semantics.

## Independently testable cases

The eight-byte vector is `47 52 45 53 43 52 30 31`. With cache flag 1 and a present key, test expected CRC 0 and then 1. Both have false cache success at this helper/caller boundary. Separately test flag 2 and a missing key as early-gate cases. A valid-looking header alone must never count as GS2 execution.

These cases do not require an official script payload. A reproduction may retain a standalone magic/header recognizer, but label its result as header recognition rather than target-compatible script/cache acceptance. Full acceptance still requires file/context validity, checksum/key handling, decoded-container validation and whatever execution state the selected build requires.

## Publication and scope

This narrows the prior Windows 6.03 header-only unknown for the inspected weapon path. It also establishes checksum-before-transformation for this exact input, rather than importing a Linux/6.113 claim or selecting between conflicting older prose. The script-request result is conditional on this caller's surrounding enablement gates. No class/all-build generalization, visible scene, login or script execution is claimed.

Ten retained source digests were verified and matching assembly was retained privately, including CRC argument setup, substring/empty-body handling and the success-output branch. The original compiler's calling conventions were not faithfully expressed by every decompiler prototype; the critical zero-length/checksum decisions were checked against instructions.


## Evidence and fixture status

[bin] Evidence W603-CACHE-GATE-20261109 identifies the owner-held static record. Its researcher-supplied SHA-256 is `47564eea573d99d4653f7930760ed93525544a3f9a626b5f21052983198379b8`. The publishing preparation checks the sanitized handoff and fixture digests; it does not independently authenticate the historical distribution or turn retained instructions into a new runtime experiment. Server and server commit: none; no new client/server run was performed.

[inf] The adjacent [cache fixture contract](windows-603-cache-conformance.static-derived.json) is independently authored. Every expected result is explicitly **static-derived**, and original-client execution is false. It is a receiver/helper boundary contract, not a capture or complete VM acceptance test.
