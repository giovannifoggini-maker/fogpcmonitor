# FogMonitor by FogLabs — Windows system monitor, standard library only.
# Target: Windows 10/11 + Python 3.10–3.13 with Tkinter.
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import csv
import json
import os
import math
import platform
import queue
import shutil
import sys
import threading
import time
import traceback
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_NAME = "FogMonitor"
VERSION = "1.7.0"
BG = "#0b100d"
PANEL = "#121b15"
PANEL_2 = "#1b2920"
PANEL_3 = "#101812"
BORDER = "#2a3c30"
GREEN = "#54f58a"
GREEN_SOFT = "#b7ffd0"
TEXT = "#ecf5ef"
MUTED = "#91a397"
AMBER = "#ffd17a"
RED = "#ff7882"
BLUE = "#88b7ff"
PURPLE = "#c0a0ff"

IS_WINDOWS = sys.platform == "win32"


TRANSLATIONS = {
    "it": {
        "system_performance": "PRESTAZIONI DI SISTEMA",
        "active": "ATTIVO", "paused": "IN PAUSA", "detecting": "RILEVAMENTO…",
        "resuming": "RIPRESA…", "updating": "AGGIORNAMENTO…",
        "pause": "Ⅱ  Pausa", "resume": "▶  Riprendi", "refresh": "↻  Aggiorna",
        "export_csv": "↓  Esporta CSV", "overview": "Panoramica",
        "overview_subtitle": "Tieni d'occhio le risorse del tuo computer, in tempo reale.",
        "sampling_interval": "AGGIORNAMENTO", "interval_1": "1 secondo",
        "interval_2": "2 secondi", "interval_5": "5 secondi",
        "cpu": "PROCESSORE", "ram": "MEMORIA RAM", "gpu": "SCHEDA GRAFICA",
        "disk": "DISCO DI SISTEMA", "usage_current": "Utilizzo attuale",
        "waiting_data": "In attesa dei dati", "cpu_calibrating": "Calibrazione del sensore",
        "cpu_usage_total": "Utilizzo processore totale",
        "memory_not_available": "Dati memoria non disponibili",
        "gpu_peak": "Picco motori GPU rilevati",
        "gpu_not_exposed": "Contatore GPU non esposto da Windows",
        "disk_free": "{free} liberi su {drive}",
        "disk_not_available": "Disco di sistema non disponibile",
        "cpu_chart": "Andamento CPU", "last_60_samples": "ULTIMI 60 CAMPIONI",
        "your_pc": "Il tuo PC", "info": "INFO", "device": "DISPOSITIVO",
        "operating_system": "SISTEMA OPERATIVO", "logical_processors": "PROCESSORI LOGICI",
        "available_ram": "RAM DISPONIBILE", "temperature": "TEMPERATURA",
        "temp_not_exposed": "Non esposta da Windows", "processes": "Processi",
        "top_memory": "Le app che stanno usando più memoria", "search": "Cerca per nome o PID",
        "process_count_one": "{count} processo", "process_count_many": "{count} processi",
        "column_process": "PROCESSO  ↕", "column_pid": "PID  ↕", "column_memory": "MEMORIA  ↕",
        "footer_ready": "Pronto · nessun dato viene inviato online",
        "waiting_first": "In attesa del primo aggiornamento",
        "interval_set": "Intervallo impostato: {interval} · i dati restano sul PC",
        "pid_copied": "PID {pid} copiato negli appunti",
        "updated_at": "Aggiornato alle {time}",
        "collecting_samples": "Raccolta dei primi campioni…",
        "no_search_results": "Nessun risultato per la ricerca",
        "waiting_processes": "In attesa dei processi di Windows…",
        "no_sample_export": "Non ci sono ancora campioni da esportare.",
        "export_dialog_title": "Esporta cronologia FogMonitor",
        "csv_files": "File CSV", "all_files": "Tutti i file",
        "export_success": "Report esportato correttamente:\n{path}",
        "export_fail": "Impossibile esportare il report:\n{error}",
        "language": "Lingua", "lang_it": "Italiano", "lang_en": "English",
        "not_available": "N/D", "threads": "thread", "used": "usati",
        "free": "liberi", "startup_error_title": "FogMonitor — errore",
        "startup_error": "FogMonitor non è riuscito ad avviarsi o ha incontrato un errore.\n\nDettagli salvati in: {path}\n\nApri quel file e invia il contenuto per identificare il problema.",
        "windows_only": "FogMonitor è progettato per Windows 10/11.",
        "language_saved": "Lingua impostata su Italiano",
    },
    "en": {
        "system_performance": "SYSTEM PERFORMANCE",
        "active": "ACTIVE", "paused": "PAUSED", "detecting": "DETECTING…",
        "resuming": "RESUMING…", "updating": "UPDATING…",
        "pause": "Ⅱ  Pause", "resume": "▶  Resume", "refresh": "↻  Refresh",
        "export_csv": "↓  Export CSV", "overview": "Overview",
        "overview_subtitle": "Keep an eye on your computer's resources in real time.",
        "sampling_interval": "UPDATE INTERVAL", "interval_1": "1 second",
        "interval_2": "2 seconds", "interval_5": "5 seconds",
        "cpu": "PROCESSOR", "ram": "MEMORY", "gpu": "GRAPHICS",
        "disk": "SYSTEM DRIVE", "usage_current": "Current usage",
        "waiting_data": "Waiting for data", "cpu_calibrating": "Calibrating sensor",
        "cpu_usage_total": "Total processor usage",
        "memory_not_available": "Memory data unavailable",
        "gpu_peak": "Peak detected GPU engines",
        "gpu_not_exposed": "GPU counter not exposed by Windows",
        "disk_free": "{free} free on {drive}",
        "disk_not_available": "System drive unavailable",
        "cpu_chart": "CPU activity", "last_60_samples": "LAST 60 SAMPLES",
        "your_pc": "Your PC", "info": "INFO", "device": "DEVICE",
        "operating_system": "OPERATING SYSTEM", "logical_processors": "LOGICAL PROCESSORS",
        "available_ram": "AVAILABLE MEMORY", "temperature": "TEMPERATURE",
        "temp_not_exposed": "Not exposed by Windows", "processes": "Processes",
        "top_memory": "Apps using the most memory", "search": "Search by name or PID",
        "process_count_one": "{count} process", "process_count_many": "{count} processes",
        "column_process": "PROCESS  ↕", "column_pid": "PID  ↕", "column_memory": "MEMORY  ↕",
        "footer_ready": "Ready · no data is sent online",
        "waiting_first": "Waiting for the first update",
        "interval_set": "Update interval set to {interval} · data stays on this PC",
        "pid_copied": "PID {pid} copied to clipboard",
        "updated_at": "Updated at {time}",
        "collecting_samples": "Collecting initial samples…",
        "no_search_results": "No matching processes",
        "waiting_processes": "Waiting for Windows processes…",
        "no_sample_export": "There are no samples to export yet.",
        "export_dialog_title": "Export FogMonitor history",
        "csv_files": "CSV files", "all_files": "All files",
        "export_success": "Report exported successfully:\n{path}",
        "export_fail": "Could not export the report:\n{error}",
        "language": "Language", "lang_it": "Italiano", "lang_en": "English",
        "not_available": "N/A", "threads": "threads", "used": "used",
        "free": "free", "startup_error_title": "FogMonitor — error",
        "startup_error": "FogMonitor could not start or encountered an error.\n\nDetails saved to: {path}\n\nOpen that file and share its contents to help identify the issue.",
        "windows_only": "FogMonitor is designed for Windows 10/11.",
        "language_saved": "Language set to English",
    },
}


def fmt_bytes(n: int) -> str:
    size = float(max(0, n))
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024
    return f"{size:.1f} TB"


def resource_path(relative_path: str) -> str:
    """Find bundled resources in both source mode and PyInstaller builds."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


def user_data_dir() -> str:
    """Writable per-user location, also suitable for packaged/read-only installs."""
    base = os.environ.get("LOCALAPPDATA") if IS_WINDOWS else None
    if not base:
        base = os.path.join(os.path.expanduser("~"), ".local", "share")
    path = os.path.join(base, "FogLabs", "FogMonitor")
    os.makedirs(path, exist_ok=True)
    return path


def error_log_path() -> str:
    return os.path.join(user_data_dir(), "FogMonitor-error.log")


def settings_path() -> str:
    return os.path.join(user_data_dir(), "settings.json")


def load_language_setting() -> str:
    """Load the last selected UI language without requiring any external package."""
    try:
        with open(settings_path(), "r", encoding="utf-8") as stream:
            language = json.load(stream).get("language", "it")
        return language if language in TRANSLATIONS else "it"
    except (OSError, ValueError, AttributeError):
        return "it"


def save_language_setting(language: str) -> None:
    try:
        with open(settings_path(), "w", encoding="utf-8") as stream:
            json.dump({"language": language}, stream, ensure_ascii=False, indent=2)
    except OSError:
        # The app must remain usable if settings cannot be persisted.
        pass


def write_error_log(details: str, append: bool = False) -> str:
    """Write diagnostics outside the install directory so packaged builds work."""
    path = error_log_path()
    with open(path, "a" if append else "w", encoding="utf-8") as log_file:
        log_file.write(details.rstrip() + "\n")
    return path


class SystemReader:
    """Windows metrics via system APIs; never fabricates missing values."""
    def __init__(self):
        self.cpu_prev = None
        self.gpu = GPUReader() if IS_WINDOWS else None
        if IS_WINDOWS:
            self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            self.kernel32.GetSystemTimes.argtypes = [ctypes.POINTER(wt.FILETIME), ctypes.POINTER(wt.FILETIME), ctypes.POINTER(wt.FILETIME)]
            self.kernel32.GetSystemTimes.restype = wt.BOOL

    @staticmethod
    def _ft(v: wt.FILETIME) -> int:
        return (v.dwHighDateTime << 32) | v.dwLowDateTime

    def cpu_percent(self):
        if not IS_WINDOWS:
            return None
        idle, kernel, user = wt.FILETIME(), wt.FILETIME(), wt.FILETIME()
        if not self.kernel32.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user)):
            return None
        now = (self._ft(idle), self._ft(kernel), self._ft(user))
        old, self.cpu_prev = self.cpu_prev, now
        if old is None:
            return None
        idle_delta = now[0] - old[0]
        total_delta = (now[1] - old[1]) + (now[2] - old[2])
        if total_delta <= 0:
            return 0.0
        return max(0.0, min(100.0, (1.0 - idle_delta / total_delta) * 100.0))

    def memory(self):
        if not IS_WINDOWS:
            return None
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", wt.DWORD), ("dwMemoryLoad", wt.DWORD),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]
        info = MEMORYSTATUSEX()
        info.dwLength = ctypes.sizeof(info)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.GlobalMemoryStatusEx.argtypes = [ctypes.POINTER(MEMORYSTATUSEX)]
        kernel32.GlobalMemoryStatusEx.restype = wt.BOOL
        if not kernel32.GlobalMemoryStatusEx(ctypes.byref(info)):
            return None
        used = int(info.ullTotalPhys - info.ullAvailPhys)
        return {"total": int(info.ullTotalPhys), "used": used,
                "available": int(info.ullAvailPhys), "percent": float(info.dwMemoryLoad)}

    def disk(self):
        if not IS_WINDOWS:
            return None
        drive = os.environ.get("SystemDrive", "C:") + "\\"
        try:
            d = shutil.disk_usage(drive)
            return {"total": d.total, "used": d.used, "free": d.free,
                    "percent": d.used / d.total * 100 if d.total else 0, "drive": drive}
        except OSError:
            return None

    def processes(self, limit=8):
        if not IS_WINDOWS:
            return []
        try:
            psapi = ctypes.WinDLL("psapi", use_last_error=True)
            kernel = ctypes.WinDLL("kernel32", use_last_error=True)
            psapi.EnumProcesses.argtypes = [ctypes.c_void_p, wt.DWORD, ctypes.POINTER(wt.DWORD)]
            psapi.EnumProcesses.restype = wt.BOOL
            psapi.GetModuleBaseNameW.argtypes = [wt.HANDLE, wt.HMODULE, wt.LPWSTR, wt.DWORD]
            psapi.GetModuleBaseNameW.restype = wt.DWORD
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            kernel.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
            kernel.OpenProcess.restype = wt.HANDLE
            kernel.CloseHandle.argtypes = [wt.HANDLE]
            kernel.CloseHandle.restype = wt.BOOL
            PROCESS_VM_READ = 0x0010
            LIST = wt.DWORD * 4096
            pids = LIST()
            needed = wt.DWORD()
            if not psapi.EnumProcesses(ctypes.byref(pids), ctypes.sizeof(pids), ctypes.byref(needed)):
                return []
            count = min(needed.value // ctypes.sizeof(wt.DWORD), len(pids))

            class PMC(ctypes.Structure):
                _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD),
                            ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                            ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]
            psapi.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.c_void_p, wt.DWORD]
            psapi.GetProcessMemoryInfo.restype = wt.BOOL
            rows = []
            name_buffer = ctypes.create_unicode_buffer(260)
            for i in range(count):
                pid = int(pids[i])
                if pid <= 0:
                    continue
                handle = kernel.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_VM_READ, False, pid)
                if not handle:
                    continue
                try:
                    name_buffer.value = ""
                    if not psapi.GetModuleBaseNameW(handle, None, name_buffer, len(name_buffer)):
                        # Some protected/UWP processes do not expose a module name.
                        continue
                    pmc = PMC(); pmc.cb = ctypes.sizeof(PMC)
                    if psapi.GetProcessMemoryInfo(handle, ctypes.byref(pmc), pmc.cb):
                        rows.append((name_buffer.value, pid, int(pmc.WorkingSetSize)))
                finally:
                    kernel.CloseHandle(handle)
            rows.sort(key=lambda r: r[2], reverse=True)
            return rows[:limit]
        except Exception:
            return []

    def gpu_percent(self):
        if not self.gpu:
            return None
        return self.gpu.read_peak()


class GPUReader:
    """Optional PDH GPU-engine counter. Missing counters are reported as unavailable."""
    def __init__(self):
        self.query = ctypes.c_void_p()
        self.counter = ctypes.c_void_p()
        self.available = False
        try:
            self.pdh = ctypes.WinDLL("pdh", use_last_error=True)
            self.pdh.PdhOpenQueryW.argtypes = [wt.LPCWSTR, ctypes.c_size_t, ctypes.POINTER(ctypes.c_void_p)]
            self.pdh.PdhOpenQueryW.restype = wt.LONG
            self.pdh.PdhAddEnglishCounterW.argtypes = [ctypes.c_void_p, wt.LPCWSTR, ctypes.c_size_t, ctypes.POINTER(ctypes.c_void_p)]
            self.pdh.PdhAddEnglishCounterW.restype = wt.LONG
            self.pdh.PdhCollectQueryData.argtypes = [ctypes.c_void_p]
            self.pdh.PdhCollectQueryData.restype = wt.LONG
            self.pdh.PdhGetFormattedCounterArrayW.argtypes = [ctypes.c_void_p, wt.DWORD, ctypes.POINTER(wt.DWORD), ctypes.POINTER(wt.DWORD), ctypes.c_void_p]
            self.pdh.PdhGetFormattedCounterArrayW.restype = wt.LONG
            if self.pdh.PdhOpenQueryW(None, 0, ctypes.byref(self.query)) == 0:
                status = self.pdh.PdhAddEnglishCounterW(self.query, r"\GPU Engine(*)\Utilization Percentage", 0, ctypes.byref(self.counter))
                if status == 0:
                    self.available = True
                    self.pdh.PdhCollectQueryData(self.query)  # initial sample
        except Exception:
            self.available = False

    def read_peak(self):
        if not self.available:
            return None
        try:
            self.pdh.PdhCollectQueryData(self.query)
            time.sleep(0.015)
            size = wt.DWORD(0)
            count = wt.DWORD(0)
            # PDH_MORE_DATA is expected for the first call; the byte count is returned.
            self.pdh.PdhGetFormattedCounterArrayW(self.counter, 0x00000200, ctypes.byref(size), ctypes.byref(count), None)
            if size.value <= 0 or count.value <= 0:
                return None
            buf = ctypes.create_string_buffer(size.value)
            status = self.pdh.PdhGetFormattedCounterArrayW(self.counter, 0x00000200, ctypes.byref(size), ctypes.byref(count), ctypes.cast(buf, ctypes.c_void_p))
            if status != 0:
                return None
            class VALUE_UNION(ctypes.Union):
                _fields_ = [("longValue", wt.LONG), ("doubleValue", ctypes.c_double), ("largeValue", ctypes.c_longlong), ("wideStringValue", wt.LPWSTR), ("stringValue", ctypes.c_char_p)]
            class COUNTER_VALUE(ctypes.Structure):
                _fields_ = [("CStatus", wt.DWORD), ("value", VALUE_UNION)]
            class ITEM(ctypes.Structure):
                _fields_ = [("szName", wt.LPWSTR), ("FmtValue", COUNTER_VALUE)]
            arr = ctypes.cast(buf, ctypes.POINTER(ITEM))
            vals = [float(arr[i].FmtValue.value.doubleValue) for i in range(count.value)
                    if arr[i].FmtValue.CStatus == 0 and 0 <= arr[i].FmtValue.value.doubleValue <= 100.5]
            if not vals:
                return None
            # Display peak engine instance, not a misleading sum of all engines.
            return min(100.0, max(vals))
        except Exception:
            return None

    def close(self):
        try:
            if self.query and self.pdh:
                self.pdh.PdhCloseQuery(self.query)
        except Exception:
            pass


def _rounded_shape(canvas, x1, y1, x2, y2, radius, fill, outline="", width=1, tags=()):
    """Draw a smooth rounded rectangle using Tk Canvas primitives."""
    if x2 <= x1 or y2 <= y1:
        return
    radius = max(0, min(radius, (x2 - x1) / 2, (y2 - y1) / 2))
    points = (
        x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
        x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1,
    )
    return canvas.create_polygon(
        *points, smooth=True, splinesteps=16, fill=fill, outline=outline,
        width=width, tags=tags
    )


class RoundedPanel(tk.Frame):
    """A panel with a soft rounded Canvas surface and normal Tk child widgets."""
    def __init__(self, master, panel_bg=PANEL, border=BORDER, radius=24, accent=None, **kwargs):
        super().__init__(master, bg=BG, bd=0, highlightthickness=0, **kwargs)
        self.panel_bg = panel_bg
        self.panel_border = border
        self.radius = radius
        self.accent = accent
        self.surface = tk.Canvas(self, bg=BG, highlightthickness=0, bd=0)
        self.surface.place(x=0, y=0, relwidth=1, relheight=1)
        self.surface.tk.call("lower", self.surface._w)
        self.bind("<Configure>", self._draw_surface)

    def _draw_surface(self, _event=None):
        c = self.surface
        c.delete("surface")
        w, h = max(2, self.winfo_width()), max(2, self.winfo_height())
        _rounded_shape(c, 1, 1, w - 1, h - 1, self.radius,
                       self.panel_bg, self.panel_border, 1, tags="surface")
        if self.accent:
            _rounded_shape(c, 17, 6, min(w - 17, 69), 10, 2,
                           self.accent, tags="surface")
        c.tag_lower("surface")


class RoundButton(tk.Canvas):
    """Rounded, lightweight button matching FogLabs' soft dashboard style."""
    def __init__(self, master, text, command, primary=False, width=None, height=38, bg=BG):
        self.label = text
        self.command = command
        self.primary = primary
        self.hover = False
        self.button_width = width or max(92, len(text) * 7 + 28)
        self.button_height = height
        self.button_bg = bg
        super().__init__(master, width=self.button_width, height=self.button_height,
                         bg=self.button_bg, highlightthickness=0, bd=0, cursor="hand2", takefocus=True)
        self.bind("<Configure>", self._draw)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._click)
        self.bind("<Return>", self._click)
        self.bind("<space>", self._click)
        self.bind("<FocusIn>", self._draw)
        self.bind("<FocusOut>", self._draw)
        self._draw()

    def set_text(self, text):
        self.label = text
        self.button_width = max(92, len(text) * 7 + 30)
        self.configure(width=self.button_width)
        self._draw()

    def _palette(self):
        if self.primary:
            fill = "#20452d" if not self.hover else "#2a583a"
            return fill, "#effff3", "#3b7650"
        fill = "#162219" if not self.hover else "#203226"
        return fill, GREEN_SOFT, "#2c4132"

    def _draw(self, _event=None):
        self.delete("all")
        w, h = max(8, self.winfo_width()), max(8, self.winfo_height())
        fill, fg, outline = self._palette()
        radius = min(13, h / 2 - 1)
        _rounded_shape(self, 1, 1, w - 1, h - 1, radius, fill, outline, 1)
        self.create_text(w / 2, h / 2, text=self.label, fill=fg,
                         font=("Segoe UI", 9, "bold"))
        if self.focus_get() is self:
            _rounded_shape(self, 3, 3, w - 3, h - 3, 11, "", GREEN, 1)

    def _on_enter(self, _event=None):
        self.hover = True
        self._draw()

    def _on_leave(self, _event=None):
        self.hover = False
        self._draw()

    def _click(self, _event=None):
        if callable(self.command):
            self.command()
        return "break"


class Meter(tk.Canvas):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("bg", PANEL)
        kwargs.setdefault("height", 8)
        kwargs.setdefault("highlightthickness", 0)
        kwargs.setdefault("bd", 0)
        super().__init__(master, **kwargs)
        self.value = 0.0
        self.color = GREEN
        self._animation_job = None
        self.bind("<Configure>", lambda _e: self.draw())

    def set_value(self, value, color=None):
        target = max(0.0, min(100.0, float(value or 0)))
        if color:
            self.color = color
        start = self.value
        if self._animation_job is not None:
            try:
                self.after_cancel(self._animation_job)
            except tk.TclError:
                pass
            self._animation_job = None
        started = time.monotonic()
        duration = 0.24

        def animate():
            progress = min(1.0, (time.monotonic() - started) / duration)
            # Cubic ease-out keeps the bar responsive without abrupt jumps.
            eased = 1.0 - (1.0 - progress) ** 3
            self.value = start + (target - start) * eased
            self.draw()
            if progress < 1.0:
                self._animation_job = self.after(16, animate)
            else:
                self.value = target
                self._animation_job = None

        animate()

    def draw(self):
        self.delete("all")
        w = max(1, self.winfo_width())
        h = max(1, self.winfo_height())
        r = h / 2
        _rounded_shape(self, 0, 0, w, h, r, "#243329")
        fill = max(h, int(w * self.value / 100)) if self.value > 0 else 0
        if fill > 0:
            _rounded_shape(self, 0, 0, min(w, fill), h, min(r, fill / 2), self.color)


class MetricCard(RoundedPanel):
    """Soft-cornered metric tile with animated usage bar and live sparkline."""
    def __init__(self, master, title, accent=GREEN, hint="Current usage"):
        super().__init__(master, panel_bg=PANEL, border=BORDER, radius=24, accent=accent)
        self.accent = accent
        self.spark_history = []
        self.spark_current = None
        body = tk.Frame(self, bg=PANEL)
        body.pack(fill="both", expand=True, padx=10, pady=(10, 7))
        heading = tk.Frame(body, bg=PANEL)
        heading.pack(fill="x")
        self.title_label = tk.Label(heading, text=title, bg=PANEL, fg=MUTED,
                                    font=("Segoe UI", 9, "bold"))
        self.title_label.pack(side="left")
        self.dot = tk.Canvas(heading, width=12, height=12, bg=PANEL, highlightthickness=0, bd=0)
        self.dot.pack(side="right", pady=2)
        self.dot.create_oval(2, 2, 10, 10, fill=accent, outline="")

        value_row = tk.Frame(body, bg=PANEL)
        value_row.pack(fill="x", pady=(6, 0))
        self.value = tk.Label(value_row, text="—", bg=PANEL, fg=TEXT,
                              font=("Segoe UI", 27, "bold"), anchor="w")
        self.value.pack(side="left", fill="x", expand=True)
        self.sparkline = tk.Canvas(value_row, width=76, height=29, bg=PANEL,
                                   highlightthickness=0, bd=0)
        self.sparkline.pack(side="right", padx=(5, 0), pady=(5, 0))
        self.spark_point = None
        self.spark_ring = None
        self.spark_core = None
        self.sparkline.bind("<Configure>", lambda _e: self.draw_sparkline())

        self.detail = tk.Label(body, text=hint, bg=PANEL, fg=MUTED,
                               font=("Segoe UI", 9), anchor="w")
        self.detail.pack(fill="x", pady=(1, 6))
        self.meter = Meter(body, bg=PANEL, height=8)
        self.meter.pack(fill="x")

    def update_metric(self, value, detail, percent=None, color=None):
        self.value.configure(text=value)
        self.detail.configure(text=detail)
        self.meter.set_value(percent or 0, color or self.accent)
        try:
            current = float(percent) if percent is not None and value not in ("N/D", "N/A", "…", "—") else None
        except (TypeError, ValueError):
            current = None
        self.spark_current = current
        self.spark_history.append(current)
        self.spark_history = self.spark_history[-24:]
        self.draw_sparkline()

    def draw_sparkline(self, phase=0.0):
        """Redraw the chart only when data or its size changes."""
        c = self.sparkline
        c.delete("all")
        self.spark_point = self.spark_ring = self.spark_core = None
        w = max(10, c.winfo_width())
        h = max(10, c.winfo_height())
        last_n = self.spark_history[-24:]
        usable = [(i, v) for i, v in enumerate(last_n) if v is not None]
        if len(usable) < 2:
            for x in range(7, int(w) - 4, 8):
                c.create_oval(x, h / 2 - 1, x + 2, h / 2 + 1, fill=BORDER, outline="")
            return

        points = []
        left, right, top, bottom = 3, w - 3, 4, h - 4
        denominator = max(1, len(last_n) - 1)
        for i, value in usable:
            x = left + (right - left) * i / denominator
            y = bottom - (bottom - top) * max(0, min(100, value)) / 100
            points.extend((x, y))

        if len(points) >= 4:
            area = [points[0], bottom, *points, points[-2], bottom]
            c.create_polygon(*area, fill=self.accent, outline="", stipple="gray50")
            c.create_line(*points, fill=self.accent, width=2, smooth=True,
                          splinesteps=12, capstyle="round", joinstyle="round")
            x, y = points[-2], points[-1]
            self.spark_point = (x, y)
            self.spark_ring = c.create_oval(x - 4, y - 4, x + 4, y + 4,
                                             outline=self.accent, width=1)
            self.spark_core = c.create_oval(x - 2, y - 2, x + 2, y + 2,
                                             fill=GREEN_SOFT, outline=self.accent, width=1)
            self.pulse_sparkline(phase)

    def pulse_sparkline(self, phase=0.0):
        """Animate only the tiny endpoint halo; leave the expensive line untouched."""
        if not self.spark_point or not self.spark_ring:
            return
        x, y = self.spark_point
        radius = 2.8 + (math.sin(phase) + 1) * 0.9
        self.sparkline.coords(self.spark_ring, x - radius, y - radius, x + radius, y + radius)


class FogMonitorApp:
    def __init__(self, root):
        self.root = root
        self.language = load_language_setting()
        self.last_sample = None
        self.root.title(f"FogMonitor · by FogLabs · v{VERSION}")
        self.root.configure(bg=BG)
        # Load the native window icon from bundled assets; the app still runs if it is absent.
        try:
            icon_path = resource_path(os.path.join("assets", "fogmonitor-icon.png"))
            self.app_icon_image = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, self.app_icon_image)
        except (tk.TclError, OSError):
            self.app_icon_image = None
        # Adapt the first window to the current display so it is usable on laptops too.
        screen_w = max(900, int(self.root.winfo_screenwidth()))
        screen_h = max(620, int(self.root.winfo_screenheight()))
        self.compact_ui = screen_h < 850
        self.ui_margin = 18 if self.compact_ui else 28
        start_w = min(1240, screen_w - 40)
        start_h = min(940, screen_h - 60)
        min_w = min(1000, screen_w - 40)
        min_h = min(620 if self.compact_ui else 680, screen_h - 60)
        self.root.minsize(max(860, min_w), max(580, min_h))
        start_x = max(0, (screen_w - start_w) // 2)
        start_y = max(0, (screen_h - start_h) // 2)
        self.root.geometry(f"{start_w}x{start_h}+{start_x}+{start_y}")
        self.root.option_add("*Font", ("Segoe UI", 10))
        self.reader = SystemReader()
        self.after_id = None
        self.running = True
        self.monitoring = True
        self.history = []
        self.sample_history = []
        self.process_rows = []
        self.sample_queue = queue.Queue(maxsize=1)
        self.stop_event = threading.Event()
        self.wake_event = threading.Event()
        self.has_sample = False
        self.sort_column = "memory"
        self.sort_reverse = True
        self.animation_phase = 0.0
        self.animation_started = time.monotonic()
        self.animation_job = None
        self.chart_point = None
        self.chart_ring = None
        self.tree_items = {}
        self._style()
        self._build()
        self.worker = threading.Thread(target=self._worker_loop, name="FogMonitorSampler", daemon=True)
        self.worker.start()
        self._tick()
        self._animate_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def tr(self, key: str, **kwargs) -> str:
        text = TRANSLATIONS.get(self.language, TRANSLATIONS["it"]).get(key, key)
        return text.format(**kwargs) if kwargs else text

    def _change_language(self, _event=None):
        selected = self.language_var.get()
        new_language = "en" if selected == "English" else "it"
        if new_language == self.language:
            return
        self.language = new_language
        save_language_setting(new_language)
        # Rebuild the interface using the new locale while keeping metrics and history.
        for child in self.root.winfo_children():
            child.destroy()
        self._build()
        self.root.update_idletasks()
        self._draw_chart()
        if self.last_sample is not None:
            self._apply_sample(self.last_sample, record_history=False)
        if not self.monitoring:
            self.pause_button.set_text(self.tr("resume"))
            self._set_status("paused", AMBER)
        elif self.last_sample is None:
            self.pause_button.set_text(self.tr("pause"))
            self._set_status("detecting", GREEN)
        else:
            self.pause_button.set_text(self.tr("pause"))
            self._set_status("active", GREEN)

    def _action_button(self, master, label, command, primary=False):
        return RoundButton(master, label, command, primary=primary)

    def _style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", background=PANEL_3, foreground=TEXT,
                        fieldbackground=PANEL_3, rowheight=(30 if self.compact_ui else 36), borderwidth=0,
                        relief="flat", bordercolor=BORDER, lightcolor=PANEL_3,
                        darkcolor=PANEL_3, font=("Segoe UI", 9), padding=(8, 5))
        style.configure("Treeview.Heading", background=PANEL_2, foreground=GREEN_SOFT,
                        relief="flat", font=("Segoe UI", 9, "bold"), padding=(10, 10))
        style.map("Treeview", background=[("selected", "#245536")],
                  foreground=[("selected", "#ffffff")])
        style.map("Treeview.Heading", background=[("active", "#203629")])
        style.configure("Fog.TCombobox", fieldbackground=PANEL_3, background=PANEL_2,
                        foreground=TEXT, arrowcolor=GREEN, bordercolor=BORDER,
                        lightcolor=BORDER, darkcolor=BORDER, padding=(8, 6))
        style.map("Fog.TCombobox", fieldbackground=[("readonly", PANEL_3)],
                  foreground=[("readonly", TEXT)], selectbackground=[("readonly", PANEL_3)],
                  selectforeground=[("readonly", TEXT)])
        style.configure("Fog.Vertical.TScrollbar", background=PANEL_2, troughcolor=PANEL_3,
                        bordercolor=PANEL_3, arrowcolor=MUTED, lightcolor=PANEL_2,
                        darkcolor=PANEL_2, relief="flat", arrowsize=12)
        style.map("Fog.Vertical.TScrollbar", background=[("active", "#2b4634")])

    def _build(self):
        # Main header: one clear identity area and only the three most useful actions.
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=self.ui_margin, pady=((12, 8) if self.compact_ui else (18, 10)))

        logo = tk.Canvas(header, width=56, height=56, bg=BG, highlightthickness=0, bd=0)
        self.logo = logo
        logo.pack(side="left", padx=(0, 14))
        # Futuristic FogLabs mark: an angular F, segmented orbit and tiny data pixels.
        # It deliberately avoids heartbeat/medical motifs.
        _rounded_shape(logo, 1, 1, 55, 55, 17, PANEL, outline="#284b35", width=1)
        logo.create_arc(4, 4, 52, 52, start=28, extent=282, style="arc",
                        outline="#286c43", width=1.4)
        logo.create_arc(4, 4, 52, 52, start=208, extent=70, style="arc",
                        outline=GREEN, width=2.1)
        logo.create_polygon(14, 13, 42, 13, 35, 20, 22, 20, 22, 24,
                            34, 24, 28, 30, 22, 30, 22, 41, 14, 41,
                            fill=GREEN, outline="")
        # Data pixels provide a subtle telemetry cue without cluttering the mark.
        logo.create_rectangle(31, 33, 35, 37, fill=GREEN_SOFT, outline="")
        logo.create_rectangle(37, 28, 41, 32, fill="#278e55", outline="")
        logo.create_rectangle(37, 36, 41, 40, fill="#278e55", outline="")
        self.logo_orbit = logo.create_oval(0, 0, 0, 0, fill=GREEN_SOFT,
                                           outline="#0b100d", width=1, tags="orbit")

        title_block = tk.Frame(header, bg=BG)
        title_block.pack(side="left", fill="y")
        wordmark = tk.Frame(title_block, bg=BG)
        wordmark.pack(anchor="w")
        tk.Label(wordmark, text="Fog", fg=TEXT, bg=BG,
                 font=("Segoe UI Semibold", 21)).pack(side="left")
        tk.Label(wordmark, text="Monitor", fg=GREEN, bg=BG,
                 font=("Segoe UI Semibold", 21)).pack(side="left")
        brandline = tk.Frame(title_block, bg=BG)
        brandline.pack(anchor="w", pady=(1, 0))
        tk.Label(brandline, text="by", fg=MUTED, bg=BG,
                 font=("Segoe UI", 9)).pack(side="left")
        tk.Label(brandline, text="FogLabs", fg=GREEN_SOFT, bg=BG,
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(4, 9))
        tk.Label(brandline, text="/  " + self.tr("system_performance"), fg="#5f7567", bg=BG,
                 font=("Segoe UI", 8, "bold")).pack(side="left")

        actions = tk.Frame(header, bg=BG)
        actions.pack(side="right", anchor="center")
        action_top = tk.Frame(actions, bg=BG)
        action_top.pack(anchor="e", pady=(0, 8))
        language_shell = RoundedPanel(action_top, panel_bg=PANEL_3, border="#304336", radius=14)
        language_shell.pack(side="left", padx=(0, 8), fill="y")
        tk.Label(language_shell, text="UI", bg=PANEL_3, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(8, 2), pady=4)
        self.language_var = tk.StringVar(value=self.tr("lang_it") if self.language == "it" else self.tr("lang_en"))
        self.language_combo = ttk.Combobox(
            language_shell, textvariable=self.language_var, values=("Italiano", "English"),
            state="readonly", width=8, style="Fog.TCombobox"
        )
        self.language_combo.pack(side="left", padx=5, pady=4)
        self.language_combo.bind("<<ComboboxSelected>>", self._change_language)

        status_box = RoundedPanel(action_top, panel_bg="#10271a", border="#245536", radius=16)
        status_box.pack(side="left")
        self.status_dot = tk.Canvas(status_box, width=16, height=16, bg="#10271a", highlightthickness=0)
        self.status_dot.pack(side="left", padx=(9, 4), pady=5)
        self.status_ring = self.status_dot.create_oval(1, 1, 15, 15, outline="#2f7547", width=1, tags="pulse")
        self.status_core = self.status_dot.create_oval(4, 4, 12, 12, fill=GREEN, outline="", tags="core")
        self.status = tk.Label(status_box, text=self.tr("active"), bg="#10271a", fg=GREEN_SOFT,
                               font=("Segoe UI", 8, "bold"))
        self.status.pack(side="left", padx=(0, 10), pady=6)
        action_row = tk.Frame(actions, bg=BG)
        action_row.pack(anchor="e")
        self.pause_button = self._action_button(action_row, self.tr("pause"), self._toggle_monitoring)
        self.pause_button.pack(side="left", padx=(0, 7))
        self.refresh_button = self._action_button(action_row, self.tr("refresh"), self._request_refresh, primary=True)
        self.refresh_button.pack(side="left", padx=(0, 7))
        self.export_button = self._action_button(action_row, self.tr("export_csv"), self._export_csv)
        self.export_button.pack(side="left")

        # Section intro and simple sampling selector.
        intro = tk.Frame(self.root, bg=BG)
        intro.pack(fill="x", padx=self.ui_margin, pady=((0, 8) if self.compact_ui else (2, 12)))
        left_intro = tk.Frame(intro, bg=BG)
        left_intro.pack(side="left")
        tk.Label(left_intro, text=self.tr("overview"), bg=BG, fg=TEXT,
                 font=("Segoe UI", 15, "bold")).pack(anchor="w")
        tk.Label(left_intro, text=self.tr("overview_subtitle"),
                 bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))
        interval_wrap = tk.Frame(intro, bg=BG)
        interval_wrap.pack(side="right", anchor="e", pady=(3, 0))
        tk.Label(interval_wrap, text=self.tr("sampling_interval"), bg=BG, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(0, 9))
        self.interval_var = tk.StringVar(value=self.tr({1.0: "interval_1", 2.0: "interval_2", 5.0: "interval_5"}.get(getattr(self, "sample_interval", 2.0), "interval_2")))
        interval_shell = RoundedPanel(interval_wrap, panel_bg=PANEL_3, border="#304336", radius=14)
        interval_shell.pack(side="left")
        self.interval_combo = ttk.Combobox(interval_shell, textvariable=self.interval_var,
                                           values=(self.tr("interval_1"), self.tr("interval_2"), self.tr("interval_5")),
                                           state="readonly", width=12, style="Fog.TCombobox")
        self.interval_combo.pack(side="left", padx=5, pady=4)
        self.interval_combo.bind("<<ComboboxSelected>>", self._set_interval)
        if not hasattr(self, "sample_interval"):
            self.sample_interval = 2.0

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=self.ui_margin, pady=((0, 8) if self.compact_ui else (0, 12)))

        # Resource cards.
        self.metrics = tk.Frame(self.root, bg=BG)
        self.metrics.pack(fill="x", padx=self.ui_margin)
        for col in range(4):
            self.metrics.grid_columnconfigure(col, weight=1, uniform="metric")
        self.cpu_card = MetricCard(self.metrics, self.tr("cpu"), accent=GREEN, hint=self.tr("waiting_data"))
        self.ram_card = MetricCard(self.metrics, self.tr("ram"), accent=BLUE, hint=self.tr("waiting_data"))
        self.gpu_card = MetricCard(self.metrics, self.tr("gpu"), accent=PURPLE, hint=self.tr("waiting_data"))
        self.disk_card = MetricCard(self.metrics, self.tr("disk"), accent=AMBER, hint=self.tr("waiting_data"))
        for i, card in enumerate((self.cpu_card, self.ram_card, self.gpu_card, self.disk_card)):
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 7, 0 if i == 3 else 7))

        # The graph gets the space; machine facts stay compact and readable.
        mid = tk.Frame(self.root, bg=BG)
        mid.pack(fill="both", expand=True, padx=self.ui_margin, pady=(8 if self.compact_ui else 12))
        chart_panel = RoundedPanel(mid, panel_bg=PANEL, border=BORDER, radius=26)
        chart_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        chart_header = tk.Frame(chart_panel, bg=PANEL)
        chart_header.pack(fill="x", padx=18, pady=((8, 0) if self.compact_ui else (10, 0)))
        tk.Label(chart_header, text=self.tr("cpu_chart"), bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        self.chart_live_value = tk.Label(chart_header, text="CPU  —%", bg="#13281a", fg=GREEN_SOFT,
                                         font=("Segoe UI", 8, "bold"), padx=9, pady=4)
        self.chart_live_value.pack(side="right", padx=(8, 0))
        tk.Label(chart_header, text=self.tr("last_60_samples"), bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(side="right")
        self.chart = tk.Canvas(chart_panel, height=(95 if self.compact_ui else 170), bg=PANEL, highlightthickness=0)
        self.chart.pack(fill="both", expand=True, padx=14, pady=((5, 7) if self.compact_ui else (6, 10)))
        self.chart.bind("<Configure>", lambda _e: self._draw_chart())

        sys_panel = RoundedPanel(mid, panel_bg=PANEL, border=BORDER, radius=26, width=285)
        sys_panel.pack(side="right", fill="y")
        sys_panel.pack_propagate(False)
        sys_head = tk.Frame(sys_panel, bg=PANEL)
        sys_head.pack(fill="x", padx=17, pady=((8, 4) if self.compact_ui else (12, 6)))
        tk.Label(sys_head, text=self.tr("your_pc"), bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        tk.Label(sys_head, text=self.tr("info"), bg=PANEL, fg=GREEN,
                 font=("Segoe UI", 8, "bold")).pack(side="right")
        info_body = tk.Frame(sys_panel, bg=PANEL)
        info_body.pack(fill="both", expand=True, padx=(12 if self.compact_ui else 17), pady=(0, 5 if self.compact_ui else 8))
        self.info_labels = {}
        if self.compact_ui:
            info_rows = [
                ("device", platform.node() or "PC Windows"),
                ("operating_system", f"Windows {platform.release()}" if IS_WINDOWS else platform.system()),
                ("logical_processors", f"{os.cpu_count() or self.tr('not_available')} {self.tr('threads')}"),
            ]
        else:
            info_rows = [
                ("device", platform.node() or "PC Windows"),
                ("operating_system", f"Windows {platform.release()}" if IS_WINDOWS else platform.system()),
                ("logical_processors", f"{os.cpu_count() or self.tr('not_available')} {self.tr('threads')}"),
                ("available_ram", self.tr("waiting_data")),
                ("temperature", self.tr("temp_not_exposed")),
            ]
        for index, (key, initial_value) in enumerate(info_rows):
            row = tk.Frame(info_body, bg=PANEL)
            row.pack(fill="x", pady=((0, 0) if self.compact_ui else (1, 0)))
            tk.Label(row, text=self.tr(key), bg=PANEL, fg=MUTED,
                     font=("Segoe UI", 7, "bold")).pack(anchor="w")
            val = tk.Label(row, text=initial_value, bg=PANEL, fg=TEXT,
                           font=("Segoe UI", 8), anchor="w", justify="left", wraplength=245)
            val.pack(anchor="w", fill="x", pady=(0, 0))
            self.info_labels[key] = val

        # Search is prominent, the process list has its own scrollbar, and selection is clickable.
        proc_panel = RoundedPanel(self.root, panel_bg=PANEL, border=BORDER, radius=26)
        proc_panel.pack(fill="x", padx=self.ui_margin, pady=(0, 7 if self.compact_ui else 9))
        ph = tk.Frame(proc_panel, bg=PANEL)
        ph.pack(fill="x", padx=16, pady=((8, 6) if self.compact_ui else (10, 8)))
        ph_left = tk.Frame(ph, bg=PANEL)
        ph_left.pack(side="left")
        tk.Label(ph_left, text=self.tr("processes"), bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(ph_left, text=self.tr("top_memory"), bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 8)).pack(anchor="w", pady=(2, 0))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._render_process_table())
        search_wrap = RoundedPanel(ph, panel_bg=PANEL_3, border="#304336", radius=16)
        search_wrap.pack(side="left", fill="x", expand=True, padx=(22, 8))
        tk.Label(search_wrap, text="⌕", bg=PANEL_3, fg=GREEN,
                 font=("Segoe UI Symbol", 14)).pack(side="left", padx=(13, 5), pady=4)
        self.search_entry = tk.Entry(search_wrap, textvariable=self.search_var, bg=PANEL_3,
                                     fg=TEXT, insertbackground=GREEN, relief="flat",
                                     font=("Segoe UI", 10), bd=0, highlightthickness=0)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5), pady=5, ipady=5)
        self.search_entry.insert(0, "")
        self.clear_search_btn = RoundButton(search_wrap, "×", lambda: self.search_var.set(""),
                                             primary=False, width=30, height=28, bg=PANEL_3)
        self.clear_search_btn.pack(side="right", padx=(0, 5), pady=4)
        self.process_count = tk.Label(ph, text=self.tr("process_count_many", count=0), bg=PANEL, fg=MUTED,
                                      font=("Segoe UI", 8))
        self.process_count.pack(side="right", padx=(8, 0))

        columns = ("name", "pid", "memory")
        table_wrap = RoundedPanel(proc_panel, panel_bg=PANEL_3, border="#26392d", radius=16)
        table_wrap.pack(fill="x", padx=12, pady=(0, 7 if self.compact_ui else 9))
        self.tree = ttk.Treeview(table_wrap, columns=columns, show="headings", height=(3 if self.compact_ui else 5), selectmode="browse")
        self.tree.heading("name", text=self.tr("column_process"), command=lambda: self._sort_processes("name"))
        self.tree.heading("pid", text=self.tr("column_pid"), command=lambda: self._sort_processes("pid"))
        self.tree.heading("memory", text=self.tr("column_memory"), command=lambda: self._sort_processes("memory"))
        self.tree.column("name", width=600, minwidth=220, anchor="w", stretch=True)
        self.tree.column("pid", width=100, minwidth=75, anchor="center", stretch=False)
        self.tree.column("memory", width=150, minwidth=110, anchor="e", stretch=False)
        scrollbar = ttk.Scrollbar(table_wrap, orient="vertical", command=self.tree.yview, style="Fog.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.tag_configure("odd", background=PANEL_3)
        self.tree.tag_configure("even", background="#121e17")
        self.tree.pack(side="left", fill="x", expand=True, padx=(7, 0), pady=7)
        scrollbar.pack(side="right", fill="y", padx=(0, 7), pady=7)
        self.tree.bind("<Double-1>", self._copy_selected_pid)

        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=self.ui_margin, pady=(0, 6 if self.compact_ui else 8))
        self.footer_msg = tk.Label(footer, text=self.tr("footer_ready"),
                                   bg=BG, fg=MUTED, font=("Segoe UI", 8))
        self.footer_msg.pack(side="left")
        self.last_update_label = tk.Label(footer, text=self.tr("waiting_first"),
                                          bg=BG, fg="#698073", font=("Segoe UI", 8))
        self.last_update_label.pack(side="right", padx=(0, 15))
        tk.Label(footer, text=f"FOGLABS  ·  v{VERSION}", bg=BG, fg="#698073",
                 font=("Segoe UI", 8, "bold")).pack(side="right")

        # Helpful keyboard shortcuts for frequent actions.
        self.root.bind("<Control-r>", lambda _e: self._request_refresh())
        self.root.bind("<Control-f>", lambda _e: self.search_entry.focus_set())
        self.root.bind("<Control-e>", lambda _e: self._export_csv())

    def _set_status(self, text, color=GREEN):
        self.status.configure(text=self.tr(text), fg=color)
        self.status_color = color
        if hasattr(self, "status_core"):
            self.status_dot.itemconfigure(self.status_core, fill=color)

    def _set_interval(self, _event=None):
        selected = self.interval_var.get()
        intervals = {self.tr("interval_1"): 1.0, self.tr("interval_2"): 2.0, self.tr("interval_5"): 5.0}
        self.sample_interval = intervals.get(selected, 2.0)
        self.wake_event.set()
        self.footer_msg.configure(text=self.tr("interval_set", interval=selected))

    def _copy_selected_pid(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        if len(values) < 2 or not str(values[1]).isdigit():
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(str(values[1]))
        self.footer_msg.configure(text=self.tr("pid_copied", pid=values[1]))

    def _worker_loop(self):
        """Collect metrics off the Tk UI thread to keep the dashboard responsive."""
        try:
            while not self.stop_event.is_set():
                if not self.monitoring:
                    self.wake_event.wait(0.5)
                    self.wake_event.clear()
                    continue
                started = time.monotonic()
                sample = {
                    "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
                    "cpu": self.reader.cpu_percent(),
                    "memory": self.reader.memory(),
                    "gpu": self.reader.gpu_percent(),
                    "disk": self.reader.disk(),
                    "processes": self.reader.processes(40),
                }
                # Keep only the latest complete sample; UI updates never backlog.
                try:
                    self.sample_queue.put_nowait(sample)
                except queue.Full:
                    try:
                        self.sample_queue.get_nowait()
                    except queue.Empty:
                        pass
                    try:
                        self.sample_queue.put_nowait(sample)
                    except queue.Full:
                        pass
                elapsed = time.monotonic() - started
                self.wake_event.wait(max(0.05, self.sample_interval - elapsed))
                self.wake_event.clear()
        except Exception:
            details = traceback.format_exc()
            try:
                write_error_log("[Sampler thread error]\n" + details, append=True)
            except OSError:
                pass
        finally:
            try:
                if self.reader.gpu:
                    self.reader.gpu.close()
            except Exception:
                pass

    def _tick(self):
        if not self.running:
            return
        sample = None
        try:
            while True:
                sample = self.sample_queue.get_nowait()
        except queue.Empty:
            pass
        if sample is not None:
            self._apply_sample(sample)
        if not self.monitoring:
            self._set_status("paused", AMBER)
        elif sample is None and not self.has_sample:
            self._set_status("detecting", GREEN)
        self.after_id = self.root.after(250, self._tick)

    def _apply_sample(self, sample, record_history=True):
        self.has_sample = True
        self.last_sample = sample
        cpu = sample["cpu"]
        mem = sample["memory"]
        gpu = sample["gpu"]
        disk = sample["disk"]
        if cpu is None:
            self.cpu_card.update_metric("…", self.tr("cpu_calibrating"), None)
            if hasattr(self, "chart_live_value"):
                self.chart_live_value.configure(text="CPU  —%", fg=MUTED)
        else:
            c = RED if cpu >= 85 else (AMBER if cpu >= 65 else GREEN)
            self.cpu_card.update_metric(f"{cpu:.0f}%", self.tr("cpu_usage_total"), cpu, c)
            if hasattr(self, "chart_live_value"):
                self.chart_live_value.configure(text=f"CPU  {cpu:.0f}%", fg=c)
            if record_history:
                self.history.append(cpu)
                self.history = self.history[-60:]
            self._draw_chart()
        if mem:
            self.ram_card.update_metric(f"{mem['percent']:.0f}%", f"{fmt_bytes(mem['used'])} {self.tr('used')} / {fmt_bytes(mem['total'])}", mem["percent"], "#79a7ff")
        else:
            self.ram_card.update_metric(self.tr("not_available"), self.tr("memory_not_available"), 0, "#79a7ff")
        if gpu is not None:
            self.gpu_card.update_metric(f"{gpu:.0f}%", self.tr("gpu_peak"), gpu, "#be8cff")
        else:
            self.gpu_card.update_metric(self.tr("not_available"), self.tr("gpu_not_exposed"), 0, "#be8cff")
        if disk:
            self.disk_card.update_metric(f"{disk['percent']:.0f}%", self.tr("disk_free", free=fmt_bytes(disk['free']), drive=disk['drive']), disk["percent"], "#ffd166")
        else:
            self.disk_card.update_metric(self.tr("not_available"), self.tr("disk_not_available"), 0, "#ffd166")

        if hasattr(self, "info_labels"):
            self.info_labels["device"].configure(text=platform.node() or "PC Windows")
            self.info_labels["operating_system"].configure(text=f"Windows {platform.release()} · {platform.machine()}")
            if "logical_processors" in self.info_labels:
                self.info_labels["logical_processors"].configure(text=f"{os.cpu_count() or self.tr('not_available')} {self.tr('threads')}")
            if "available_ram" in self.info_labels:
                self.info_labels["available_ram"].configure(text=fmt_bytes(mem["available"]) if mem else self.tr("not_available"))
        self.process_rows = sample.get("processes", [])
        self._render_process_table()
        self._set_status("active", GREEN)
        if hasattr(self, "last_update_label"):
            self.last_update_label.configure(text=self.tr("updated_at", time=datetime.now().strftime("%H:%M:%S")))
        if record_history:
            self.sample_history.append({
                "timestamp": sample["timestamp"],
                "cpu_pct": cpu,
                "ram_pct": mem.get("percent") if mem else None,
                "ram_used_bytes": mem.get("used") if mem else None,
                "ram_total_bytes": mem.get("total") if mem else None,
                "gpu_pct": gpu,
                "disk_pct": disk.get("percent") if disk else None,
                "disk_free_bytes": disk.get("free") if disk else None,
            })
            self.sample_history = self.sample_history[-1800:]

    def _render_process_table(self):
        """Update Treeview rows in place to avoid flicker and preserve selection."""
        if not hasattr(self, "tree"):
            return
        query = self.search_var.get().strip().lower() if hasattr(self, "search_var") else ""
        rows = [r for r in self.process_rows if query in r[0].lower() or query in str(r[1])]
        if hasattr(self, "process_count"):
            self.process_count.configure(text=self.tr("process_count_one" if len(rows) == 1 else "process_count_many", count=len(rows)))
        key_map = {
            "name": lambda r: r[0].lower(),
            "pid": lambda r: r[1],
            "memory": lambda r: r[2],
        }
        rows.sort(key=key_map.get(self.sort_column, key_map["memory"]), reverse=self.sort_reverse)
        shown = rows[:40]

        if not shown:
            # Keep one stable placeholder instead of deleting/re-creating the whole table.
            for iid in self.tree.get_children():
                if iid != "placeholder":
                    self.tree.delete(iid)
            message = self.tr("no_search_results") if query else self.tr("waiting_processes")
            if self.tree.exists("placeholder"):
                self.tree.item("placeholder", values=(message, "—", "—"))
            else:
                self.tree.insert("", "end", iid="placeholder", values=(message, "—", "—"), tags=("odd",))
            self.tree_items = {}
            return

        if self.tree.exists("placeholder"):
            self.tree.delete("placeholder")

        wanted = set()
        for index, (name, pid, memory) in enumerate(shown):
            iid = f"pid_{pid}"
            wanted.add(iid)
            values = (name, pid, fmt_bytes(memory))
            tag = "even" if index % 2 else "odd"
            if self.tree.exists(iid):
                self.tree.item(iid, values=values, tags=(tag,))
            else:
                self.tree.insert("", "end", iid=iid, values=values, tags=(tag,))
            self.tree.move(iid, "", index)

        for iid in self.tree.get_children():
            if iid not in wanted:
                self.tree.delete(iid)
        self.tree_items = {str(pid): f"pid_{pid}" for _, pid, _ in shown}

    def _sort_processes(self, column):
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = column != "name"
        self._render_process_table()

    def _toggle_monitoring(self):
        self.monitoring = not self.monitoring
        if self.monitoring:
            self.pause_button.set_text(self.tr("pause"))
            self._set_status("resuming", GREEN)
            self.wake_event.set()
        else:
            self.pause_button.set_text(self.tr("resume"))
            self._set_status("paused", AMBER)
            self.wake_event.set()

    def _request_refresh(self):
        if not self.monitoring:
            self.monitoring = True
            self.pause_button.set_text(self.tr("pause"))
        self._set_status("updating", GREEN)
        self.wake_event.set()

    def _export_csv(self):
        if not self.sample_history:
            messagebox.showinfo(APP_NAME, self.tr("no_sample_export"), parent=self.root)
            return
        path = filedialog.asksaveasfilename(
            parent=self.root, title=self.tr("export_dialog_title"),
            defaultextension=".csv", initialfile="FogMonitor-report.csv",
            filetypes=[(self.tr("csv_files"), "*.csv"), (self.tr("all_files"), "*.*")]
        )
        if not path:
            return
        fields = ["timestamp", "cpu_pct", "ram_pct", "ram_used_bytes", "ram_total_bytes", "gpu_pct", "disk_pct", "disk_free_bytes"]
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(self.sample_history)
            messagebox.showinfo(APP_NAME, self.tr("export_success", path=path), parent=self.root)
        except OSError as exc:
            messagebox.showerror(APP_NAME, self.tr("export_fail", error=exc), parent=self.root)

    def _animate_ui(self):
        """Run lightweight 20 FPS accents without redrawing complete charts every frame."""
        if not self.running:
            return
        self.animation_phase = ((time.monotonic() - self.animation_started) * 1.8) % (math.pi * 2)
        phase = self.animation_phase
        try:
            pulse = (math.sin(phase) + 1) / 2
            inset = 1 + pulse * 2
            if hasattr(self, "status_ring"):
                self.status_dot.coords(self.status_ring, inset, inset, 16 - inset, 16 - inset)
                self.status_dot.itemconfigure(
                    self.status_ring,
                    outline="#214d30" if not self.monitoring else ("#2c6540" if pulse < .55 else "#57b878")
                )
            if hasattr(self, "logo_orbit"):
                angle = phase * .78
                x = 28 + math.cos(angle) * 22
                y = 28 + math.sin(angle) * 22
                self.logo.coords(self.logo_orbit, x - 2, y - 2, x + 2, y + 2)
            for card in (getattr(self, "cpu_card", None), getattr(self, "ram_card", None),
                         getattr(self, "gpu_card", None), getattr(self, "disk_card", None)):
                if card:
                    card.pulse_sparkline(phase)
            if self.chart_point and self.chart_ring:
                x, y = self.chart_point
                radius = 4.2 + pulse * 1.4
                self.chart.coords(self.chart_ring, x - radius, y - radius, x + radius, y + radius)
        except tk.TclError:
            return
        self.animation_job = self.root.after(50, self._animate_ui)

    def _draw_chart(self):
        c = self.chart
        c.delete("all")
        self.chart_point = None
        self.chart_ring = None
        w = max(10, c.winfo_width()); h = max(10, c.winfo_height())
        left, top, right, bottom = 8, 12, w - 8, h - 12
        for pct in (0, 25, 50, 75, 100):
            y = bottom - (bottom - top) * pct / 100
            c.create_line(left, y, right, y, fill="#26372d", dash=(2, 6))
            c.create_text(right - 2, y - 5, text=f"{pct}%", fill="#71877a", anchor="e", font=("Consolas", 8))
        if len(self.history) >= 2:
            points = []
            usable_w = right - left
            usable_h = bottom - top
            for i, v in enumerate(self.history):
                x = left + usable_w * i / max(1, len(self.history) - 1)
                y = bottom - usable_h * v / 100
                points.extend((x, y))
            area = [left, bottom, *points, right, bottom]
            c.create_polygon(*area, fill="#173322", outline="", stipple="gray50")
            # Dark underlay gives the line more contrast without expensive effects.
            c.create_line(*points, fill="#275c3b", width=5, smooth=True)
            c.create_line(*points, fill=GREEN, width=2, smooth=True)
            # A single endpoint marker keeps the chart clean while showing the latest sample.
            self.chart_point = (points[-2], points[-1])
            phase = getattr(self, "animation_phase", 0.0)
            pulse = 4.2 + (math.sin(phase) + 1) / 2 * 1.4
            self.chart_ring = c.create_oval(points[-2]-pulse, points[-1]-pulse,
                                            points[-2]+pulse, points[-1]+pulse,
                                            outline="#3c9660", width=1)
            c.create_oval(points[-2]-3, points[-1]-3, points[-2]+3, points[-1]+3,
                          fill=GREEN_SOFT, outline=GREEN, width=1)
        else:
            c.create_text(w / 2, h / 2, text=self.tr("collecting_samples"), fill=MUTED, font=("Segoe UI", 9))

    def _close(self):
        self.running = False
        self.stop_event.set()
        self.wake_event.set()
        if self.after_id:
            try: self.root.after_cancel(self.after_id)
            except tk.TclError: pass
        if self.animation_job:
            try: self.root.after_cancel(self.animation_job)
            except tk.TclError: pass
        self.root.destroy()


def _show_startup_error(title: str, message: str) -> None:
    """Show a native Windows dialog even if Tk failed to initialize."""
    if IS_WINDOWS:
        try:
            ctypes.windll.user32.MessageBoxW(None, message, title, 0x10 | 0x0)
            return
        except Exception:
            pass
    print(message, file=sys.stderr)


def main():
    if not IS_WINDOWS:
        print(TRANSLATIONS[load_language_setting()]["windows_only"])
        return 1

    root = None
    try:
        # Richiede a Windows coordinate DPI coerenti, per mantenere testo e UI nitidi
        # anche su display ad alta densità. Se il processo è già configurato, continua.
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass
        root = tk.Tk()
        FogMonitorApp(root)
        root.mainloop()
        return 0
    except Exception:
        details = traceback.format_exc()
        try:
            log_path = write_error_log("FogMonitor startup/runtime error\n" + details)
        except OSError:
            log_path = "FogMonitor-error.log (impossibile salvare i dettagli)"
        try:
            if root is not None:
                root.destroy()
        except Exception:
            pass
        _show_startup_error(
            TRANSLATIONS[load_language_setting()]["startup_error_title"],
            TRANSLATIONS[load_language_setting()]["startup_error"].format(path=log_path)
        )
        print(details, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
