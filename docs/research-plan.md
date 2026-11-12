# Research plan, November 2026

Planning snapshot: 12 November 2026. This page puts the open research issues in
order and shows what each one unblocks. It adds no findings. The avenues
themselves are in #370, the manual's milestones in #191, and the ordered agent
tasks in [`NEXT.md`](NEXT.md). When an issue closes, strike its row here in the
same PR.

Every item follows [`AGENTS.md`](../AGENTS.md): lab runs are offline against lab
servers, findings are published as plain behaviour with a source tag and a
manual carry, and keys, captures, account details, hosts and machine names stay
out of the repo.

## Wave 1: finish what is already running

These started on 2026-11-11 and are partly done. Each one unblocks work in
another repo, so they come first.

| Issue | Question | Kind | Unblocks |
|---|---|---|---|
| #396 | Where the 6.1x outgoing cipher starts, which cipher it is, and where its key comes from | [cap] [lab] | #397; the 6.x repro clients; the Seihai 6.x scope (seihai#377) |
| #398 | Per-build action results from the client test harness, 1.x to 6.x | [lab] | Part IV tables (#370 avenue 1); Seihai and repro fidelity checks |
| #399 | Mac PowerPC runtime: 4.20r6 machine field, 4.04r2 and 5.12 live, flag sends | [lab] | #370 avenue 6; Mac rows in `version-profiles/` |
| graal-client-repro#203 | How the 140 builds in the repro v0.0.4.1 release compare with the real 6.x clients | [lab] | graal-client-repro#106 and #108 |
| #400 | Main CI is green again (Linux manual PDF without apt) | CI | Trustworthy checks for every PR below |

Order inside the wave: #400 first (small, and every later PR needs green
checks), then #396, since #397 builds on it. #398, #399 and graal-client-repro#203
run in parallel on separate lab VMs.

## Wave 2: protocol facts the servers and clients need

| Issue | Question | Kind | Needed by |
|---|---|---|---|
| #397 | What the 6.1x/7.x connector script sets up: protocol, cipher, id tables, login | [bin] [lab] | Seihai 6.x/7.x client (Issho); the repro 6.x/7.x builds |
| #254 | The packet ids still open: 132, 133, 181, 104's flag byte, 108 sub 1, 124 | [bin] [lab] | seihai-gserver stages 4 to 6; seihai-rc |
| #378 | The upstream gs2lib packet name beside each id in the protocol notes | doc | Every repo that cites an id (one vocabulary across the suite) |
| #245 | The two damage and file-transfer points left | [lab] | seihai-gserver#50 (real clients hurting each other) |
| #370 avenue 7 | Server, listserver and RC behaviour against the GPL fork in the loopback lab | [lab] | seihai-gserver stage 4; seihai-rc stage 4 |

## Wave 3: behaviour tables and the manual

| Issue | Work | Kind |
|---|---|---|
| #370 avenue 1 | Measured cadences and the `unmeasured` cells, run through the #398 harness instead of by hand | [lab] |
| #370 avenue 3 | One GS2 opcode and operand table across 4.2.0.8, 5.0.0.7, 6.00 and 6.1.1.3 | [bin] |
| #370 avenue 10 | 7.x Worlds runtime: cadence, lifecycle, the IDs 15/16 encoder ranges | [lab] |
| #370 avenue 11 | The evidence index and authored fixtures, groundwork for 0.0.7 | doc |
| #191 | Carry each wave into the manual; tags and releases only on the owner's go-ahead | doc |

## Held: the owner decides or supplies something

| Issue | Waiting on |
|---|---|
| #247 | A written yes before any 5.x/6.x Login capture against a public server |
| #246 | A 1.32 client export |
| #370 avenue 8 | Archive copies of the missing builds (1.32; a build between the 2.1 tests and 2.22) |
| #243 | Read as lifted for research by #370; the 3.04 stage 0 captures still need a lab slot |
| ~~#244~~ | ~~Now from the public pyReborn repository~~ Done: [study](../client-internals/pyreborn-study/README.md) |

## How to use this page

- Pick the first open row of the earliest wave that has no open dependency.
- Before starting, fetch `main` and check open PRs for overlap, as `AGENTS.md` asks.
- When a row's issue closes, strike the row in the same PR that closes it, and
  move anything left over to the next wave or to App. E of the manual.
