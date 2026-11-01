# Ghidra headless salvage pipeline

Reference scripts for static reads of recovered server tools, staff clients, and
trainers. They live here because the exporter writes decompiler output, import
lists, and addresses into a local folder. That output is never committed.
Hand-written plain-behaviour summaries of those binaries live in
`squirelworks/seihai-servertools` (`recovered-drive-tools/`, `recovered-hacks/`),
not in this repository and not in the Seihai client.

Treat inputs as recovered tooling. Record purpose, CLI, protocols, and config
roles in your own words. Do not invent malware or exploit payloads.

## Layout

| Path | Role |
| --- | --- |
| `current` → `ghidra_12.2_PUBLIC/` | Installed Ghidra release (gitignored) |
| `ghidra_scripts/ExportSalvageArtifacts.java` | Post-analysis export script |
| `analyze_tool.sh` | One-shot wrapper: prelim snapshot + headless. Raw files stay in `local-out/`. |
| `projects/` | Scratch Ghidra projects (deleted per run by default) |

`analyze_tool.sh` reads `JDK_HOME` or `JAVA_HOME` (JDK 25 or newer). Optional
`RIZIN_BIN` is a directory prepended to `PATH` when `rz-bin` is not already
there. There is no default install path.

The second argument of `analyze_tool.sh` is the directory for a hand-written
`SUMMARY.md`. The script creates a counts-only stub there if the file is
missing, and leaves an existing summary alone. For the recovered Drive tools
and trainers, that directory is the matching folder already kept in
seihai-servertools. Do not commit a second copy of those notes here.

Raw exporter output (strings, imports, decompilation, disassembly) goes to
gitignored `local-out/` and is not committed.

## Versions

See `VERSION.txt`.

- **Ghidra:** 12.2 PUBLIC (`20261016`)
- **JDK:** Temurin 25.0.5+8 (Ghidra 12.2 requires Java 25+)
- **Helpers:** `file`, `strings`, `binutils` (`objdump`/`readelf`/`nm`), `radare2`/`r2`, `rizin`/`rz-bin`, `xxd`, `python3`

## Install / refresh Ghidra

If `current/` is missing (fresh clone), from this directory:

```bash
mkdir -p /tmp/ghidra-dl
cd /tmp/ghidra-dl
curl -L -o ghidra.zip \
  "https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_12.2_build/ghidra_12.2_PUBLIC_20261016.zip"
unzip -q ghidra.zip
mv ghidra_12.2_PUBLIC /path/to/Graal_analysis/tools/ghidra/
ln -sfn ghidra_12.2_PUBLIC /path/to/Graal_analysis/tools/ghidra/current
```

Install a JDK 25 build yourself and export `JDK_HOME` to it. Point Ghidra at
that JDK by setting `JAVA_HOME_OVERRIDE` in
`ghidra_12.2_PUBLIC/support/launch.properties` to the same directory.

Verify:

```bash
export JDK_HOME=/path/to/jdk-25
"$JDK_HOME/bin/java" -version
tools/ghidra/current/support/analyzeHeadless 2>&1 | head
```

## Analyze one binary

```bash
export JDK_HOME=/path/to/jdk-25
tools/ghidra/analyze_tool.sh \
  /path/to/binary \
  /path/to/summary-dir
```

Optional third arg: max functions to decompile (default `40`).

```bash
tools/ghidra/analyze_tool.sh ./some-tool /path/to/summary-dir 60
```

### Output tree

```
summary-dir/
  SUMMARY.md                 # hand-written prose only (the only note worth keeping)

tools/ghidra/local-out/<tool>/    # gitignored
  summary_stats.txt          # counts; string bodies omitted
  functions.txt|.csv
  imports.txt
  exports.txt
  strings_interesting.txt
  decompiled/
  prelim/                    # file/strings/readelf/rizin/radare2
  logs/
  DO_NOT_COMMIT.txt
```

Do not copy `local-out/` into `SUMMARY.md`. Describe behaviour in your own words.
Do not write dotted addresses, decompiled C, or auto-generated function names
into a committed note. Labs stay on the loopback address.

## Raw analyzeHeadless

```bash
export JDK_HOME=/path/to/jdk-25
export JAVA_HOME="$JDK_HOME"
export GHIDRA_HEADLESS_MAXMEM=4G
GHIDRA=tools/ghidra/current
$GHIDRA/support/analyzeHeadless \
  tools/ghidra/projects myproj \
  -import /path/to/bin \
  -overwrite -deleteProject \
  -scriptPath tools/ghidra/ghidra_scripts \
  -postScript ExportSalvageArtifacts.java /tmp/out 40
```

Point `-postScript` at a gitignored directory (`local-out/` or `/tmp`). Do not
point it at a path whose text files would be committed.

## Notes

- Headless deletes the scratch project by default (`-deleteProject`) so reruns stay clean.
- Decompilation targets entry points, name-matched helpers, then large or busy functions. That C stays under `local-out/`.
- The exporter skips unnamed auto-generated functions when it builds the local counts file, so those names are not copied forward.
- Interesting-string filters bias toward paths, CLI flags, URLs, config extensions, and server-related tokens. Those hits stay under `local-out/` and are not written into `SUMMARY.md`.
- `summary_stats.txt` records counts only. It does not embed string bodies.
- Committed summaries are prose: what the tool does, which screens or formats it touches, and what a later clean-room note could learn. No string dumps, import lists, or addresses.
