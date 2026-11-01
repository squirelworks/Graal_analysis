# Notes navigator

A local browser for the markdown notes in this repository. It is a navigator, not a research note. The index (path, title, folder) is built when the process starts. Nothing is written back into the repo.

## Start

From the repository root:

```
python3 tools/navigator/navigator.py
```

Then open the page in a browser on this machine. The process listens on the loopback address, port 8765. That port is not a lab server port.

```
python3 tools/navigator/navigator.py --port 8766
```

The bind address defaults to the loopback address, built the same way as `tools/lab-servers/listserver.py`. Any other host is refused. `--repo` can point at another checkout; it defaults to this repository.

It walks markdown files and skips `.git`.

## Local only

Search filters the title and the path in the browser. There is no search service. The process does not phone home: no telemetry, no analytics, and no outbound request. It serves only markdown files inside the repository, and it refuses a path that leaves the repository. Raw HTML in a note is escaped, not executed.

## Tests

```
python3 -m pytest tools/navigator -q
```
