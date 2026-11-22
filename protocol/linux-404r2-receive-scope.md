# Linux 4.04r2 object-script delivery and receive-switch scope

Subject: the owner-labelled Linux 4.04r2 x86 ELF, researcher-supplied
executable SHA-256 `50f2057117cfafd5a1151d6e6fdd1413095fa71445ff274bf923ce7dc04198aa`. This identity does not establish equivalence with
a Windows component or another release bearing a similar label.

The publication editor reviewed the sanitized 2026-11-09 research handoff and
recorded its digest. Underlying evidence digests and observations are supplied by
the researcher; raw code, captures and client assets were not opened to fill gaps.
Source IDs resolve through [the evidence index](../docs/evidence-index.tsv).

The 2026-11-22 follow-up independently read selected retained transport,
dispatch and handler exports bound to the same executable. Export hashes were
checked against the retained manifest; this was not a fresh executable hash or
a runtime experiment. Source: `L404-DELIVERY-BOUNDARIES-20261122`.

## Explicit switch coverage

`[bin]` The exact-build receive switch contains 97 explicit cases. The static
mapping retains direct handler edges for those cases. This is switch coverage,
not a complete count of handled messages. Transport processing before dispatch
must be included before a complete handled-message claim is justified.
Source: `L404-PACKET-CASES`.

`[bin]` A missing case in that switch does not establish rejection of the
corresponding message. The mapping alone does not settle script-delivery paths,
cache validation, or the relationship among candidate script messages.

## Transport and raw-message boundary

`[bin]` The selected transport body waits for a complete two-byte-length-prefixed
frame and selects a mode-dependent decode route. Its call sequence selects
candidate message extents through a helper called with LF or a saved raw extent,
then invokes a virtual callback with a byte-derived logical identifier and a
helper-derived body. Full string-slicing and delimiter-helper payload and
malformed-input semantics remain unverified by this selected read.
The retained virtual-table reconstruction suggests the known receive switch as
that callback, but the indirect call is not independently resolved across every
connection path. Source: `L404-DELIVERY-BOUNDARIES-20261122`.

`[bin]` Logical message 100 is already one of the 97 switch cases. Its selected
body sets the pending-raw flag and decodes an extent from a three-byte prefix;
the transport consumes and clears that flag when selecting a raw chunk.
It must not be added to the switch count as a separate 98th handled message.
This traces a static state relationship, not successful raw-frame delivery or
complete malformed-input behavior. Source: `L404-DELIVERY-BOUNDARIES-20261122`.

## Static message-131 path

`[bin]` Message 131 selects an object-script handler. The handler requires a
three-byte identifier, decodes a positive object identifier, chooses an object
lookup, strips those three bytes and gives the remainder to that object's script
setter. The setter creates an execution context when needed; its loading path
calls the compiled-segment reader. A non-empty payload also reaches an
initialization callback. Sources: `L404-OBJECT-SCRIPT-HANDLER`,
`L404-SCRIPT-SETTER` and `L404-SCRIPT-CONTEXT-LOAD`.

`[bin]` This establishes a static message-131-to-container-reader path for this
input. It does not establish the complete identifier encoding or all object
lookup roles. The lookup roles are inferred, and the indirect initialization
callback is not fully resolved. No message-131 network fixture was delivered.
The separate live profile-script reader experiment does not execute this
network path. Messages 140 and 197 and other weapon/class paths remain open.

## Separate message-193 lookup path

`[bin]` Message 193 selects a different handler. It requires more than five
payload bytes and a clear state flag, decodes a five-byte value, derives a
lookup argument through a helper called with a five-byte offset, and forwards
the value when the lookup returns an object. The selected trace does not
establish the lookup or value-receiving behavior. It therefore does not
establish checksum comparison, cache hit/miss, requests, persistence, or the
object's weapon/class role. Exact string-field boundaries also remain open.
Source: `L404-DELIVERY-BOUNDARIES-20261122`.

This static candidate is separate from message 131's container-loading path.
It supplies no message-193 network fixture and does not transfer another
platform's message-140 or message-197 layout to this Linux executable.

## Version boundary and remaining work

The [existing v4 study](v4x-clients.md) names Windows and macOS inputs. This
Linux case mapping is kept as its own exact-executable observation; neither the
release label nor the case count transfers another platform's field layouts.
No complete wire layout, successful login or gameplay compatibility is claimed.

- [x] ~~Count the explicit cases of this receive switch with direct edges.~~ The scoped static map has 97.
- [ ] Resolve the transport's indirect dispatch across relevant connection paths
  before publishing a complete handled-ID set; message 100 is already counted.
- [ ] Recover the message-193 lookup and value-receiving helpers and trace cache
  checks before resolving competing script-delivery roles.
- [x] ~~Trace one object-script delivery into the compiled-container reader.~~
  The static message-131 path above supplies a partial exact-build answer.
- [ ] Deliver a message-131 fixture and resolve lookup/callback semantics before
  claiming network-path validation or closing the broader delivery question.
- [ ] Capture version-specific message payloads before asserting field layouts.
