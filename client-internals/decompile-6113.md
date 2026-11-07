# What the 6.1.1.3 decompile contains

Date: 2026-11-07. Static read of the decompile of `Graal 6.1.1.3.exe`. The C listing is 227,199 bytes and 7,005 lines. The paired HTML listing is the same image; it is used where the C listing has no string and where an export never becomes a function. Nothing was run. Tags: **[bin]**.

The 2026-11-07 gap folder and its archive hold four cleaned notes (`v5x-clients`, `v6x-clients`, `v5v6-windows-unpacked`, `v5v6-lab-play`). They do not hold a second 6.1.1.3 image. **[bin]**

Earlier pages identify the file and compare it with unpacked 6.00: `packed-6113.md`, `skipped-v6-read.md`, `engine-6113.md`. This page is the function count and the split of this listing.

## What this file is

A 32-bit Windows GUI executable. The optional header records linker version 9.0 and about 2.6 MB of code. This listing does not decompile that bulk. The image has six sections: `.rsrc`, `.idata`, two blank names, and two eight-letter names. The image timestamp is 8 August 2014, 13:19:46 UTC. **[bin]**

The version resource says product Graal, original file name `Graal.exe`, company Eurocenter Games, copyright year 2014. The file-version and product-version strings are `6.113`. The fixed version words are major 6, minor 1, build 1, revision 3. **[bin]**

The export directory is named `QPlay.exe`. The only import is `SetCurrentDirectoryA` from `KERNEL32`, and the import is not bound. No function in the C listing calls it. **[bin]**

## How the bytes split

The C listing decompiles **106 functions**.

| Piece | Functions | Bytes in the C listing | What it is |
| --- | ---: | ---: | --- |
| Entry and its two helpers | 3 | 644 | The unpacker. This is the only coherent logic |
| Named export bodies | 103 | 188,720 | Labels from the export directory. The text is long. The operations are not the named calls |
| Opening type definitions | 0 | 13,226 | PE and version-resource typedefs, then undefined globals |
| Warnings and three names that did not decompile | 0 | 24,609 | See below |

644 bytes is under one percent of the file. The 103 named bodies are about 83 percent. **[bin]**

Three further export names are comments only. `RsaSSL_Sign` stopped on overlapping inputs. `HmacSetKey` stopped when the decompiler failed. `CyaSSL_Debugging_OFF` stopped because the flow was longer than the decompiler allows. **[bin]**

## The unpacker

Entry calls one helper, then executes a breakpoint. The helper reads the byte at its return address. When that byte is the breakpoint opcode, it clears the byte and walks four kilobytes, a dword at a time, xoring each dword with a constant and then adding a second value. The recovered call passes the block, the length and the xor constant. The helper does not allocate memory, change page protection, or jump to another entry. **[bin]**

## Export names

The names are a CyaSSL client under the C++ namespace `CyaInt`, plus unmangled cipher and hash calls, plus the zlib C API. No named body calls another named body. Where a parameter is read, the use is arithmetic on a register or a flags word, not the argument the signature declares (a socket, a buffer, a key, a certificate). **[bin]**

Several names are one body. Private decrypt and the inline SSL verify share a body. MD5 update and MD5 final share a body. Get-fd and set-nonblock share a body. Read and send share a body. Want-write, the sized error-string call and keep-arrays share a body. Connect-cert and pending share a body. Get-session and set-session share a body. Seven names share one body: OCSP options, the OCSP override URL, debugging on, the logging callback, the two DTLS timeout calls, and set-compression. **[bin]**

The forty zlib names (compress, deflate, inflate, crc32, adler32, `zlibVersion`, including `inflateUndermine`, `inflateReset2` and `crc32_combine64`) are strings in the export directory. They are not functions in the C listing. At those labels the HTML listing has undefined bytes. **[bin]**

## Subsystems

| Subsystem | What the decompile shows |
| --- | --- |
| TLS client methods | Names for an SSLv3 client method, an SSLv23 client method, and TLS 1.0, 1.1 and 1.2 client methods. The TLS 1.1 body returns a register. The TLS 1.2 body is decimal-adjust arithmetic on registers. Neither builds a method table |
| Handshake and record IO | Names for context and session create and free, `set_fd`, negotiate, connect-cert, read, write, peek, send, recv, shutdown, non-blocking, and custom read and write callbacks. No body opens a socket or calls another of these names |
| DTLS | Names for a DTLS flag, peer get and set, and the two timeout calls. The timeout calls are the shared OCSP body |
| Certificates and OCSP | Names for OCSP options and an override URL, CA load, CRL enable and disable, certificate file and buffer, private key file and buffer, a domain-name check, and issuer and subject names. No body parses a certificate |
| Ciphers and hashes | Names for AES-CBC (set key, set IV, encrypt, decrypt), ARC4, MD5, SHA, SHA-256 and HMAC. SHA update is an empty infinite loop. HMAC set-key did not decompile. The other bodies are broken instructions or a short register return |
| RSA and the RNG | Names for public encrypt, private decrypt, inline decrypt, SSL sign and verify, key decode, and encrypt size, plus RNG init and generate. SSL sign did not decompile. The other bodies do not run an RSA operation |
| zlib | Forty export names, listed above. No recovered inflate, deflate or checksum routine |
| Logging | Debugging on, debugging off, and a logging callback. Debugging off did not decompile. Debugging on is the shared OCSP body |
| Graal session, GS2, GUI, files | No opcode switch, no script container, no playfield class, no form, no level or gani magic, no login token. The string search is below |

## Strings

The C listing has no string literal. The HTML listing's readable strings are the version-resource keys and values (`Graal`, `Graal.exe`, `6.113`, `Eurocenter Games`, the copyright year 2014) and the export and import names (`QPlay.exe`, `kernel32.dll`, `SetCurrentDirectoryA`, the `CyaInt` and zlib names). There is no host, no protocol sentence, no GS2 name, no GUI class name, and no level, gani or script magic. **[bin]**
