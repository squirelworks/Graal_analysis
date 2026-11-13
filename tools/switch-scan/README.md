# switch-scan

`swscan.py <file.exe|file.dll> [min] [max]` lists the `jmp [reg*4+table]` switches in a 32-bit PE whose bound lies between `min` and `max`, with the case values that do not go to the default target. It handles a byte index table and a bias before the jump. It reproduces the published handled-id sets for the 2.05 Delphi client and the 4.20r8 engine, and was used for [protocol/v4x-windows-403r3-411.md](../../protocol/v4x-windows-403r3-411.md) and the 4.x rows of [plo-handled-ids-by-build.tsv](../../version-profiles/plo-handled-ids-by-build.tsv).

It prints switch locations so you can find them again. Do not copy those into notes (`AGENTS.md`, "No binary addresses"). A packet dispatcher may test some ids before its switch (4.11 and later test 100 and 108 first), so check the code just before the switch.
