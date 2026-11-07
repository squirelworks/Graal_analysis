"""findptr.py PID TARGET_HEX SPAN: find dwords in the exe image (0x400000-0x1000000) pointing into [TARGET-SPAN, TARGET]."""
import ctypes, struct, sys
k = ctypes.WinDLL("kernel32")
h = k.OpenProcess(0x410, False, int(sys.argv[1]))
t, span = int(sys.argv[2], 16), int(sys.argv[3])
def rd(a, n):
    b = ctypes.create_string_buffer(n); g = ctypes.c_size_t()
    ok = k.ReadProcessMemory(h, ctypes.c_void_p(a), b, n, ctypes.byref(g)); return b.raw[:g.value] if ok else b""
for base in range(0x400000, 0x1000000, 0x1000):
    d = rd(base, 0x1000)
    for off in range(0, len(d) - 3, 4):
        v = struct.unpack_from("<I", d, off)[0]
        if t - span <= v <= t:
            vmt = struct.unpack("<I", rd(v, 4) or b"\0\0\0\0")[0]
            print(hex(base + off), "->", hex(v), "x at +", hex(t - v), "vmt", hex(vmt))
