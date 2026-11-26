# Batch W, fourth pass: server flags on 5.x clients (2026-11-26)

Date: 2026-11-26. Follows [3d-batch-w-rows-part2-2026-11-26.md](3d-batch-w-rows-part2-2026-11-26.md).
Captures stay in the owner-held lab kit. **[lab]**

## T3D-133 follow-up: which flags a 5.x client takes from PLO_FLAGSET

Client: real 5.24r4 Windows (2D), in a Win10 lab VM with its clock at 2012. Server:
**seihai-gserver main at `8800c2b`** in the same VM on its lab address, guest login.

- The guest account template held `FLAG client.labflag=on` and `FLAG clientr.labflag=on`, and
  `serverflags.txt` held `server.labflag=on`.
- A clientside level NPC set its chat to `"S:" @ server.labflag @ "|C:" @ client.labflag @ "|CR:" @ clientr.labflag`
  about 4 s after the level loaded, then set `client.mine = "set"`.

At login the server sent three PLO_FLAGSET messages, each the plain text `<name>=on`:
`client.labflag=on`, `clientr.labflag=on` and `server.labflag=on`.

| Flag | Sent as | Read by the clientside script |
|---|---|---|
| `client.labflag` | PLO_FLAGSET `client.labflag=on` | `on` |
| `clientr.labflag` | PLO_FLAGSET `clientr.labflag=on` | `on` |
| `server.labflag` | PLO_FLAGSET `server.labflag=on` | **empty** |

`client.mine = "set"` went back to the server as PLI_FLAGSET `client.mine=set`.

**So FLAGSET itself works, and `server.` values do not read back in a script.** A plain
PLO_FLAGSET `server.x=v` leaves `server.x` empty in a 5.24r4 clientside script, just as in the 3D
5.12 `weapon3d` (part 2).

A separate probe on real 5.12 (seihai-gserver main `5cd9c15`) refines this: the `server.` flag is
**stored** under the client's `server.` namespace, since `getstringkeys("server.")` lists the key.
But its **value** reads empty by every syntax tried (`server.x`, `makevar("server.x")`,
`server.(@"x")`, `.length()`, `type()`). A bare name and `serverr.x` read their values fine, and
sending the flag by events only or by set only gives the same key-present, value-empty result, so
delivery is not the cause.

**The cause is the client.** A wire capture on real 5.12 (`5cd9c15`) shows the value arriving
intact on every path (TCP PLO_FLAGSET, a UDP `events` line, a UDP `set`), and the TCP PLO_FLAGSET
alone creates the empty-valued `server.` key while the same message delivers a readable
`serverr.` value. The compiler is ruled out separately (seihai-core emits `server.x` reads the
same way as the official compiler). So 5.x keeps client-received `server.` keys but blanks
their values, whatever the transport: they are read-only on the client side by design. **Rule:
send server-to-client script values as `serverr.x` or a bare name, not `server.x`.** T3D-133 is therefore a server-flag question for 2D
and 3D alike, not a 3D one.
