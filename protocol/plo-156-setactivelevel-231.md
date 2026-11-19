# PLO_SETACTIVELEVEL (156): the extra step in 2.31

Date: 2026-11-19. Static read of the Windows 2.31 client, compared with 2.17.1 and 2.22.
Issue #647. Evidence `W231-SETACTIVELEVEL-STATIC-20261119` ([index](../docs/evidence-index.tsv)).

## Summary

The step that 2.31 adds after `PLO_SETACTIVELEVEL` (156) is the **launch-link start
parameters**. 2.31 is the first client here that understands a `graal://` link on its
command line. When the client was started with such a link and the link carries text
after the server name, the first 156 of the session makes the client send that text to
the server as a `PLI_TRIGGERACTION` (38) named `serverstartparams`. Then the client
forgets the text, so this happens once per launch. A client started without a link, or
with `-connect`, never does it. **[bin]**

So the step has no effect on the client's own state, and nothing visible happens on
screen. Its only effect is one extra client→server message. **[bin][inf]**

## What 156 does, by version

| Step | 2.17.1 | 2.22 | 2.31 |
|---|---|---|---|
| Body | the level name (rest of the message) | the same | the same |
| `.gmap` name | loads the gmap and makes it the object level | the same | the same (the gmap lookup gains one flag argument; effect not traced) |
| Other name | looks the level up and makes it the object level | the same | the same |
| Afterwards | nothing | nothing | if start parameters are pending: send them as a trigger action, then clear them |

The body format is unchanged in 2.31, so a server needs nothing new to talk to it. **[bin]**

## Where the start parameters come from (2.31)

The client reads its command line once at start-up. **[bin]**

| Argument | Server name | Start parameters |
|---|---|---|
| `-connect NAME` | `NAME` | cleared |
| `graal://SERVER/TEXT` | `SERVER`, trimmed | `TEXT` (everything after the first `/`), trimmed |
| `graal://SERVER` | `SERVER`, trimmed | cleared |

The server name is the same value `-connect` sets, the name the client looks for in the
server list. The text after the first `/` is kept as it is apart from trimming spaces and
control characters at both ends; it is not URL-decoded. **[bin]**

## The message it sends

When start parameters are pending, the 156 handler builds a trigger action and sends it,
in the same way a script's `triggeraction` does: **[bin]**

```
PLI_TRIGGERACTION (38): npc id 0 (three bytes), x 0, y 0 (one byte each, half-tiles),
                        "serverstartparams," + TEXT
```

- The action name is the lower-case text `serverstartparams`, followed by a comma and the
  text from the link. If the text is empty, nothing is sent, because the parameters are
  only kept when there is text. **[bin]**
- The NPC id is 0 and the position is 0, 0, so the server sees a trigger action that is
  not aimed at an NPC or a tile. **[bin]**
- The routine is the client's general trigger-action sender. Besides the server send it
  has a second, local branch that only runs under a client mode flag not traced here;
  in an ordinary online session only the server send matters. **[bin][inf]**
- The parameters are cleared straight after, so a later 156 (another level, a gmap
  crossing) sends nothing. **[bin]**

Purpose, inferred: an official server could pick up a web link such as
`graal://Some Server/event=42` and react in its level or NPC-server scripts when the
player arrives. Waiting for the first 156 means the server has already put the player in
a level when the action arrives. **[inf]**

## Other clients

- 2.17.1 and 2.22 have no `graal://` handling and no `serverstartparams` text. **[bin]**
- 4.20r8, 5.00r7 and 5.12 accept `graal://` links but carry no `serverstartparams` text,
  so this step did not survive into 4.x. On 4.x 156 starts the Login session's warp
  instead (`../client-internals/live-behaviour-404.md`). **[bin]**

## For servers and Seihai

- A server can ignore a `serverstartparams` trigger action. GServer-v2 treats it as an
  ordinary trigger action from the player. **[srv]**
- To test it: start 2.31 with a `graal://` link that names the lab server and has text
  after it, then watch for the trigger action after the first 156. The probe proxy logs
  it as a `C>S` line with id 38. Confirmed in [the 2026-11-19 lab](lab-baddyprops-ganiscript-156-2026-11-19.md#231-start-parameters-after-156-647). **[lab]**

## Open

- [x] ~~Lab: start 2.31 under Wine with `graal://<lab server name>/hello` and confirm the
  `PLI_TRIGGERACTION` after the first 156, and that a second 156 sends nothing.~~ Confirmed in
  [the 2026-11-19 lab](lab-baddyprops-ganiscript-156-2026-11-19.md#231-start-parameters-after-156-647).
- [ ] Whether the extra flag on the 2.31 gmap lookup changes anything a player can see.
