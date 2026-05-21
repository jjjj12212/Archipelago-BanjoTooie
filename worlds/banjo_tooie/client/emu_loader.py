"""Direct-emulator-memory loader for Banjo-Tooie.
Heavily based on JXJacob's GST autotracking code.

Per-emulator attach strategies, RDRAM endian handling, the Linux ptrace
helper, and the cross-platform ProcessMemory abstraction were ported with
permission from the DK64 Randomizer (https://github.com/2dos/DK64-Randomizer)
emu_loader, Copyright (c) DK64 Randomizer Dev Team, MIT-licensed. Many
thanks to the DK64 team.

Authors:
- Killklli
- Ballaam
- Green Bean
- Umed
- JXJacob
"""

from __future__ import annotations

import ctypes
import glob
import logging
import os
import platform
import subprocess
from enum import IntEnum, auto
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    from CommonClient import logger
except ImportError:
    logger = logging.getLogger(__name__)


IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"


# Windows API surface (only used when IS_WINDOWS).
if IS_WINDOWS:
    import ctypes.wintypes

    PROCESS_VM_READ = 0x0010
    PROCESS_VM_WRITE = 0x0020
    PROCESS_VM_OPERATION = 0x0008
    PROCESS_QUERY_INFORMATION = 0x0400
    TH32CS_SNAPMODULE = 0x00000008
    TH32CS_SNAPMODULE32 = 0x00000010
    TH32CS_SNAPPROCESS = 0x00000002
    MAX_PATH = 260

    MEM_COMMIT = 0x1000
    MEM_PRIVATE = 0x20000
    PAGE_NOACCESS = 0x01
    PAGE_READWRITE = 0x04
    PAGE_EXECUTE_READWRITE = 0x40
    PAGE_GUARD = 0x100

    class MODULEENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize", ctypes.wintypes.DWORD),
            ("th32ModuleID", ctypes.wintypes.DWORD),
            ("th32ProcessID", ctypes.wintypes.DWORD),
            ("GlblcntUsage", ctypes.wintypes.DWORD),
            ("ProccntUsage", ctypes.wintypes.DWORD),
            ("modBaseAddr", ctypes.POINTER(ctypes.wintypes.BYTE)),
            ("modBaseSize", ctypes.wintypes.DWORD),
            ("hModule", ctypes.wintypes.HMODULE),
            ("szModule", ctypes.c_char * 256),
            ("szExePath", ctypes.c_char * 260),
        ]

    class PROCESSENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize", ctypes.wintypes.DWORD),
            ("cntUsage", ctypes.wintypes.DWORD),
            ("th32ProcessID", ctypes.wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.POINTER(ctypes.wintypes.ULONG)),
            ("th32ModuleID", ctypes.wintypes.DWORD),
            ("cntThreads", ctypes.wintypes.DWORD),
            ("th32ParentProcessID", ctypes.wintypes.DWORD),
            ("pcPriClassBase", ctypes.wintypes.LONG),
            ("dwFlags", ctypes.wintypes.DWORD),
            ("szExeFile", ctypes.c_char * MAX_PATH),
        ]

    class MEMORY_BASIC_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BaseAddress", ctypes.c_void_p),
            ("AllocationBase", ctypes.c_void_p),
            ("AllocationProtect", ctypes.wintypes.DWORD),
            ("RegionSize", ctypes.c_size_t),
            ("State", ctypes.wintypes.DWORD),
            ("Protect", ctypes.wintypes.DWORD),
            ("Type", ctypes.wintypes.DWORD),
        ]


# Linux ptrace handling
def check_and_fix_ptrace_scope() -> bool:
    """Ensure /proc/<pid>/mem is openable from this process. Returns True on
    success. On restrictive systems, prompts for sudo to set ptrace_scope=0."""
    if not IS_LINUX:
        return True
    ptrace_scope_path = "/proc/sys/kernel/yama/ptrace_scope"
    if not os.path.exists(ptrace_scope_path):
        return True
    try:
        with open(ptrace_scope_path, "r") as f:
            scope = int(f.read().strip())
        if scope == 0:
            return True
        logger.info(
            f"Detected restrictive ptrace scope ({scope}). Attempting to enable memory access..."
        )
        logger.info("You may be prompted for your sudo password.")
        try:
            # tee writes to the protected file; redirect its stdout so the
            # echoed value doesn't leak into our own logs.
            result = subprocess.run(
                ["sudo", "tee", ptrace_scope_path],
                input=b"0\n",
                timeout=30,
                stdout=subprocess.DEVNULL,
            )
            if result.returncode == 0:
                logger.info("Successfully enabled ptrace access.")
                return True
            logger.warning(
                f"Failed to set ptrace scope. Run manually: echo 0 | sudo tee {ptrace_scope_path}"
            )
            return False
        except subprocess.TimeoutExpired:
            logger.warning("Sudo prompt timed out.")
            return False
        except Exception as e:
            logger.warning(f"Failed to set ptrace scope: {e}")
            return False
    except Exception as e:
        logger.warning(f"Could not check ptrace scope: {e}")
        return True


# Process enumeration
def get_windows_processes() -> List[Dict[str, Any]]:
    processes: List[Dict[str, Any]] = []
    snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snapshot == -1:
        return processes
    try:
        pe32 = PROCESSENTRY32()
        pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
        if ctypes.windll.kernel32.Process32First(snapshot, ctypes.byref(pe32)):
            while True:
                try:
                    processes.append(
                        {
                            "name": pe32.szExeFile.decode("utf-8"),
                            "pid": pe32.th32ProcessID,
                        }
                    )
                except UnicodeDecodeError:
                    pass
                if not ctypes.windll.kernel32.Process32Next(
                    snapshot, ctypes.byref(pe32)
                ):
                    break
    finally:
        ctypes.windll.kernel32.CloseHandle(snapshot)
    return processes


def get_linux_processes() -> List[Dict[str, Any]]:
    processes: List[Dict[str, Any]] = []
    try:
        for pid_dir in glob.glob("/proc/[0-9]*"):
            try:
                pid = int(os.path.basename(pid_dir))
                comm_path = os.path.join(pid_dir, "comm")
                if os.path.exists(comm_path):
                    with open(comm_path, "r") as f:
                        processes.append({"name": f.read().strip(), "pid": pid})
            except (ValueError, OSError, IOError):
                continue
    except OSError:
        pass
    return processes


def get_running_processes() -> List[Dict[str, Any]]:
    if IS_WINDOWS:
        return get_windows_processes()
    if IS_LINUX:
        return get_linux_processes()
    return []


# Process memory access
class ModuleInfo:
    def __init__(self, name: str, base: Optional[int]):
        self.name = name
        self.lpBaseOfDll = base


class ProcessMemory:
    """Read/write the address space of another process."""

    def __init__(self, process_name: str, pid: Optional[int] = None):
        self.process_name = process_name
        self.process_id: Optional[int] = None
        self.process_handle = None
        self.mem_fd: Optional[int] = None
        self.attach(pid)

    def attach(self, target_pid: Optional[int]) -> None:
        for proc in get_running_processes():
            if target_pid is not None:
                if proc["pid"] != target_pid:
                    continue
            else:
                if not proc["name"] or not proc["name"].lower().startswith(
                    self.process_name.lower()
                ):
                    continue

            self.process_id = proc["pid"]
            if IS_WINDOWS:
                self.process_handle = ctypes.windll.kernel32.OpenProcess(
                    PROCESS_VM_READ
                    | PROCESS_VM_WRITE
                    | PROCESS_VM_OPERATION
                    | PROCESS_QUERY_INFORMATION,
                    False,
                    self.process_id,
                )
                if not self.process_handle:
                    raise RuntimeError(f"OpenProcess failed for {self.process_name}")
            elif IS_LINUX:
                check_and_fix_ptrace_scope()
                try:
                    self.mem_fd = os.open(f"/proc/{self.process_id}/mem", os.O_RDWR)
                except (OSError, IOError) as e:
                    if e.errno in (1, 13) and check_and_fix_ptrace_scope():
                        self.mem_fd = os.open(f"/proc/{self.process_id}/mem", os.O_RDWR)
                    else:
                        raise RuntimeError(
                            f"open /proc/{self.process_id}/mem failed: {e}"
                        )
            return
        raise RuntimeError(f"Process {self.process_name} not found")

    def close(self) -> None:
        if IS_WINDOWS and self.process_handle:
            ctypes.windll.kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
        elif IS_LINUX and self.mem_fd is not None:
            os.close(self.mem_fd)
            self.mem_fd = None

    # ----- modules -----

    def list_modules(self) -> List[ModuleInfo]:
        if IS_WINDOWS:
            return self.modules_windows()
        if IS_LINUX:
            return self.modules_linux()
        return []

    def modules_windows(self) -> List[ModuleInfo]:
        modules: List[ModuleInfo] = []
        if not self.process_handle or not self.process_id:
            return modules
        snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(
            TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, self.process_id
        )
        if snapshot == -1:
            return modules
        try:
            me32 = MODULEENTRY32()
            me32.dwSize = ctypes.sizeof(MODULEENTRY32)
            if ctypes.windll.kernel32.Module32First(snapshot, ctypes.byref(me32)):
                while True:
                    modules.append(
                        ModuleInfo(
                            name=me32.szModule.decode("utf-8"),
                            base=ctypes.cast(me32.modBaseAddr, ctypes.c_void_p).value,
                        )
                    )
                    if not ctypes.windll.kernel32.Module32Next(
                        snapshot, ctypes.byref(me32)
                    ):
                        break
        finally:
            ctypes.windll.kernel32.CloseHandle(snapshot)
        return modules

    def modules_linux(self) -> List[ModuleInfo]:
        modules: List[ModuleInfo] = []
        if not self.process_id:
            return modules
        try:
            with open(f"/proc/{self.process_id}/maps", "r") as f:
                seen: Set[str] = set()
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 6:
                        continue
                    address_range, perms = parts[0], parts[1]
                    pathname = parts[5]
                    if "x" not in perms or not pathname or pathname.startswith("["):
                        continue
                    name = os.path.basename(pathname)
                    if name in seen:
                        continue
                    seen.add(name)
                    start = int(address_range.split("-")[0], 16)
                    modules.append(ModuleInfo(name=name, base=start))
        except (OSError, IOError):
            pass
        return modules

    # ----- writable regions (for signature-scan emulators) -----

    def list_writable_regions(self, min_size: int = 0x800000) -> List[Tuple[int, int]]:
        if IS_WINDOWS:
            return self.writable_regions_windows(min_size)
        if IS_LINUX:
            return self.writable_regions_linux(min_size)
        return []

    def writable_regions_linux(self, min_size: int) -> List[Tuple[int, int]]:
        regions: List[Tuple[int, int]] = []
        if not self.process_id:
            return regions
        try:
            with open(f"/proc/{self.process_id}/maps", "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        continue
                    address_range, perms = parts[0], parts[1]
                    pathname = parts[5] if len(parts) > 5 else ""
                    if "r" not in perms or "w" not in perms:
                        continue
                    if (
                        pathname
                        and pathname != "[heap]"
                        and not pathname.startswith("[anon")
                    ):
                        continue
                    try:
                        start_str, end_str = address_range.split("-")
                        start, end = int(start_str, 16), int(end_str, 16)
                    except ValueError:
                        continue
                    if end - start >= min_size:
                        regions.append((start, end - start))
        except (OSError, IOError):
            pass
        return regions

    def writable_regions_windows(self, min_size: int) -> List[Tuple[int, int]]:
        regions: List[Tuple[int, int]] = []
        if not self.process_handle:
            return regions
        VirtualQueryEx = ctypes.windll.kernel32.VirtualQueryEx
        VirtualQueryEx.argtypes = [
            ctypes.wintypes.HANDLE,
            ctypes.c_void_p,
            ctypes.POINTER(MEMORY_BASIC_INFORMATION),
            ctypes.c_size_t,
        ]
        VirtualQueryEx.restype = ctypes.c_size_t

        mbi = MEMORY_BASIC_INFORMATION()
        mbi_size = ctypes.sizeof(MEMORY_BASIC_INFORMATION)
        max_address = (
            0x7FFFFFFFFFFF if ctypes.sizeof(ctypes.c_void_p) == 8 else 0x7FFFFFFF
        )
        writable_mask = PAGE_READWRITE | PAGE_EXECUTE_READWRITE

        address = 0
        while address < max_address:
            if (
                VirtualQueryEx(
                    self.process_handle,
                    ctypes.c_void_p(address),
                    ctypes.byref(mbi),
                    mbi_size,
                )
                == 0
            ):
                break
            base = mbi.BaseAddress or 0
            size = mbi.RegionSize
            if size == 0:
                break
            protect = mbi.Protect
            if (
                mbi.State == MEM_COMMIT
                and mbi.Type == MEM_PRIVATE
                and not (protect & PAGE_GUARD)
                and not (protect & PAGE_NOACCESS)
                and (protect & writable_mask)
                and size >= min_size
            ):
                regions.append((base, size))
            address = base + size
        return regions

    # ----- bytes I/O -----

    def read_bytes(self, address: int, size: int) -> bytes:
        if IS_WINDOWS:
            if not self.process_handle:
                raise RuntimeError("Not attached")
            buf = ctypes.create_string_buffer(size)
            read = ctypes.wintypes.DWORD(0)
            ok = ctypes.windll.kernel32.ReadProcessMemory(
                self.process_handle,
                ctypes.c_void_p(address),
                buf,
                size,
                ctypes.byref(read),
            )
            if not ok:
                raise RuntimeError(f"ReadProcessMemory failed at 0x{address:x}")
            return buf.raw[: read.value]
        if IS_LINUX:
            if self.mem_fd is None:
                raise RuntimeError("Not attached")
            data = os.pread(self.mem_fd, size, address)
            if len(data) != size:
                raise RuntimeError(
                    f"short read at 0x{address:x}: got {len(data)}/{size}"
                )
            return data
        raise RuntimeError("Unsupported OS")

    def write_bytes(self, address: int, data: bytes) -> None:
        size = len(data)
        if IS_WINDOWS:
            if not self.process_handle:
                raise RuntimeError("Not attached")
            written = ctypes.wintypes.DWORD(0)
            ok = ctypes.windll.kernel32.WriteProcessMemory(
                self.process_handle,
                ctypes.c_void_p(address),
                data,
                size,
                ctypes.byref(written),
            )
            if not ok:
                err = ctypes.windll.kernel32.GetLastError()
                raise RuntimeError(
                    f"WriteProcessMemory failed at 0x{address:x} (err {err})"
                )
            return
        if IS_LINUX:
            if self.mem_fd is None:
                raise RuntimeError("Not attached")
            written = os.pwrite(self.mem_fd, data, address)
            if written != size:
                raise RuntimeError(f"short write at 0x{address:x}: {written}/{size}")
            return
        raise RuntimeError("Unsupported OS")

    def read_int(self, address: int) -> int:
        return int.from_bytes(self.read_bytes(address, 4), "little")

    def read_longlong(self, address: int) -> int:
        return int.from_bytes(self.read_bytes(address, 8), "little")


# BTHACK signature validation
RDRAM_BASE = 0x80000000  # KSEG0 start; RDRAM mirror
RDRAM_SIZE = 0x800000  # 8 MB with expansion pak (required by BT)
BTHACK_ANCHOR_OFFSET = 0x400000  # physical RDRAM offset of AP_MEMORY_PTR
BTHACK_STRUCT_SIZE = 52
BTHACK_SUB_POINTER_OFFSETS = (
    0x04,  # pc
    0x08,  # pc_message
    0x0C,  # signpost_messages
    0x10,  # pc_settings
    0x14,  # pc_items
    0x18,  # pc_traps
    0x1C,  # pc_exit_map
    0x20,  # n64
    0x24,  # n64_saves_real
    0x28,  # n64_saves_fake
    0x2C,  # n64_saves_nests
    0x30,  # n64_saves_signposts
)


def is_rdram_pointer(value: int) -> bool:
    return RDRAM_BASE <= value < RDRAM_BASE + RDRAM_SIZE


def validate_bt_signature(pm: ProcessMemory, rdram_base: int) -> bool:
    """Return True if ``rdram_base`` looks like AP-Banjo-Tooie RDRAM.

    - u32 at ``rdram_base + 0x400000`` must be a valid 0x80xxxxxx pointer
      (BTHACK's ``AP_MEMORY_PTR``).
    - At the dereferenced ``ap_memory_ptr_t`` struct, all 12 sub-pointers
      at offsets 0x04..0x30 must themselves be valid RDRAM pointers. The
      patch's ``inject_hooks()`` populates every one of them at game boot.
    """
    try:
        anchor = int.from_bytes(
            pm.read_bytes(rdram_base + BTHACK_ANCHOR_OFFSET, 4), "little"
        )
    except Exception:
        return False
    if not is_rdram_pointer(anchor):
        return False
    physical = anchor & 0x7FFFFFFF
    if physical + BTHACK_STRUCT_SIZE > RDRAM_SIZE:
        return False
    try:
        struct_bytes = pm.read_bytes(rdram_base + physical, BTHACK_STRUCT_SIZE)
    except Exception:
        return False
    for offset in BTHACK_SUB_POINTER_OFFSETS:
        sub_ptr = int.from_bytes(struct_bytes[offset : offset + 4], "little")
        if not is_rdram_pointer(sub_ptr):
            return False
    return True


# Per-emulator detection
class Emulators(IntEnum):
    Project64_v4 = auto()
    Project64 = auto()
    BizHawk = auto()
    RMG = auto()
    RMG_Flatpak
    Simple64 = auto()
    ParallelLauncher903 = auto()
    ParallelLauncher = auto()
    RetroArch = auto()
    Gopher64 = auto()
    Ares = auto()


class EmulatorInfo:
    """Detection rules and attached state for one emulator."""

    def __init__(
        self,
        emu_id: Emulators,
        readable_name: str,
        process_name: str,
        find_dll: bool,
        dll_name: Optional[str],
        additional_lookup: bool,
        lower_offset_range: int,
        upper_offset_range: int,
        range_step: int = 16,
        extra_offset: int = 0,
        linux_dll_name: Optional[str] = None,
        scan_memory_for_signature: bool = False,
        signature_alignment: int = 0x10000,
    ):
        self.id = emu_id
        self.readable_name = readable_name
        self.process_name = process_name
        self.find_dll = find_dll
        self.dll_name = dll_name
        self.linux_dll_name = linux_dll_name
        self.additional_lookup = additional_lookup
        self.lower_offset_range = lower_offset_range
        self.upper_offset_range = upper_offset_range
        self.range_step = range_step
        self.extra_offset = extra_offset
        self.scan_memory_for_signature = scan_memory_for_signature
        self.signature_alignment = signature_alignment

        self.connected_process: Optional[ProcessMemory] = None
        self.connected_offset: Optional[int] = None
        self.connection_error: Optional[str] = None

    def library_names(self) -> List[str]:
        names: List[str] = []
        if IS_LINUX and self.linux_dll_name:
            names.append(self.linux_dll_name)
        elif self.dll_name:
            names.append(self.dll_name)
        if IS_LINUX and self.dll_name:
            if self.dll_name.endswith(".dll"):
                so = self.dll_name[:-4] + ".so"
                if so not in names:
                    names.append(so)
            if not self.dll_name.startswith("lib"):
                lib = "lib" + self.dll_name
                if lib not in names:
                    names.append(lib)
                if lib.endswith(".dll"):
                    libso = lib[:-4] + ".so"
                    if libso not in names:
                        names.append(libso)
        return [n for n in names if n]

    def disconnect(self) -> None:
        if self.connected_process:
            self.connected_process.close()
        self.connected_process = None
        self.connected_offset = None

    def set_error(self, msg: str) -> None:
        self.connection_error = msg
        logger.debug(f"[{self.readable_name}] {msg}")

    def scan_writable_for_signature(self, pm: ProcessMemory) -> Optional[int]:
        for region_start, region_size in pm.list_writable_regions():
            max_base = region_size - BTHACK_ANCHOR_OFFSET - BTHACK_STRUCT_SIZE
            if max_base < 0:
                continue
            for base in range(0, max_base + 1, self.signature_alignment):
                candidate = region_start + base
                if validate_bt_signature(pm, candidate):
                    return candidate
        return None

    def attach(self) -> bool:
        self.disconnect()
        self.connection_error = None

        procs = [
            p
            for p in get_running_processes()
            if p["name"] and p["name"].lower().startswith(self.process_name.lower())
        ]
        if not procs:
            self.set_error(f"Process '{self.process_name}' not running")
            return False

        # Signature-scan path. Multiple processes may share a name
        # (parent + child); try each until one yields the BT signature.
        if self.scan_memory_for_signature:
            last_err: Optional[str] = None
            for proc in procs:
                try:
                    pm = ProcessMemory(self.process_name, pid=proc["pid"])
                except Exception as e:
                    last_err = f"attach pid {proc['pid']} failed: {e}"
                    continue
                base = self.scan_writable_for_signature(pm)
                if base is None:
                    pm.close()
                    continue
                self.connected_process = pm
                self.connected_offset = base
                return True
            self.set_error(last_err or "BT signature not found in any heap region")
            return False

        # Module + offset-range path.
        try:
            pm = ProcessMemory(procs[0]["name"])
        except Exception as e:
            self.set_error(f"attach failed: {e}")
            return False

        dll_base = 0
        if self.find_dll:
            wanted = [n.lower() for n in self.library_names()]
            for mod in pm.list_modules():
                if mod.name.lower() in wanted and mod.lpBaseOfDll:
                    dll_base = mod.lpBaseOfDll
                    break
            if dll_base == 0 and self.id == Emulators.BizHawk:
                # Fallback used by other Mupen-family loaders when module
                # enumeration returns nothing.
                dll_base = 2024407040
            elif dll_base == 0:
                pm.close()
                self.set_error(f"Module {self.library_names()} not loaded")
                return False

        saw_any_data = False
        for off in range(
            self.lower_offset_range, self.upper_offset_range, self.range_step
        ):
            if self.additional_lookup:
                try:
                    candidate = pm.read_longlong(dll_base + off)
                except Exception:
                    continue
                if candidate == 0:
                    continue
                saw_any_data = True
                rdram_base = candidate + self.extra_offset
            else:
                rdram_base = dll_base + off + self.extra_offset
                saw_any_data = True

            if validate_bt_signature(pm, rdram_base):
                self.connected_process = pm
                self.connected_offset = rdram_base
                return True

        pm.close()
        if not saw_any_data:
            self.set_error(f"Could not read any data from {self.readable_name}")
        else:
            self.set_error(
                f"BT signature not found in {self.readable_name} (is the ROM patched and loaded?)"
            )
        return False

    # Apply N64 address fixing based on size
    @staticmethod
    def u8_addr(addr: int) -> int:
        r = addr % 4
        if r == 0:
            return addr + 3
        if r == 1:
            return addr + 1
        if r == 2:
            return addr - 1
        return addr - 3

    @staticmethod
    def u16_addr(addr: int) -> int:
        r = addr % 4
        if r in (2, 3):
            return addr - 2
        return addr + 2

    def resolve(self, address: int, size: int) -> int:
        if address & 0x80000000:
            address &= 0x7FFFFFFF
        if size == 1:
            address = self.u8_addr(address)
        elif size == 2:
            address = self.u16_addr(address)
        return self.connected_offset + address  # type: ignore[operator]

    def require_attached(self) -> None:
        if self.connected_process is None or self.connected_offset is None:
            raise RuntimeError("Not attached to an emulator")

    def read_u8(self, address: int) -> int:
        self.require_attached()
        return int.from_bytes(self.connected_process.read_bytes(self.resolve(address, 1), 1), "little")  # type: ignore[union-attr]

    def read_u16(self, address: int) -> int:
        self.require_attached()
        return int.from_bytes(self.connected_process.read_bytes(self.resolve(address, 2), 2), "little")  # type: ignore[union-attr]

    def read_u32(self, address: int) -> int:
        self.require_attached()
        return int.from_bytes(self.connected_process.read_bytes(self.resolve(address, 4), 4), "little")  # type: ignore[union-attr]

    def write_u8(self, address: int, value: int) -> None:
        self.require_attached()
        self.connected_process.write_bytes(self.resolve(address, 1), (value & 0xFF).to_bytes(1, "little"))  # type: ignore[union-attr]

    def write_u16(self, address: int, value: int) -> None:
        self.require_attached()
        self.connected_process.write_bytes(self.resolve(address, 2), (value & 0xFFFF).to_bytes(2, "little"))  # type: ignore[union-attr]

    def write_u32(self, address: int, value: int) -> None:
        self.require_attached()
        self.connected_process.write_bytes(self.resolve(address, 4), (value & 0xFFFFFFFF).to_bytes(4, "little"))  # type: ignore[union-attr]


# Emulator catalog
EMULATOR_CONFIGS: Dict[Emulators, EmulatorInfo] = {
    Emulators.Project64_v4: EmulatorInfo(
        Emulators.Project64_v4,
        "Project64 4.0",
        "project64",
        find_dll=False,
        dll_name=None,
        additional_lookup=False,
        scan_memory_for_signature=True,
        lower_offset_range=0xFDD00000,
        upper_offset_range=0xFE1FFFFF,
    ),
    Emulators.BizHawk: EmulatorInfo(
        Emulators.BizHawk,
        "BizHawk",
        "emuhawk",
        find_dll=True,
        dll_name="mupen64plus.dll",
        additional_lookup=False,
        lower_offset_range=0x5A000,
        upper_offset_range=0x5658DF,
        linux_dll_name="libmupen64plus.so",
    ),
    Emulators.RMG: EmulatorInfo(
        Emulators.RMG,
        "Rosalie's Mupen GUI",
        "rmg",
        find_dll=True,
        dll_name="mupen64plus.dll",
        additional_lookup=True,
        lower_offset_range=0x29C15D8,
        upper_offset_range=0x2FC15D8,
        extra_offset=0x80000000,
        linux_dll_name="libmupen64plus.so",
    ),
    Emulators.RMG_Flatpak: EmulatorInfo(
        Emulators.RMG_Flatpak,
        "Rosalie's Mupen GUI (Flatpak)",
        "rmg",
        find_dll=True,
        additional_lookup=True,
        lower_offset_range=0x0,
        upper_offset_range=0x60000,
        range_step=8,
        extra_offset=0,
        linux_dll_name="libmupen64plus.so",
    ),
    Emulators.Simple64: EmulatorInfo(
        Emulators.Simple64,
        "simple64",
        "simple64-gui",
        find_dll=True,
        dll_name="libmupen64plus.dll",
        additional_lookup=True,
        lower_offset_range=0x1380000,
        upper_offset_range=0x29C95D8,
        linux_dll_name="libmupen64plus.so",
    ),
    Emulators.ParallelLauncher903: EmulatorInfo(
        Emulators.ParallelLauncher903,
        "Parallel Launcher (9.0.3+)",
        "retroarch",
        find_dll=True,
        dll_name="parallel_n64_next_libretro.dll",
        additional_lookup=True,
        lower_offset_range=0x1400000,
        upper_offset_range=0x1800000,
        linux_dll_name="parallel_n64_next_libretro.so",
    ),
    Emulators.ParallelLauncher: EmulatorInfo(
        Emulators.ParallelLauncher,
        "Parallel Launcher",
        "retroarch",
        find_dll=True,
        dll_name="parallel_n64_next_libretro.dll",
        additional_lookup=True,
        lower_offset_range=0x845000,
        upper_offset_range=0xD56000,
        linux_dll_name="parallel_n64_next_libretro.so",
    ),
    Emulators.RetroArch: EmulatorInfo(
        Emulators.RetroArch,
        "RetroArch (Mupen64Plus-Next)",
        "retroarch",
        find_dll=True,
        dll_name="mupen64plus_next_libretro.dll",
        additional_lookup=True,
        lower_offset_range=0,
        upper_offset_range=0xFFFFFF,
        range_step=4,
        linux_dll_name="mupen64plus_next_libretro.so",
    ),
    Emulators.Project64: EmulatorInfo(
        Emulators.Project64,
        "Project64",
        "project64",
        find_dll=False,
        dll_name=None,
        additional_lookup=False,
        scan_memory_for_signature=True,
        lower_offset_range=0xDFD00000,
        upper_offset_range=0xE01FFFFF,
    ),
    Emulators.Gopher64: EmulatorInfo(
        Emulators.Gopher64,
        "Gopher64",
        "gopher64",
        find_dll=False,
        dll_name=None,
        additional_lookup=False,
        lower_offset_range=0,
        upper_offset_range=0,
        scan_memory_for_signature=True,
        signature_alignment=0x10000,
    ),
    Emulators.Ares: EmulatorInfo(
        Emulators.Ares,
        "ares",
        "ares",
        find_dll=False,
        dll_name=None,
        additional_lookup=False,
        lower_offset_range=0,
        upper_offset_range=0,
        scan_memory_for_signature=True,
        signature_alignment=0x1000,
    ),
}


def connect_to_any_emulator() -> Optional[EmulatorInfo]:
    """Try each known emulator in turn; return the first that attaches."""
    for emu in Emulators:
        info = EMULATOR_CONFIGS[emu]
        try:
            if info.attach():
                logger.info(f"Connected to {info.readable_name}")
                return info
        except Exception as e:
            logger.debug(f"[{info.readable_name}] attach raised: {e}")
            continue
    return None


# High-level client surface used by BTClient.py
class BTEmuLoaderClient:
    """High-level facade over EmulatorInfo with BTHACK pointer-chase helpers."""

    def __init__(self):
        self.emulator: Optional[EmulatorInfo] = None

    # ----- lifecycle -----

    def connect(self) -> bool:
        self.emulator = connect_to_any_emulator()
        return self.emulator is not None

    def disconnect(self) -> None:
        if self.emulator:
            self.emulator.disconnect()
        self.emulator = None

    def is_connected(self) -> bool:
        return self.emulator is not None and self.emulator.connected_process is not None

    @property
    def emulator_name(self) -> str:
        return self.emulator.readable_name if self.emulator else "<none>"

    # ----- raw memory I/O -----

    def read_u8(self, address: int) -> int:
        assert self.emulator is not None
        return self.emulator.read_u8(address)

    def read_u16(self, address: int) -> int:
        assert self.emulator is not None
        return self.emulator.read_u16(address)

    def read_u32(self, address: int) -> int:
        assert self.emulator is not None
        return self.emulator.read_u32(address)

    def write_u8(self, address: int, value: int) -> None:
        assert self.emulator is not None
        self.emulator.write_u8(address, value)

    def write_u16(self, address: int, value: int) -> None:
        assert self.emulator is not None
        self.emulator.write_u16(address, value)

    def write_u32(self, address: int, value: int) -> None:
        assert self.emulator is not None
        self.emulator.write_u32(address, value)

    def read_bytes_n64(self, address: int, length: int) -> bytes:
        return bytes(self.read_u8(address + i) for i in range(length))

    def write_bytes_n64(self, address: int, data: bytes) -> None:
        for i, b in enumerate(data):
            self.write_u8(address + i, b)

    # ----- BTHACK pointer-chase helpers -----

    def deref(self, address: int) -> Optional[int]:
        """Read a u32 BE pointer; return its physical RDRAM offset or None
        if the value isn't a valid RDRAM pointer."""
        ptr = self.read_u32(address)
        if not is_rdram_pointer(ptr):
            return None
        return ptr & 0x7FFFFFFF

    def get_anchor(self) -> Optional[int]:
        """Physical RDRAM offset of the BTHACK anchor struct."""
        return self.deref(BTHACK_ANCHOR_OFFSET)

    def get_rom_version(self) -> Optional[Tuple[int, int, int]]:
        """(major, minor, patch) of the BTHACK ROM patch, or None if unpatched."""
        anchor = self.get_anchor()
        if anchor is None:
            return None
        major = self.read_u16(anchor + 0x0)
        minor = self.read_u8(anchor + 0x2)
        patch = self.read_u8(anchor + 0x3)
        return (major, minor, patch)
