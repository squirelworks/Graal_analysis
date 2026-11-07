# Notes navigator

A local map of the markdown notes in this repository. It is a navigator, not a research note. Nothing is written back into the repo.

## Start

From the repository root:

```
python3 tools/navigator/navigator.py
```

Then open the page in a browser on this machine. The process listens on the loopback address, port 8765. That port is not a lab server port.

The bind address defaults to the loopback address, built the same way as `tools/lab-servers/listserver.py`. Any other host is refused. `--port` and `--repo` override the port and the checkout.

## Local only

The process does not phone home: no telemetry, no analytics, and no outbound request. It serves only markdown files inside the repository, and it refuses a path that leaves the repository. Raw HTML in a note is escaped, not executed. Search compares the title and the path on this machine. There is no search service.

## Home map

The home page is one screen with three parts:

- An architecture diagram of the corpus areas: client versions, protocol, formats, NPC scripts, Graal3D, Torque, tools, labs and archives. Choosing an area opens that cluster.
- A web of the relative markdown links inside the focused area. Choosing a node opens the note. A large area shows the linked notes, not every file. Search filters that web; it is not the whole page.
- A version map from left to right: 1998 and 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, and Graal3D. A node is linked only when that note is in the repository.

The note page is the reader, with a strip of the notes that link here and the notes this page links to.

## Tests

```
python3 -m pytest tools/navigator -q
```
