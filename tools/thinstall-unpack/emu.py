#!/usr/bin/env python3
# Thinstall stub/runtime emulator for Graal4Setup.exe. No Graal code is run: we stop on the first
# fetch inside the virtual exe's image range (the region the runtime fills at ImageBase).
# phase 1: run stub until it calls into the runtime (fetch from heap) -> snapshot.
# phase 2: load snapshot, run runtime with API shims; stop when code inside IB image (outside stub text) is fetched.
# usage: emu2.py packed.exe outprefix
import sys, struct, pickle, os, pefile
from unicorn import *
from unicorn.x86_const import *

src, out = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
pe = pefile.PE(data=raw)
IB = pe.OPTIONAL_HEADER.ImageBase
SZ = (pe.OPTIONAL_HEADER.SizeOfImage + 0xfff) & ~0xfff
STUB = (IB + 0x1000, IB + 0x6000)
MB = 1 << 20
API = 7 << 28            # fake API stubs
HEAPBASE = 1 << 29       # bump allocator
HEAPH = 80 * MB          # fake process heap handle
REGS = [UC_X86_REG_EAX, UC_X86_REG_EBX, UC_X86_REG_ECX, UC_X86_REG_EDX, UC_X86_REG_ESI, UC_X86_REG_EDI,
        UC_X86_REG_EBP, UC_X86_REG_ESP, UC_X86_REG_EIP, UC_X86_REG_EFLAGS]
TEB = 0x7ffd << 16
mu = Uc(UC_ARCH_X86, UC_MODE_32)
S = dict(hsz={}, names={}, nxt=API, heap=HEAPBASE, mods={}, fpos=0, implog=[], handles={}, nh=0x100, tls=[0]*64, ntls=0, phase=1)

def sread(a, n):
    out = b''
    while n > 0:
        k = min(n, 0x1000 - (a & 0xfff))
        try: out += bytes(mu.mem_read(a, k))
        except UcError: break
        a += k; n -= k
    return out
def strs(a, n=520):
    return sread(a, n).split(b'\0')[0].decode('latin1') if a else ''
def wstrs(a, n=1040):
    if not a: return ''
    b = sread(a, n); i = 0
    while i + 1 < len(b) and b[i:i+2] != b'\0\0': i += 2
    return b[:i].decode('utf-16le', 'replace')
def w32(a, v): mu.mem_write(a, struct.pack('<I', v & 0xffffffff))
def fake(name):
    a = S['nxt']; S['nxt'] += 16; S['names'][a] = name
    if S['phase'] >= 2: mu.mem_write(a, bytes.fromhex('8bff558bec'))
    return a
def halloc(n):
    if 'hp' not in S or S['hp'] + n + 16 > S['hend']:
        sz = max(0x1000000, (n + 0xffff) & ~0xffff); b = alloc(sz); S['hp'] = b; S['hend'] = b + sz
    p = S['hp']; S['hp'] = (p + n + 31) & ~15; S.setdefault('hsz', {})[p] = n
    mu.mem_write(p, b'\0' * n); return p
def alloc(n, perm=UC_PROT_ALL):
    n = (n + 0xffff) & ~0xffff; a = S['heap']; S['heap'] += n + 0x10000
    mu.mem_map(a, n, perm); return a


def setup_fs():
    GDT = 0x7fff << 16
    try: mu.mem_map(GDT, 0x1000)
    except UcError: pass
    def desc(base, limit, access, flags):
        return struct.pack('<Q', (limit & 0xffff) | ((base & 0xffffff) << 16) | (access << 40) | (((limit >> 16) & 0xf) << 48) | (flags << 52) | (((base >> 24) & 0xff) << 56))
    mu.mem_write(GDT, b'\0' * 8 + desc(0, (1 << 20) - 1, 0x9a, 0xc) + desc(0, (1 << 20) - 1, 0x92, 0xc) + desc(TEB, 0xfff, 0x92, 0x4) + desc(0, (1 << 20) - 1, 0x92 , 0xc))
    mu.reg_write(UC_X86_REG_GDTR, (0, GDT, 0x28, 0))
    mu.reg_write(UC_X86_REG_FS, 3 << 3)
    for r in (UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS, UC_X86_REG_GS): mu.reg_write(r, 2 << 3)

snap = out + '.snap'
if os.path.exists(snap):
    st = pickle.load(open(snap, 'rb'))
    for a, sz, perm, data in st['mem']:
        mu.mem_map(a, sz, perm); mu.mem_write(a, data)
    for r, v in zip(REGS, st['regs']): mu.reg_write(r, v)
    S.update(st['S']); S['phase'] = 2
    setup_fs()
else:
    mu.mem_map(IB, SZ)
    mu.mem_write(IB, raw[:pe.OPTIONAL_HEADER.SizeOfHeaders])
    for s in pe.sections: mu.mem_write(IB + s.VirtualAddress, s.get_data()[:s.SizeOfRawData])
    mu.mem_map(MB, MB)
    mu.mem_map(TEB, 0x10000)
    w32(TEB, 0xffffffff); w32(TEB + 0x18, TEB); w32(TEB + 0x30, TEB + 0x1000); w32(TEB + 0x24, 0x10); w32(TEB + 0x20, 0x8)
    w32(TEB + 4, 2 * MB); w32(TEB + 8, MB)
    w32(TEB + 0x1000 + 8, IB)  # PEB.ImageBaseAddress
    setup_fs()
    mu.mem_map(API, MB); mu.mem_write(API, b'\xc3' * MB)
    for e in pe.DIRECTORY_ENTRY_IMPORT:
        for imp in e.imports:
            w32(imp.address, fake(imp.name.decode() if imp.name else 'ord%d' % imp.ordinal))
    mu.mem_protect(IB, SZ, UC_PROT_READ | UC_PROT_WRITE); mu.mem_protect(STUB[0], STUB[1] - STUB[0], UC_PROT_ALL)
    mu.reg_write(UC_X86_REG_EIP, IB + pe.OPTIONAL_HEADER.AddressOfEntryPoint); mu.reg_write(UC_X86_REG_ESP, 2 * MB - 4096)

import json
ARGTAB = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'argtab.json')))
DEFRET = dict(IsProcessorFeaturePresent=1, SetPriorityClass=1, SetThreadPriority=1, ShowWindow=1, UpdateWindow=1,
              RegisterClassA=0xc001, RegisterClassExA=0xc001, RegisterClassW=0xc001, RegisterClassExW=0xc001,
              SetEvent=1, GetSystemMetrics=1024, GetDC=0x1234, GetDeviceCaps=32, ReleaseDC=1)
CMDLINE = None
def cmdline():
    global CMDLINE
    if CMDLINE is None:
        CMDLINE = alloc(0x1000); mu.mem_write(CMDLINE, b'"C:\\g\\Graal.exe"\0'); mu.mem_write(CMDLINE + 0x100, '"C:\\g\\Graal.exe"\0'.encode('utf-16le'))
    return CMDLINE

def api(n, a, esp):
    """return (retval, nargs) or None to stop"""
    base = n.split('!')[-1]
    D = {}
    if base == 'GetModuleHandleA': return (IB if a[0] == 0 else S['mods'].setdefault(strs(a[0]).lower(), fake('mod:' + strs(a[0]))), 1)
    if base == 'GetModuleHandleW': return (IB if a[0] == 0 else S['mods'].setdefault(wstrs(a[0]).lower(), fake('mod:' + wstrs(a[0]))), 1)
    if base in ('LoadLibraryA', 'LoadLibraryExA'):
        return (S['mods'].setdefault(strs(a[0]).lower(), fake('mod:' + strs(a[0]))), 1 if base == 'LoadLibraryA' else 3)
    if base in ('LoadLibraryW', 'LoadLibraryExW'):
        return (S['mods'].setdefault(wstrs(a[0]).lower(), fake('mod:' + wstrs(a[0]))), 1 if base == 'LoadLibraryW' else 3)
    if base == 'GetProcAddress':
        m = S['names'].get(a[0], 'mod:?')[4:] if a[0] != IB else 'SELF'
        fn = strs(a[1]) if a[1] > 0xffff else 'ord%d' % a[1]
        S['implog'].append((m, fn)); return (fake(m + '!' + fn), 2)
    if base == 'VirtualAlloc':
        if a[0]:
            try: mu.mem_map(a[0] & ~0xfff, (a[1] + (a[0] & 0xfff) + 0xfff) & ~0xfff)
            except UcError: pass
            mu.mem_protect(a[0] & ~0xfff, (a[1] + (a[0] & 0xfff) + 0xfff) & ~0xfff, UC_PROT_ALL if S['phase'] == 1 else UC_PROT_READ | UC_PROT_WRITE) if not (IB <= a[0] < IB + SZ) else None
            return (a[0], 4)
        return (alloc(a[1], UC_PROT_READ | UC_PROT_WRITE if S['phase'] == 1 else UC_PROT_ALL), 4)
    if base in ('GlobalAlloc', 'LocalAlloc'): return (alloc(a[1]), 2)
    if base == 'HeapAlloc': return (halloc(a[2]), 3)
    if base == 'HeapReAlloc':
        n2 = halloc(a[3]); old = S['hsz'].get(a[2], 0); mu.mem_write(n2, bytes(mu.mem_read(a[2], min(a[3], old)))); return (n2, 4)
    if base == 'HeapSize': return (S['hsz'].get(a[2], 0), 3)
    if base == 'HeapCreate': return (HEAPH, 3)
    if base == 'GetProcessHeap': return (HEAPH, 0)
    if base in ('HeapFree', 'HeapDestroy'): return (1, {'HeapFree': 3, 'HeapDestroy': 1}[base])
    if base == 'HeapSize': return (0x10000, 3)
    if base in ('VirtualFree',): return (1, 3)
    if base == 'VirtualProtect':
        if a[3]: w32(a[3], 4)
        return (1, 4)
    if base == 'VirtualQuery':
        mbi = struct.pack('<7I', a[0] & ~0xfff, IB if IB <= a[0] < IB + SZ else a[0] & ~0xfff, 0x40, 0x1000, 0x1000, 0x40, 0x1000000)
        mu.mem_write(a[1], mbi); return (28, 3)
    if base in ('GlobalFree', 'LocalFree'): return (0, 1)
    if base in ('SetLastError',): return (0, 1)
    if base == 'GetLastError': return (0, 0)
    if base == 'GetModuleFileNameA': p = b'C:\\g\\Graal.exe\0'; mu.mem_write(a[1], p); return (len(p) - 1, 3)
    if base == 'GetModuleFileNameW': p = 'C:\\g\\Graal.exe\0'.encode('utf-16le'); mu.mem_write(a[1], p); return (13, 3)
    if base in ('GetEnvironmentVariableA', 'GetEnvironmentVariableW'): return (0, 3)
    if base in ('CreateFileA', 'CreateFileW'):
        nm = strs(a[0]) if base[-1] == 'A' else wstrs(a[0]); S['implog'].append(('CreateFile', nm))
        if nm.lower().endswith('graal.exe'):
            S['nh'] += 4; S['handles'][S['nh']] = 0; return (S['nh'], 7)
        return (0xffffffff, 7)
    if base == 'SetFilePointer':
        h = a[0]; off = a[1]
        if a[2]: off |= struct.unpack('<i', mu.mem_read(a[2], 4))[0] << 32
        cur = S['handles'].get(h, S['fpos'])
        p = {0: off, 1: cur + off, 2: len(raw) + off}[a[3]]
        if h in S['handles']: S['handles'][h] = p
        else: S['fpos'] = p
        return (p, 4)
    if base == 'ReadFile':
        h = a[0]; p = S['handles'].get(h, S['fpos'])
        d = raw[p:p + a[2]]; mu.mem_write(a[1], d); S['implog'].append(('READ', '%x %x -> %x ret %x' % (p, a[2], a[1], struct.unpack('<I', mu.mem_read(esp, 4))[0])))
        if h in S['handles']: S['handles'][h] = p + len(d)
        else: S['fpos'] = p + len(d)
        if a[3]: w32(a[3], len(d))
        return (1, 5)
    if base == 'GetFileSize':
        if a[1]: w32(a[1], 0)
        return (len(raw), 2)
    if base == 'CloseHandle': return (1, 1)
    if base in ('GetVersion',): return ((2600 << 16) | 0x105, 0)
    if base in ('GetVersionExA', 'GetVersionExW'):
        mu.mem_write(a[0] + 4, struct.pack('<4I', 5, 1, 2600, 2)); return (1, 1)
    if base in ('GetCommandLineA',): return (cmdline(), 0)
    if base in ('GetCommandLineW',): return (cmdline() + 0x100, 0)
    if base == 'GetCurrentProcess': return (0xffffffff, 0)
    if base == 'GetCurrentThread': return (0xfffffffe, 0)
    if base in ('GetCurrentProcessId', 'GetCurrentThreadId'): return (0x44, 0)
    if base == 'GetTickCount': return (100000, 0)
    if base == 'TlsAlloc': S['ntls'] += 1; return (S['ntls'], 0)
    if base == 'TlsGetValue': return (S['tls'][a[0]], 1)
    if base == 'TlsSetValue': S['tls'][a[0]] = a[1]; return (1, 2)
    if base in ('InitializeCriticalSection', 'EnterCriticalSection', 'LeaveCriticalSection', 'DeleteCriticalSection'): return (0, 1)
    if base in ('InterlockedIncrement',):
        v = struct.unpack('<I', mu.mem_read(a[0], 4))[0] + 1; w32(a[0], v); return (v, 1)
    if base in ('InterlockedDecrement',):
        v = struct.unpack('<I', mu.mem_read(a[0], 4))[0] - 1; w32(a[0], v); return (v, 1)
    if base in ('GetSystemInfo',):
        mu.mem_write(a[0], struct.pack('<9I', 0, 0x1000, 0x10000, (0x7ffe << 16) | 0xffff, 1, 1, 586, 0x10000, 0)); return (0, 1)
    if base in ('GetSystemDirectoryA', 'GetWindowsDirectoryA'):
        p = b'C:\\WINDOWS\\system32\0' if 'System' in base else b'C:\\WINDOWS\0'; mu.mem_write(a[0], p); return (len(p) - 1, 2)
    if base in ('GetSystemDirectoryW', 'GetWindowsDirectoryW'):
        p = ('C:\\WINDOWS\\system32\0' if 'System' in base else 'C:\\WINDOWS\0'); mu.mem_write(a[0], p.encode('utf-16le')); return (len(p) - 1, 2)
    if base in ('GetFileAttributesA', 'GetFileAttributesW'): return (0xffffffff, 1)
    if base in ('RegOpenKeyExA', 'RegOpenKeyExW', 'RegOpenKeyA', 'RegCreateKeyExA'): return (2, {'RegOpenKeyA': 3, 'RegCreateKeyExA': 9}.get(base, 5))
    if base in ('RegQueryValueExA', 'RegQueryValueExW'): return (2, 6)
    if base in ('RegCloseKey',): return (0, 1)
    if base in ('GetACP',): return (1252, 0)
    if base in ('GetOEMCP',): return (437, 0)
    if base in ('MultiByteToWideChar',):
        s = sread(a[2], 0x4000 if a[3] == 0xffffffff else a[3])
        if a[3] == 0xffffffff: s = s.split(b'\0')[0] + b'\0'
        w = s.decode('latin1').encode('utf-16le')
        if a[5]: mu.mem_write(a[4], w[:a[5] * 2])
        return (len(s), 6)
    if base in ('WideCharToMultiByte',):
        s = sread(a[2], 0x8000 if a[3] == 0xffffffff else a[3] * 2)
        if a[3] == 0xffffffff:
            i = 0
            while i < len(s) and s[i:i+2] != b'\0\0': i += 2
            s = s[:i + 2]
        m = s.decode('utf-16le', 'replace').encode('latin1', 'replace')
        if a[5]: mu.mem_write(a[4], m[:a[5]])
        return (len(m), 8)
    if base in ('lstrlenA',): return (len(strs(a[0], 0x10000)), 1)
    if base in ('lstrlenW',): return (len(wstrs(a[0], 0x10000)), 1)
    if base in ('lstrcpyA',): mu.mem_write(a[0], strs(a[1], 0x10000).encode('latin1') + b'\0'); return (a[0], 2)
    if base in ('lstrcatA',):
        x = strs(a[0], 0x10000) + strs(a[1], 0x10000); mu.mem_write(a[0], x.encode('latin1') + b'\0'); return (a[0], 2)
    if base in ('lstrcmpiA', 'lstrcmpA'):
        x, y = strs(a[0]), strs(a[1])
        if base == 'lstrcmpiA': x, y = x.lower(), y.lower()
        return ((x > y) - (x < y), 2)
    if base in ('GetStartupInfoA', 'GetStartupInfoW'): mu.mem_write(a[0], struct.pack('<I', 68) + b'\0' * 64); return (0, 1)
    if base in ('GetStdHandle',): return (0x10, 1)
    if base in ('SetUnhandledExceptionFilter',): return (0, 1)
    if base in ('FlushInstructionCache',): return (1, 3)
    if base in ('GetCurrentDirectoryA',): p = b'C:\\g\0'; mu.mem_write(a[1], p); return (4, 2)
    if base in ('GetCurrentDirectoryW',): mu.mem_write(a[1], 'C:\\g\0'.encode('utf-16le')); return (4, 2)
    if base in ('IsBadReadPtr', 'IsBadWritePtr', 'IsBadCodePtr'): return (0, 2 if base != 'IsBadCodePtr' else 1)
    if base in ('Sleep',): return (0, 1)
    if base in ('FreeLibrary',): return (1, 1)
    if base in ('DisableThreadLibraryCalls',): return (1, 1)
    if base in ('GetFullPathNameA',):
        p = strs(a[0]);
        if ':' not in p: p = 'C:\\g\\' + p
        mu.mem_write(a[2], p.encode('latin1') + b'\0')
        if a[3]: w32(a[3], a[2] + p.rfind('\\') + 1)
        return (len(p), 4)
    if base in ('GetFullPathNameW',):
        p = wstrs(a[0])
        if ':' not in p: p = 'C:\\g\\' + p
        mu.mem_write(a[2], (p + '\0').encode('utf-16le'))
        if a[3]: w32(a[3], a[2] + 2 * (p.rfind('\\') + 1))
        return (len(p), 4)
    if base in ('CreateMutexA', 'CreateMutexW', 'CreateEventA', 'CreateEventW', 'CreateFileMappingA', 'CreateFileMappingW', 'OpenMutexA'):
        S['nh'] += 4; return (S['nh'], {'CreateMutexA': 3, 'CreateMutexW': 3, 'CreateEventA': 4, 'CreateEventW': 4, 'OpenMutexA': 3}.get(base, 6))
    if base in ('WaitForSingleObject',): return (0, 2)
    if base in ('ReleaseMutex', 'SetEvent', 'ResetEvent'): return (1, 1)
    if base in ('GetLocalTime', 'GetSystemTime'): mu.mem_write(a[0], struct.pack('<8H', 2006, 7, 1, 26, 12, 0, 0, 0)); return (0, 1)
    if base in ('GetSystemTimeAsFileTime',): mu.mem_write(a[0], struct.pack('<Q', 127962000000000000)); return (0, 1)
    if base in ('QueryPerformanceCounter',): mu.mem_write(a[0], struct.pack('<Q', 123456789)); return (1, 1)
    if base in ('GetUserDefaultLCID', 'GetSystemDefaultLCID', 'GetThreadLocale', 'GetUserDefaultLangID', 'GetSystemDefaultLangID'): return (0x409, 0)
    if base in ('GetDriveTypeA', 'GetDriveTypeW'): return (3, 1)
    if base in ('SetErrorMode',): return (0, 1)
    if base in ('OutputDebugStringA', 'OutputDebugStringW'):
        S['implog'].append(('DBG', strs(a[0]) if base[-1] == 'A' else wstrs(a[0]))); return (0, 1)
    if base in ('wsprintfA',): return (0, 0)
    if base in ('GetKeyboardType',): return (4, 1)
    if base == 'GetFileType': return (2, 1)
    if base in ('SetHandleCount',): return (a[0], 1)
    if base in ('GetEnvironmentStrings', 'GetEnvironmentStringsA'):
        e = alloc(0x1000); mu.mem_write(e, b'PATH=C:\\WINDOWS\0\0'); return (e, 0)
    if base in ('GetEnvironmentStringsW',):
        e = alloc(0x1000); mu.mem_write(e, 'PATH=C:\\WINDOWS\0\0'.encode('utf-16le')); return (e, 0)
    if base in ('FreeEnvironmentStringsA', 'FreeEnvironmentStringsW'): return (1, 1)
    if base in ('GetCPInfo',): mu.mem_write(a[1], struct.pack('<I', 1) + b'?\0' + b'\0' * 12); return (1, 2)
    if base in ('GetStringTypeW', 'GetStringTypeA', 'LCMapStringA', 'LCMapStringW'): return (0, {'GetStringTypeW': 4, 'GetStringTypeA': 5, 'LCMapStringA': 6, 'LCMapStringW': 6}[base])
    if base in ('IsDebuggerPresent',): return (0, 0)
    if base in ('SetConsoleCtrlHandler',): return (1, 2)
    if base in ('GetTimeZoneInformation',): return (0, 1)
    if base in ('RtlUnwind',): return (0, 4)
    if base in ('InitializeCriticalSectionAndSpinCount',): return (1, 2)
    if base in ('FlsAlloc',): S['ntls'] += 1; return (S['ntls'], 1)
    if base in ('FlsGetValue',): return (S['tls'][a[0]], 1)
    if base in ('FlsSetValue',): S['tls'][a[0]] = a[1]; return (1, 2)
    if base in ('GetModuleHandleExA', 'GetModuleHandleExW'):
        if a[2]: w32(a[2], IB)
        return (1, 3)
    if base in ('lstrcpynA',):
        x = strs(a[1], 0x10000)[:max(a[2] - 1, 0)]; mu.mem_write(a[0], x.encode('latin1') + b'\0'); return (a[0], 3)
    if base in ('lstrcpyW',): mu.mem_write(a[0], (wstrs(a[1], 0x10000) + '\0').encode('utf-16le')); return (a[0], 2)
    if base in ('lstrcatW',):
        x = wstrs(a[0], 0x10000) + wstrs(a[1], 0x10000); mu.mem_write(a[0], (x + '\0').encode('utf-16le')); return (a[0], 2)
    if base in ('lstrcmpiW', 'lstrcmpW'):
        x, y = wstrs(a[0]), wstrs(a[1])
        if base == 'lstrcmpiW': x, y = x.lower(), y.lower()
        return ((x > y) - (x < y), 2)
    if base in ('CharUpperA', 'CharLowerA', 'CharUpperW', 'CharLowerW'): return (a[0], 1)
    if base in ('GetTempPathA',): p = b'C:\\TEMP\\\0'; mu.mem_write(a[1], p); return (len(p) - 1, 2)
    if base in ('GetTempPathW',): mu.mem_write(a[1], 'C:\\TEMP\\\0'.encode('utf-16le')); return (8, 2)
    if base in ('CreateDirectoryA', 'CreateDirectoryW'): return (1, 2)
    if base in ('FindFirstFileA', 'FindFirstFileW'): return (0xffffffff, 2)
    if base in ('FindClose',): return (1, 1)
    if base in ('GetLongPathNameA', 'GetShortPathNameA'):
        x = strs(a[0]); mu.mem_write(a[1], x.encode('latin1') + b'\0'); return (len(x), 3)
    if base in ('GetLongPathNameW', 'GetShortPathNameW'):
        x = wstrs(a[0]); mu.mem_write(a[1], (x + '\0').encode('utf-16le')); return (len(x), 3)
    if base in ('ExpandEnvironmentStringsA',):
        x = strs(a[0]); mu.mem_write(a[1], x.encode('latin1') + b'\0'); return (len(x) + 1, 3)
    if base in ('ExpandEnvironmentStringsW',):
        x = wstrs(a[0]); mu.mem_write(a[1], (x + '\0').encode('utf-16le')); return (len(x) + 1, 3)
    if base in ('SetEnvironmentVariableA', 'SetEnvironmentVariableW'): return (1, 2)
    if base in ('GetVolumeInformationA', 'GetVolumeInformationW'):
        if a[4]: w32(a[4], 305419896)
        return (1, 8)
    if base in ('MapViewOfFile',): return (alloc(a[4] or MB), 5)
    if base in ('UnmapViewOfFile',): return (1, 1)
    if base in ('DuplicateHandle',):
        if a[3]: w32(a[3], a[1])
        return (1, 7)
    if base in ('SHGetSpecialFolderPathA',): mu.mem_write(a[1], b'C:\\Documents and Settings\\lab\\Application Data\0'); return (1, 4)
    if base in ('SHGetSpecialFolderPathW',): mu.mem_write(a[1], 'C:\\Documents and Settings\\lab\\Application Data\0'.encode('utf-16le')); return (1, 4)
    if base in ('GetUserNameA', 'GetComputerNameA'):
        mu.mem_write(a[0], b'lab\0'); w32(a[1], 3) if a[1] else None; return (1, 2)
    if base in ('GetUserNameW', 'GetComputerNameW'):
        mu.mem_write(a[0], 'lab\0'.encode('utf-16le')); w32(a[1], 3) if a[1] else None; return (1, 2)
    if base in ('GetFileVersionInfoSizeA', 'GetFileVersionInfoSizeW'): return (0, 2)
    if base in ('SetCurrentDirectoryA', 'SetCurrentDirectoryW'): return (1, 1)
    if base in ('FlushFileBuffers', 'SetEndOfFile'): return (1, 1)
    if base in ('GetFileTime',): return (1, 4)
    if base in ('LockResource',): return (a[0], 1)
    if base in ('FindResourceA', 'FindResourceW', 'LoadResource', 'SizeofResource'): return (0, {'LoadResource': 2, 'SizeofResource': 2}.get(base, 3))
    if base in ('GetPrivateProfileStringA',):
        d = strs(a[2]); mu.mem_write(a[3], d.encode('latin1') + b'\0'); return (len(d), 6)
    if base in ('GetPrivateProfileIntA',): return (a[2], 4)
    if base in ('DeleteFileA', 'DeleteFileW'): return (0, 1)
    if base in ('GetFileInformationByHandle',): mu.mem_write(a[1], b'\0' * 52); return (1, 2)
    if base in ('GetFileSizeEx',): mu.mem_write(a[1], struct.pack('<Q', len(raw))); return (1, 2)
    if base in ('SetFilePointerEx',):
        h = a[0]; off = a[1] | (a[2] << 32); cur = S['handles'].get(h, S['fpos'])
        p = {0: off, 1: cur + off, 2: len(raw) + off}[a[4]]
        if h in S['handles']: S['handles'][h] = p
        if a[3]: mu.mem_write(a[3], struct.pack('<Q', p))
        return (1, 5)
    if base == 'WriteProcessMemory':
        mu.mem_write(a[1], sread(a[2], a[3])); S['implog'].append(('WPM', '%x %d %s %s' % (a[1], a[3], sread(a[2], min(a[3], 16)).hex(), S['names'].get(a[1], ''))))
        if a[4]: w32(a[4], a[3])
        return (1, 5)
    if base == 'ReadProcessMemory':
        mu.mem_write(a[2], sread(a[1], a[3]))
        if a[4]: w32(a[4], a[3])
        return (1, 5)
    if base in ARGTAB:
        S['implog'].append(('DEFAULT0', base)); return (DEFRET.get(base, 0), ARGTAB[base])
    return None

stopinfo = {}
PRO = bytes.fromhex('8bff558bec')
def hook_api(uc, addr, size, ud):
    if addr in S['names']:
        if S['phase'] >= 2 and bytes(mu.mem_read(addr, 1)) != b'\x8b': return  # patched by runtime: let the jmp run
        n = S['names'][addr]
    elif (addr - 5) in S['names'] and S['phase'] >= 2:
        n = S['names'][addr - 5]
        esp = mu.reg_read(UC_X86_REG_ESP); mu.reg_write(UC_X86_REG_EBP, struct.unpack('<I', mu.mem_read(esp, 4))[0]); mu.reg_write(UC_X86_REG_ESP, esp + 4)
        S['implog'].append(('ORIG', n))
    else: return
    esp = mu.reg_read(UC_X86_REG_ESP)
    a = struct.unpack('<10I', mu.mem_read(esp + 4, 40))
    r = api(n, a, esp)
    if r is None or n.split('!')[-1] in ('ExitProcess', 'MessageBoxA', 'MessageBoxW', 'TerminateProcess', 'FatalAppExitA'):
        stopinfo['api'] = n; stopinfo['args'] = [hex(x) for x in a[:6]]
        try: stopinfo['s0'] = [strs(x, 200) for x in a[:3] if x > 0x10000]
        except Exception: pass
        uc.emu_stop(); return
    ret = struct.unpack('<I', mu.mem_read(esp, 4))[0]
    mu.reg_write(UC_X86_REG_EAX, r[0] & 0xffffffff)
    mu.reg_write(UC_X86_REG_ESP, esp + 4 + 4 * r[1]); mu.reg_write(UC_X86_REG_EIP, ret)
    if os.environ.get('TRACE') : print('API', n, [hex(x) for x in a[:4]], '->', hex(r[0] & 0xffffffff))
mu.hook_add(UC_HOOK_CODE, hook_api, begin=API, end=API + MB)

hits = []
def hook_bad(uc, acc, addr, size, val, ud):
    hits.append((acc, addr)); return False
mu.hook_add(UC_HOOK_MEM_INVALID | UC_HOOK_MEM_FETCH_PROT, hook_bad)

if S['phase'] == 2:
    PEB = TEB + 0x1000; LDR = TEB + 0x2000; ENT = TEB + 0x2100; NM = TEB + 0x2400
    if not S.get('pro'):
        for a0 in S['names']: mu.mem_write(a0, PRO)
        S['pro'] = 1
    w32(PEB + 0xc, LDR); w32(PEB + 8, IB); w32(PEB + 0x18, HEAPH)
    w32(LDR, 0x28); w32(LDR + 4, 1)
    for off in (0, 8, 0x10):
        w32(LDR + 0xc + off, ENT + off); w32(LDR + 0x10 + off, ENT + off)
        w32(ENT + off, LDR + 0xc + off); w32(ENT + off + 4, LDR + 0xc + off)
    w32(ENT + 0x18, IB); w32(ENT + 0x1c, IB + pe.OPTIONAL_HEADER.AddressOfEntryPoint); w32(ENT + 0x20, SZ)
    fn = 'C:\\g\\Graal.exe'.encode('utf-16le'); mu.mem_write(NM, fn + b'\0\0')
    mu.mem_write(ENT + 0x24, struct.pack('<HHI', len(fn), len(fn) + 2, NM)); mu.mem_write(ENT + 0x2c, struct.pack('<HHI', 18, 20, NM + 10))
    # everything outside IB image runs; IB image (except stub) non-exec -> stop on virtual exe entry
    for r0, r1, perm in list(mu.mem_regions()):
        if r0 >= HEAPBASE and r0 < API: mu.mem_protect(r0, r1 - r0 + 1, UC_PROT_ALL)
    mu.mem_protect(IB, SZ, UC_PROT_READ | UC_PROT_WRITE); mu.mem_protect(STUB[0], STUB[1] - STUB[0], UC_PROT_ALL)

eip = mu.reg_read(UC_X86_REG_EIP)
try:
    mu.emu_start(eip, 0, count=int(os.environ.get('COUNT', '4000000000')))
except UcError as e:
    print('err', e)
eip = mu.reg_read(UC_X86_REG_EIP)
print('lastapi', S['names'].get(mu.reg_read(UC_X86_REG_EIP)), 'phase', S['phase'], 'eip', hex(eip), 'hits', [(x, hex(y)) for x, y in hits[-3:]], 'stop', stopinfo)
if hits and hits[-1][0] == UC_MEM_FETCH_PROT and S['phase'] in (1, 2):
    if S['phase'] == 2: snap = out + '.snap3'
    mem = [(r0, r1 - r0 + 1, perm, bytes(mu.mem_read(r0, r1 - r0 + 1))) for r0, r1, perm in mu.mem_regions()]
    mu.reg_write(UC_X86_REG_EIP, hits[-1][1])
    pickle.dump(dict(mem=mem, regs=[mu.reg_read(r) for r in REGS], S=S), open(snap, 'wb'))
    print('snapshot saved')
    open(out + '.log', 'w').write('\n'.join('%s!%s' % x for x in S['implog']))
else:
    open(out + '.img', 'wb').write(bytes(mu.mem_read(IB, SZ)))
    open(out + '.log', 'w').write('\n'.join('%s!%s' % x for x in S['implog']))
    for r0, r1, perm in mu.mem_regions():
        if HEAPBASE <= r0 < API and r1 - r0 > MB:
            open(out + '.heap_%08x' % r0, 'wb').write(bytes(mu.mem_read(r0, r1 - r0 + 1)))
