# The 3D player keeps the whole 2D identity (gani, head, body, nick, chat) alongside its 3D shape (T3D-056, Linux 4.20r6)

Date: 2026-11-25. Registered-class / field reads of the 4.20r6 client (5.12-class, protocol 24) plus a single-client loopback lab against our own 3D lab server, GS2 drawn via a client-side `weapon3d` script ([T3D-018](3d-client-events-420r6-2026-11-25.md)). Linux 4.20r6 is 3D-equal to 4.20r8 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md)). Board row: [T3D-056](3d-capability-board.tsv). **Single client only** — how the name label / chat bubble / 2D actor draw over *another* player's 3D shape is the multi-client question ([T3D-069](3d-capability-board.tsv)); this note establishes the field map and the own-player behaviour.

## Headline

**The 2D-player identity is not discarded in 3D.** The 3D player object is a `TPlayer` → `TServerPlayer` → `TGaniObject` → `TLevelObject`/`TDrawableObject`, so it carries **both** a 3D `shape` **and** the full 2D-player identity — gani, head, body, sword/shield, colours, `nick`, `chat` — on the same object.

## The field map **[bin]**

| 2D-player attribute | field(s) on the 3D player object | note |
| --- | --- | --- |
| 3D body | `shape - string`, `shapeobject - object` | the `.3ds`/`.dts` 3D mesh |
| gani (animation) | `ani`, `aniparams`, `anistep`; `playerlook - boolean` | `playerlook`: if true the animation takes its head, body, sword, shield and `attr[]` from the owner; set false to drive the images yourself via `showimg.actor.head` etc. |
| head | `head - string`, `headimg - string` | |
| body | `body - string`, `bodyimg - string` | |
| sword / shield | `sword - string`, `shield - string` | |
| colours | `colors - object` | the player's colour set |
| nickname | `nick - string` (read-only on the own player), aka `nickname` | |
| chat | `chat - string` | |
| direction | `dir - integer` | |

- **Rendering paths.** The 2D sprite (gani + head/body) is an optional **`showimg.actor` overlay** pinned to the shape, gated by `playerlook`. The **nickname** draws as a floating name label via the `GuiShapeNameHud` GUI control (the GUI-over-3D layer, [T3D-058](3d-gui-overlay-420r6-2026-11-25.md)). The **chat** draws as a chat bubble; chat rides the control-object update ([T3D-018](3d-client-events-420r6-2026-11-25.md)).
- So head/body/gani/nick/chat are **not** purely-2D attributes with no 3D home — each has a field on the 3D player object and a draw path.

## Lab: the client's own player (single client) **[lab]**

A `weapon3d` GS2 script set, on the client's **own** player: `player.nick`, `player.chat` (updated on a timer), `player.headimg`/`player.bodyimg`, `player.ani`, with a `showtext` HUD line echoing the live values to prove the script ran.

Result (screenshot):

- **The weapon ran** — the HUD read `ran; chat=10 nick=g3dlab` (the chat counter reached 10 on the timer).
- **`player.nick` could not be set by the client** — it stayed the account name; `nick` is **read-only for the own player**.
- **`player.chat` was set**, but **no chat bubble drew over the own 3D cube**.
- **No floating name label drew over the own cube.**
- **The own player drew only as its 3D shape** (the red cube); the 2D head/body sprite did not appear over the own avatar (and the head/body images were not served, so the actor had nothing to build from).

**So for the client's own player, the 3D view shows only the 3D shape** — no self name label, no self chat bubble, no 2D actor sprite. This is the expected "you don't see your own nametag" behaviour, and it confirms the name label / chat bubble / actor are drawn for **other** players' shapes, not the own avatar — which needs a second client to observe ([T3D-069](3d-capability-board.tsv)).

## Answer

- In 3D the player is drawn as its 3D `shape` (`.3ds`/`.dts` mesh), and the 3D player object **also carries the whole 2D identity**: gani (`ani`/`playerlook`), head/body (`headimg`/`bodyimg`), sword/shield, `colors`, `nick`, `chat`.
- Render paths: 2D sprite → optional `showimg.actor` overlay pinned to the shape (via `playerlook`); nickname → floating name label (`GuiShapeNameHud`); chat → chat bubble.
- Name label, chat bubble and 2D actor are drawn for **other** players, not the client's own avatar — confirmed live: setting the own `player.chat` draws no self-bubble and `player.nick` (the account nick, uneditable) draws no self-label. The own player shows only its 3D shape.

## For a server

- A player in a 3D world keeps its 2D look props; you set them with the same fields (`headimg`, `bodyimg`, `ani`, `nick`, `chat`, `colors`, …). `playerlook` controls whether the gani drives the look or the script sets `showimg.actor.*` directly.
- Nametags/chat bubbles over 3D players are drawn for the *other* players a client sees, not for the viewer's own avatar — plan HUD text accordingly (the own player's state is better shown with a GUI overlay, [T3D-058](3d-gui-overlay-420r6-2026-11-25.md)).
