# Finding the Version ID from the Decompile

The version ID is recovered from the **PE version resource**, not from executable logic.

## Primary method: PE version resource

In a Ghidra dump the structure appears as `VS_VERSION_INFO`:

```c
struct VS_VERSION_INFO {
    word StructLength;
    word ValueLength;
    word StructType;
    wchar16 Info[16];
    byte Padding[2];
    dword Signature;
    word StructVersion[2];
    word FileVersion[4];      // four-part version
    word ProductVersion[4];
    dword FileFlagsMask[2];
    dword FileFlags;
    dword FileOS;
    dword FileType;
    dword FileSubtype;
    dword FileTimestamp;
};
```

The actual string values live in the `.rsrc` section as UTF-16. For GraalEditor the notes record them directly:

- CompanyName: `Linux Cyberjoueur`
- FileVersion: `2.3.1.1`
- InternalName: `Graal editor`
- ProductName: `GraalEditor`

That resource is present in both the packed Thinstall stub (`graal/GraalEditor.exe`) and the unpacked Delphi image. The packed-stub dump is only the loader (~3 k lines), so the version string is still readable from the stub’s resources without unpacking.

## Secondary signals

| Source | What it gives | Example |
|--------|---------------|---------|
| Filename | Client build | `Graal_2171.exe` → 2.171, `Graal_222.exe` → 2.22, `Graal_231.exe` → 2.31 |
| PE optional header | Linker version | Editor: Major/MinorLinkerVersion = 2.25 |
| Banner / About strings | Date or product string | gif2mng: `"Graal Image conversion and palette fixing tool 2004-06-03"`; `TAboutDlg` caption “Version” |
| String search | Hard-coded tokens | `graalversion`, `Version`, product names |

## Practical steps on a new dump

1. Open the binary (or the Ghidra project) and locate the version resource under `.rsrc` / `VS_VERSION_INFO`.
2. Read the UTF-16 StringFileInfo block for `FileVersion`, `ProductVersion`, `CompanyName`, `InternalName`.
3. Cross-check the PE optional header for linker version if needed.
4. For the game clients, the filename itself is the version token used in the notes.

## What the project recorded

- GraalEditor 2.3.1.1 (Linux Cyberjoueur). The file in `graal/` is a Thinstall package; the Delphi image was recovered by running the stub decompressor and the Thinstall `0xD7` block codec. Unpacked image is at `GraalEditor/unpacked/GraalEditor.exe` (Borland linker 2.25).
- Clients: `Graal_2171.exe` (2.171), `Graal_222.exe` (2.22), `Graal_231.exe` (2.31).
- gif2mng banner date: 2004-06-03.

All of the above is measured from the binaries and their resources. The version resource is the authoritative FileVersion; filenames supply the client build numbers used in the notes.
