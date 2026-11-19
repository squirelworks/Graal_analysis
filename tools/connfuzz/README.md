# conf.gs connector fuzzer (lab only)

Date: 2026-11-19

A lab tool that stands in for the Windows 6.1.1.3 **connector host** on the
loopback address: it builds the signed `conf.gs` reply container, applies one
mutation at a time, and serves it over plain HTTP so a real 6.113 client in a
lab VM fetches it. It is the connector-gate counterpart to `../probe/`, which
fuzzes the **game** wire one gate later.

Design, mutation taxonomy, the key patch that unlocks deep (post-verify)
fuzzing, and the crash/hang/accept triage are in
[`../../protocol/conf-gs-fuzzing.md`](../../protocol/conf-gs-fuzzing.md). The
container format is [`../../protocol/connector-script.md`](../../protocol/connector-script.md) §2.

**Lab only.** It serves on loopback behind a VM or network namespace with no
route to the public network. It is never pointed at any real connector host, and
nothing here helps reach one. No key, host or reply body is embedded or written
to disk.

## Parts

| File | Role |
|---|---|
| `connfuzz.py` | Builds the `{marker, 256-byte signature, inner length, payload}` container; the one-field-at-a-time mutator library; a stdlib HTTP responder for `GET /conf.gs?p=...`. Signing is external (`sign_payload`), with a lab key supplied at run time — no key is committed. |
| `selftest.py` | Offline: asserts the container layout, that each mutator changes exactly the field it names, and that the HTTP composer honours its options. No client, no keys, no network. |

## Run

Offline selftest (CI-safe, the way `../probe/selftest.py` runs):

```sh
python3 selftest.py
```

List the mutations, then serve one on a loopback port for a lab client:

```sh
python3 connfuzz.py --list
python3 connfuzz.py --mutation len:oversize --port 8080
```

### Two phases (see the design note)

- **Phase A — container framing.** Mutate the marker, the 256-byte signature
  field, the 4-byte inner length, and the payload-vs-declared-length, around an
  inert payload. Runnable against a **stock** client: these fields are consumed
  before the signature verdict matters, so a defect here is pre-authentication.
- **Phase B — decrypted script content.** Needs the trust-anchor swap (the key
  patch) so the client accepts replies signed with a lab key. Produce the real
  256-byte signature with `sign_payload(payload, signer_cmd)` — the bare-SHA-256
  PKCS#1 v1.5 type-1 scheme — then mutate the script body, the id tables, the
  token and the cipher params. The connector **payload cipher** must be pinned
  first for the client to *run* a mutated script (Still open in the design note).

### Observing the client

The client runs in the lab VM and is read from outside with the method in
[`../../client-internals/hypervisor-live-debug.md`](../../client-internals/hypervisor-live-debug.md)
(host-side snapshots and hardware breakpoints, no in-guest debugger). Classify
each reply as crash / hang / silent-reject / accept-and-diverge / no-effect, and
log the mutation label with the outcome so any finding reproduces. An
accept-and-diverge reply hands off to `../probe/gen5probe.py` for the game wire.

Keep every capture, key, host and reply body off git (see `../../AGENTS.md`).
