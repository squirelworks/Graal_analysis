# Several 3D clients in one world: questions and lab design (T3D-065 to T3D-076)

This note plans how to find out what Graal3D does when two or more players
are in the same 3D world: how each client shows the others, what carries
their movement and looks, what content passes between them, and what happens
when the clients are different builds. It is a plan, not a result.

## What the static reads already say

- **5.12.** Other players are most likely `GameObject` ghosts:
  - 5.12 has no `Player` class, and its `GameObject` carries the fields a
    player needs: `nickname`, `nickcolor`, `shape`, `attachedtoobject`,
    `movetype`, `velocity`, `collision`.
  - `GuiShapeNameHud` draws name tags (distance fade, chat profile, offsets).
  - The host exposes `getPlayerNickName` and an external player-list
    update, and `onRemotePlayerChats` is among the GS2 events.
  - **[bin][inf]**
- **4.04r2.** The stock Torque `Player` and `PlayerData` are registered for
  scripts, with the footstep, splash and impact sounds, beside `AIPlayer` and
  the same name HUD. Other players may arrive as stock `Player` ghosts with a
  datablock. **[bin][inf]**
- **3.153.** This is stock TGE plus Graal's network changes, so stock `Player`
  ghosts are expected. **[inf]**
- **All three.** Each client also keeps the classic Graal TCP connection, where
  other-player props (head, body, colours, gani, chat, nickname) normally
  arrive. Which of the two channels drives the 3D view of another player is
  the main open question (T3D-068).

## Lab design

The lab runs on lab host A. Each client gets its own VM or VM clone. Shared VMs are
never power-cycled, and every client connects only to seihai-gserver-v2 in
graal3d mode on the lab network.

| Pair | Builds | VMs |
|---|---|---|
| S1 | 5.12 + 5.12 | two Win10 clones |
| S2 | 4.04r2 + 4.04r2 | two Win10 clones |
| S3 | 3.153 + 3.153 | two PPC Mac OS X instances, if the host can run two |
| M1 | 4.04r2 + 5.12 | two Win10 clones |
| M2 | 4.20r6 (Mac) + 5.12 | Mac VM + Win10 clone |
| M3 | 3.153 + 5.12 | PPC VM + Win10 clone |
| H1 | 2D client (5.24r3) + 5.12 in the same level | two Win10 clones |
| N1 | three or more 5.12 at set distances | three Win10 clones |

Same-build pairs (S) come first. They give the baseline for the mixed
pairs (M), the hybrid pair (H) and the crowd run (N).

### Join first, and capture and observe together

The main question is what each client does when other players join. Every
pair therefore starts with a join phase: A connects and idles, then B joins,
then C where the setup allows.

Every step records two things together, never one without the other:

- **Packets.** A capture of each client's own traffic, TCP and UDP in both
  directions. Each client gets its own capture.
- **Client-side observation.** A screenshot, the console log and the 3D event
  trace from the probe weapon.

Clocks are kept in sync, and each step's start time goes on a step log. For
each join, leave and reconnect, the report gives a timeline: what B sends,
what A receives because of B's join, what A draws or logs, and how long that
takes.

### Steps for each pair

1. Start the server with one small world: flat terrain, one shape and a Sun.
   Clear `levels3d/` and `FILENAMECACHE.txt` on every client.
2. Log both clients in with distinct accounts, looks and nicknames.
3. Capture TCP and UDP on the server side for each client separately.
4. Run a fixed script of actions on client A, with screenshots from client B
   after each:
   - stand still;
   - walk in a square;
   - jump;
   - change head, body, colours and gani;
   - say chat text;
   - send a PM;
   - fire or use a weapon;
   - touch an NPC or trigger;
   - walk into B;
   - mount or attach where the build allows;
   - disconnect, then reconnect.
5. Repeat with B as the actor.
6. On each client, run a GS2 weapon that logs these events:
   - `onGhostAlwaysObjectReceived`, `onRemotePlayerChats`, `onCollision`,
     `onMount` and `onUnmount`;
   - the player-list callbacks.

### What to record for each pair

- How B shows A:
  - the ghost class and the update fields used;
  - the shape and its skin;
  - the name tag (text, colour, distance fade);
  - the animation, the chat bubble, and whether head and body show.
- Which channel carries A's movement, and how the timing compares between UDP
  ghost updates and TCP prop packets.
- For each kind of content (files, attachments, chat, PM, weapons, NPC
  objects): did B get it from the server, or relayed from A?
- Mixed builds:
  - ghost errors, unknown classes and dropped connections;
  - what each side draws of the other;
  - whether the server must split worlds by protocol (19, 21, 24).
- Hybrid level: what the 2D client shows of the 3D player and the reverse.
- Crowd run: how many ghosts each client holds against distance, and what is
  deleted when a player leaves.

### Server-side needs

These are for the gserver 3D thread:

- The server can put several clients in one 3D world.
- It ghosts each player to the others in the form each build expects
  (GameObject for 5.12; probably Player for 4.04r2 and 3.153).
- It mirrors the classic other-player props on TCP.
- It logs per-client ghost traffic for the captures.

Where the server can't yet do one of these, the lab records the client's
behaviour with what the server sends, and the gap goes on the board.

## Board rows

T3D-065 to T3D-076, area "Multi-client", in
[3d-capability-board.tsv](3d-capability-board.tsv).
