# Static reads for Appendix E, twelfth batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (a decompiler read of the Windows 2.22 input A on the lab host A
lab, a linear disassembly of the same file, and a full byte comparison of A, B and the community
control; no client run) and **[test]** (a check of the held `.sig` files against the decoded key).
Only behaviour is given here. Covers App. E#103.

Inputs: A, the original Windows 2.22 `Graal2220.exe` (token `GNW03014`); B, the four-byte variant of
[windows-222-verifier-variants.md](../formats/windows-222-verifier-variants.md); and the control,
the Graal Reborn `Graal_222.exe` with its `graal.sig`, `arrays2.sig` and `arrays2.dat`.

## How the three inputs relate

A full byte comparison of A and the control gives 34 bytes in eight ranges:

| Range | In A | In the control |
| --- | --- | --- |
| 1 to 4 | four conditional branches in the verify routine (key size, signature size, helper result, final comparison) | the same four as unconditional jumps |
| 5 | `Graal Gold` | `Gold` |
| 6 | `Classic` | `Silver` |
| 7 | `Hosted` | `Bronze` |
| 8 | `Graal2002` | `Graal Reborn` |

The four guard bytes are exactly the A-to-B difference. So **B is A with only the verify guards
patched, and the control is B with four labels renamed**. That accounts for the earlier counts: 34
bytes from A to the control, and 30 bytes in four ranges (the renames) from B to the control.

The control therefore has **four** patched branches, not three as
[arrays-and-signatures.md](../formats/arrays-and-signatures.md#the-graal-reborn-222-exe-has-the-check-disabled)
said. The two notes describe the same patch.

## Where the check runs

At start-up, the main form's RSA component (SHA-1 signing digest, PKCS#1 scheme) is given its key
from the obfuscated string. Then, for each pair in turn, the signature file is loaded, the data file
is loaded, and the verify routine runs: `graal.sig` against the executable itself, then
`arrays2.sig` against `arrays2.dat`. Any failure raises an error, and the "corrupted" message
follows. So the patched routine is the one reached at start-up, for both files.

## The verify routine (A)

1. If the key is shorter than 89 bits, it fails ("key too short" for the PKCS#1 scheme).
2. If the signature length is not (key bits + 7) / 8 bytes, it fails.
3. It computes m = s^e mod n and writes m as (key bits − 1) / 8 bytes.
4. A helper builds the expected block: `01`, then `FF` bytes, then `00`, then the 20-byte SHA-1 of
   the data, (key bits − 1) / 8 bytes in all. There is **no DigestInfo** prefix, so this is not
   standard PKCS#1 v1.5. The helper always reports success, so the third guard can never fire even
   in A.
5. The two blocks are compared. A mismatch fails.

With all four guards jumped, every failure path is skipped and the routine always passes. So B and
the control accept any executable and any `arrays2.dat`, with any signature file.

## The key

The key text is built one character at a time: 1,024 hex characters. Decoding them as hex in
reversed byte order, then `not(b) − 10` on each byte, gives 512 ASCII hex characters. Read as one
number, that is a **2,047-bit** modulus. Under step 2, that key wants a 256-byte signature.

The only `.sig` files held are the control's, and both are 128 bytes. So under A they would fail the
size check before any arithmetic. Checking them against the decoded modulus, against either half of
it, and with byte order reversed, with exponents 3, 17 and 65537, gave no padded block. This is
consistent with the control's files not being signatures made with this key. No `.sig` from an
unpatched release is held, so A has not been seen to accept any file.

## What this settles

- A is the unpatched build. B and the control are patched builds that accept any file; the control
  also renames the four labels.
- The check runs at start-up, for the executable and for `arrays2.dat`.
- The verify algorithm and block format are read, including the always-successful helper.

## Not covered

- Where the public exponent is set. The component's stored properties hold no exponent, and its
  setter's caller was not found.
- The second key string that the earlier note reports in 2.17, 2.22 and 2.31. The key setter has a
  second caller that was not followed.
- Whether an official 2.22 release carried 256-byte signatures. None is held.
