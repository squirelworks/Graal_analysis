# build-diff

Cross-build function matcher used for `client-internals/build-diff-204-205.md`.

1. In Ghidra (headless), after analysis and name application, run `ExportFeatures.java <out.jsonl>` on each build.
2. Run `python3 fdiff.py old.jsonl old.exe new.jsonl new.exe out.json [Class1,Class2,...]`.
   The optional class list turns off virtual-slot name matching for classes whose VMT shifted between the builds.

The output lists identical, changed (with instruction-stream similarity and string-literal deltas), only-old and only-new functions.
