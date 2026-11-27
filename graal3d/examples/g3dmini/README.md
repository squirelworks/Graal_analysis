# g3dmini: a small Graal 3D server

`g3dmini.py` is the UDP half of a Graal 3D server for the Torque protocol 24 clients (4.20r8,
5.00r7, 5.12 and Frankenstein 6.037), in one file of standard-library Python. It goes with part 8
of the [community guide](../../community-guide.md#8-writing-your-own-server).

It does the handshake, the notify link, guaranteed events, ghosts (Sun, Sky, TerrainBlock,
GameObjects and a Camera per client), the mission start with phase 2 held until the terrain is
in, terrain streaming by stamp, and relays each player's position to the others.

It does not do the TCP side. A real client also logs in over TCP on the listed port, fetches
every file there and waits for `PLO_SERVERLISTCONNECTED`; pair g3dmini with a server that does
that, or read seihai-gserver's `src/graal3d/` for a complete one.

```text
python3 g3dmini.py --make-terrain hills     # 256 demo chunks and heights.info
python3 g3dmini.py --world world.txt        # UDP on localhost:14901
python3 g3dmini.py --help
python3 -m pytest -q                        # the checks below
```

`world.txt` is a sample world. Its shapes and textures (and the four terrain textures named in
`hills/heights.info`) are not included; any `.dts` version 24, `.3ds` with a material, and
8-bit PNG will do.

`test_g3dmini.py` checks the encoders against the test vectors in
[torque/udp-session.md](../../../torque/udp-session.md) (the 71-byte connect request, the 276-byte
accept, the GameObject, Sun and Sky payloads, the real client's first packet), chunk encoding and
settling, and runs one loopback login with a scripted client: both mission phases, all 256
chunks, the six ghosts, the control object and the camera.
