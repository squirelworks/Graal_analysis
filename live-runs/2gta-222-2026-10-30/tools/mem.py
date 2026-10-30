"""Read-only memory reader for the Graal client (ReadProcessMemory only).

mem.py snap PID OUT          -> save candidate doubles (0 < v < 4096, multiple of 1/32)
mem.py filter PID IN OUT OP  -> keep addrs where new value OP old (inc/dec/same/changed)
mem.py show PID IN [N]       -> print addr and current value
mem.py dump PID ADDR LEN     -> hex dump
mem.py watch PID ADDR LEN SECS MS -> log changed dwords in [ADDR, ADDR+LEN)
"""
import ctypes, ctypes.wintypes as wt, struct, sys, pickle, time

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
PROCESS_VM_READ, PROCESS_QUERY_INFORMATION = 0x10, 0x400

class MBI(ctypes.Structure):
    _fields_ = [("BaseAddress", ctypes.c_void_p), ("AllocationBase", ctypes.c_void_p),
                ("AllocationProtect", wt.DWORD), ("PartitionId", wt.WORD), ("RegionSize", ctypes.c_size_t),
                ("State", wt.DWORD), ("Protect", wt.DWORD), ("Type", wt.DWORD)]

def open_proc(pid):
    h = k32.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid)
    if not h:
        raise OSError(ctypes.get_last_error())
    return h

def read(h, addr, n):
    buf = ctypes.create_string_buffer(n)
    got = ctypes.c_size_t()
    if not k32.ReadProcessMemory(h, ctypes.c_void_p(addr), buf, n, ctypes.byref(got)):
        return None
    return buf.raw[:got.value]

def regions(h):
    addr, m = 0, MBI()
    while addr < 0x7FFF0000:
        if not k32.VirtualQueryEx(h, ctypes.c_void_p(addr), ctypes.byref(m), ctypes.sizeof(m)):
            break
        base, size = m.BaseAddress or 0, m.RegionSize
        if m.State == 0x1000 and m.Protect & 0xEE and not m.Protect & 0x100:  # committed, readable/writable, not guard
            yield base, size
        addr = base + size

def snap(h):
    out = {}
    for base, size in regions(h):
        data = read(h, base, size)
        if not data:
            continue
        for off in range(0, len(data) - 7, 4):
            v = struct.unpack_from("<d", data, off)[0]
            if 0.5 < v < 4096 and (v * 32).is_integer():
                out[base + off] = v
    return out

def cur(h, addrs):
    res = {}
    for a in addrs:
        d = read(h, a, 8)
        if d:
            res[a] = struct.unpack("<d", d)[0]
    return res

def main():
    cmd, pid = sys.argv[1], int(sys.argv[2])
    h = open_proc(pid)
    if cmd == "snap":
        s = snap(h); pickle.dump(s, open(sys.argv[3], "wb")); print(len(s))
    elif cmd == "filter":
        old = pickle.load(open(sys.argv[3], "rb")); op = sys.argv[5]
        new = cur(h, old)
        keep = {}
        for a, v in new.items():
            o = old[a]
            if (op == "inc" and v > o) or (op == "dec" and v < o) or (op == "same" and v == o) or (op == "changed" and v != o):
                keep[a] = v
        pickle.dump(keep, open(sys.argv[4], "wb")); print(len(keep))
    elif cmd == "show":
        s = pickle.load(open(sys.argv[3], "rb")); n = int(sys.argv[4]) if len(sys.argv) > 4 else 40
        for a, v in sorted(cur(h, s).items())[:n]:
            print(hex(a), v)
    elif cmd == "dump":
        a, n = int(sys.argv[3], 16), int(sys.argv[4])
        d = read(h, a, n) or b""
        for i in range(0, len(d), 16):
            print(hex(a + i), d[i:i+16].hex(" "))
    elif cmd == "watch":
        a, n, secs, ms = int(sys.argv[3], 16), int(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6])
        prev, t0 = read(h, a, n), time.perf_counter()
        while time.perf_counter() - t0 < secs:
            time.sleep(ms / 1000)
            d = read(h, a, n)
            if d is None:
                continue
            t = time.perf_counter() - t0
            for off in range(0, n, 4):
                if d[off:off+4] != prev[off:off+4]:
                    print(f"{t:8.3f} +0x{off:03X} {prev[off:off+4].hex()} -> {d[off:off+4].hex()}")
            prev = d

main()
