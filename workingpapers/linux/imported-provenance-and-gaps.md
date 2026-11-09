# Imported Linux notes: provenance and recovery gaps

Document-only review, 9 November 2026. The imported Cursor and Gemini collections are third-party research inputs. This note records useful recovery leads and checks on the documents; it does not authenticate their client binaries or adopt their engine conclusions. Original installers, imported scripts and analysis tools were not run. Server and server commit: none.

## What was independently checked

[file] A prior document-only review recorded exact document digests privately and found byte-identical counterparts for three imported Linux analysis logs. These are duplicate documents, not independent replication or proof that any two executables match.

[doc] The Linux analysis documents contain headless import, analysis and save-success messages. They are tool-run logs, not selected function exports. Their loading messages include truncated MD5 hints, without independently verified executable identities linking these imported runs to approved Linux inputs. Successful analysis logging does not establish complete decompilation or specific file/cache behavior.

## Useful imported claims, not independently reproduced

[doc] **Archive labelled 3.15r1 / internal label 3.151.** Cursor's inventory and extraction log say the installer identifies itself as Linux 3.151. They report a payload 139 bytes shorter than its declared size, a corrupt gzip stream and no recovered client ELF. This is a concrete replacement-archive lead and a reason to preserve both labels. The review did not rerun extraction or establish the full original-installer digest. It does not identify this archive as 3.153 or settle Appendix E#208.

[doc] **Linux 5.12.** Cursor reports recovery of an installer bootstrap tar, including a bootstrap package, but failure of the game payload's bzip2 integrity checks. Its log says nine recovered blocks remained unusable and a tenth was incomplete; no client ELF was recovered. These are reported extraction outcomes, not a repair reproduced here. Bootstrap files must not be counted as a recovered 5.12 game engine.

[doc] **Duplicate and installation accounting.** Cursor reports two byte-identical 4.20r8 installers and distinguishes a packed 3.04 setup helper from the packed game client. It records Makeself headers without a no-execution option, autopackage payload metadata and bundled audio-library differences between the 4.x packages. These details are useful follow-up and installation-provenance leads. Installer equality, package integrity and library contents were not independently rechecked against original archives in this review. A prepared extraction tree is not automatically a completed installation or an authenticated release.

## Claims excluded from established findings

[doc] A Gemini REA summary repeats Windows DLL-import and decorated-type details in its Linux sections. That platform inconsistency prevents treating the generic summary as verified Linux architecture evidence. Its later Ghidra report logs successful analysis after an earlier report says the provider was unavailable; these may describe different runs, but the documents alone do not establish the complete chronology and input linkage.

[doc] The imported `full-extract/README.md` explicitly identifies an unpacked Windows 6.03 executable as its primary input. It is not a Linux 6.01 x64 selected-function export. The three Linux analysis logs therefore do not fill the missing Linux cache-helper evidence simply by appearing beside that package.

[inf] Broad imported conclusions that Torque was completely purged or all residual strings are dead are not supported by marker absence alone. The existing [Linux architecture handoff](README.md#coverage-and-architecture) correctly separates visible infrastructure changes from proof of total code removal. No imported claim changes the published scripting, event, cache or runtime contracts here.

## Evidence boundary

The imported source documents and archive-member mapping remain owner-held. The public index identifies evidence class and platform only; it does not expose filenames, package names, member paths, exact digests or retrieval instructions. Claims above remain attributed to the imported reports and are not represented as independently reproduced.

## Follow-up boundaries

- [x] ~~Review imported Linux documents and separate useful provenance leads from established behavior.~~
- [x] ~~Hash the reviewed documents and deduplicate the three repeated analysis logs.~~
- [ ] Link imported executable and original-installer full digests to approved inputs before transferring their claims.
- [ ] Obtain an intact archive for the reported 3.151 and 5.12 failures; no new extraction or repair is asserted here.
- [ ] Locate retained exact-input function evidence before claiming that these imports resolve Linux 6.01 x64 local cache/file structure.

No new experiment, imported-script execution or code transfer to implementation repositories is part of this note.
