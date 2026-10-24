# 10 Open questions and corrections

## Corrections to batch b / earlier notes
- Batch b note 04: "2.04 swaps 26 for 25" is wrong. 2.04 only drops 26; 25 is present in all builds.
- Batch b note 04: "id 6 may be a false positive of the scan". Wrong: 6 (TOALL/chat, clipped at 200 characters) is a real sender in all 20 builds.
- Batch b treated 2.00 as one build; the 4 builds (2.00, rev1, rev2, rev3) have identical handler shapes and one token. The only differences are VCL/RTL layer changes and small UI-class edits.
- Repo `packet-ids.md` says PLO 26 NPCACTION has no handler in 2.05: confirmed, and the earlier history is now known: handled and active-level gated in 2.00-2.03, removed in 2.04.

## Open
1. Exact field layouts of the long handlers (PLAYERPROPS 9, OTHERPLPROPS 8, NPCPROPS 3, LEVELLINK 1) per build: the layout scan is too crude. Needs per-handler manual reading or a type-aware recompile of the decompile.
2. 2.04 to 2.05 UDP receive wrapper: removal of one bit-test step. Purpose not resolved.
3. Per-build UDP id sets for ids 0, 15 and 22 (movement, showimg, chat) for 2.00-2.04: the call forms were not recovered. Receiver-side sets for 2.00-2.04 are also not extracted (a second jump table the dispatcher rebuild did not cover).
4. Whether gen-3 junk-byte insertion is byte-for-byte unchanged in 2.01-2.04. The call structure matches; the index formula was not diffed.
5. The 2.1 test decompiles are lossy; argument-level facts about 49 and the changes to 0, 6, 14 there are structural only.
6. What PLI 36/38's TCP "second copy" is conditioned on (flag identity). Reading is [inferred] from the shared wrapper.
7. Purpose of TADP (new in 2.05) and of PLO 168 (empty client-side reset).
8. Whether the token digits really are a build date. The dates fit the changelog order for 2.01-2.05 but nothing in the binary names the format.
9. Not touched: tamper-check (PLI 39) is absent from this whole family; nothing here helps derive it.

## For Seihai
- To support 2.00-2.1: allow-list the tokens in `02`; handle PLO ids per build set in `04`; PLI sets in `05`. A server that serves 2.1 test must be ready for 49 and 169 as server-to-client only; no new client-to-server id exists in 2.1 test.
- Do not send ids 46+ to a 2.00 client (it has no handler) and avoid 47+ for a 2.01 client, 48/165 for 2.02, 166 for 2.03, 168 for 2.04. Unhandled ids go to a silent default in every build, so the practical effect is lost information, not a crash.
