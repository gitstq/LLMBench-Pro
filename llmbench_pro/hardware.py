"""
Hardware Detection Module
Detects CPU, GPU, Memory, and Storage information
"""

import platform
import subprocess
import os
import re
from typing import Dict, Any, List, Optional
from pathlib import Path


class HardwareDetector:
    """
    System Hardware Detector
    
    Detects and reports hardware configuration for LLM inference optimization
    """
    
    def __init__(self):
        self.system = platform.system()
        self.machine = platform.machine()
        
    def detect(self) -> Dict[str, Any]:
        """
        Detect all hardware components
        
        Returns:
            Dictionary containing complete hardware information
        """
        return {
            "system": self._get_system_info(),
            "cpu": self._detect_cpu(),
            "memory": self._detect_memory(),
            "gpu": self._detect_gpu(),
            "storage": self._detect_storage(),
            "recommendations": self._generate_recommendations(),
        }
    
    def _get_system_info(self) -> Dict[str, str]:
        """Get basic system information"""
        return {
            "os": self.system,
            "arch": self.machine,
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        }
    
    def _detect_cpu(self) -> Dict[str, Any]:
        """Detect CPU information"""
        cpu_info = {
            "model": "Unknown",
            "cores": 0,
            "threads": 0,
            "frequency": 0,
            "architecture": self.machine,
        }
        
        try:
            if self.system == "Linux":
                cpu_info = self._detect_cpu_linux()
            elif self.system == "Darwin":
                cpu_info = self._detect_cpu_macos()
            elif self.system == "Windows":
                cpu_info = self._detect_cpu_windows()
        except Exception:
            pass
            
        # Fallback to os.cpu_count()
        if cpu_info["cores"] == 0:
            cpu_info["cores"] = os.cpu_count() or 1
            cpu_info["threads"] = cpu_info["cores"]
            
        return cpu_info
    
    def _detect_cpu_linux(self) -> Dict[str, Any]:
        """Detect CPU on Linux"""
        cpu_info = {"model": "Unknown", "cores": 0, "threads": 0, "frequency": 0}
        
        try:
            # Read from /proc/cpuinfo
            with open("/proc/cpuinfo", "r") as f:
                content = f.read()
                
            # Get model name
            model_match = re.search(r"model name\s*:\s*(.+)", content)
            if model_match:
                cpu_info["model"] = model_match.group(1).strip()
            
            # Count cores and threads
            cores = len(re.findall(r"processor\s*:", content))
            cpu_info["threads"] = cores
            
            # Try to get physical cores
            siblings_match = re.search(r"siblings\s*:\s*(\d+)", content)
            cores_match = re.search(r"cpu cores\s*:\s*(\d+)", content)
            if cores_match:
                cpu_info["cores"] = int(cores_match.group(1))
            else:
                cpu_info["cores"] = cores
            
            # Get frequency
            freq_match = re.search(r"cpu MHz\s*:\s*([\d.]+)", content)
            if freq_match:
                cpu_info["frequency"] = int(float(freq_match.group(1)))
                
        except Exception:
            pass
            
        return cpu_info
    
    def _detect_cpu_macos(self) -> Dict[str, Any]:
        """Detect CPU on macOS"""
        cpu_info = {"model": "Unknown", "cores": 0, "threads": 0, "frequency": 0}
        
        try:
            # Get CPU brand string
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                cpu_info["model"] = result.stdout.strip()
            
            # Get core count
            result = subprocess.run(
                ["sysctl", "-n", "hw.physicalcpu"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                cpu_info["cores"] = int(result.stdout.strip())
            
            result = subprocess.run(
                ["sysctl", "-n", "hw.logicalcpu"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                cpu_info["threads"] = int(result.stdout.strip())
            
            # Get frequency (approximate)
            result = subprocess.run(
                ["sysctl", "-n", "hw.cpufrequency"],
                capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                cpu_info["frequency"] = int(result.stdout.strip()) // 1_000_000
                
        except Exception:
            pass
            
        return cpu_info
    
    def _detect_cpu_windows(self) -> Dict[str, Any]:
        """Detect CPU on Windows"""
        cpu_info = {"model": "Unknown", "cores": 0, "threads": 0, "frequency": 0}
        
        try:
            result = subprocess.run(
                ["wmic", "cpu", "get", "Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                if len(lines) >= 2:
                    parts = lines[1].split()
                    if len(parts) >= 4:
                        cpu_info["model"] = parts[0]
                        cpu_info["frequency"] = int(parts[1])
                        cpu_info["cores"] = int(parts[2])
                        cpu_info["threads"] = int(parts[3])
        except Exception:
            pass
            
        return cpu_info
    
    def _detect_memory(self) -> Dict[str, Any]:
        """Detect system memory"""
        memory_info = {
            "total_gb": 0,
            "available_gb": 0,
            "used_percent": 0,
        }
        
        try:
            if self.system == "Linux":
                with open("/proc/meminfo", "r") as f:
                    content = f.read()
                
                total_match = re.search(r"MemTotal:\s*(\d+)", content)
                available_match = re.search(r"MemAvailable:\s*(\d+)", content)
                
                if total_match:
                    total_kb = int(total_match.group(1))
                    memory_info["total_gb"] = round(total_kb / 1024 / 1024, 1)
                
                if available_match:
                    available_kb = int(available_match.group(1))
                    memory_info["available_gb"] = round(available_kb / 1024 / 1024, 1)
                    
            elif self.system == "Darwin":
                result = subprocess.run(
                    ["sysctl", "-n", "hw.memsize"],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    total_bytes = int(result.stdout.strip())
                    memory_info["total_gb"] = round(total_bytes / 1024**3, 1)
                
                # Get available memory using vm_stat
                result = subprocess.run(["vm_stat"], capture_output=True, text=True)
                if result.returncode == 0:
                    free_match = re.search(r"free\s*:\s*(\d+)", result.stdout)
                    if free_match:
                        free_pages = int(free_match.group(1))
                        memory_info["available_gb"] = round(free_pages * 4096 / 1024**3, 1)
                        
            elif self.system == "Windows":
                import ctypes
                kernel32 = ctypes.windll.kernel32
                c_ulonglong = ctypes.c_ulonglong
                
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", c_ulonglong),
                        ("ullAvailPhys", c_ulonglong),
                        ("ullTotalPageFile", c_ulonglong),
                        ("ullAvailPageFile", c_ulonglong),
                        ("ullTotalVirtual", c_ulonglong),
                        ("ullAvailVirtual", c_ulonglong),
                        ("ullAvailExtendedVirtual", c_ulonglong),
                    ]
                
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(stat)
                kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                
                memory_info["total_gb"] = round(stat.ullTotalPhys / 1024**3, 1)
                memory_info["available_gb"] = round(stat.ullAvailPhys / 1024**3, 1)
                memory_info["used_percent"] = stat.dwMemoryLoad
                
        except Exception:
            pass
            
        if memory_info["total_gb"] > 0 and memory_info["available_gb"] > 0:
            memory_info["used_percent"] = round(
                (1 - memory_info["available_gb"] / memory_info["total_gb"]) * 100, 1
            )
            
        return memory_info
    
    def _detect_gpu(self) -> List[Dict[str, Any]]:
        """Detect GPU information"""
        gpus = []
        
        # Try NVIDIA GPU detection
        nvidia_gpus = self._detect_nvidia_gpu()
        gpus.extend(nvidia_gpus)
        
        # Try AMD GPU detection
        amd_gpus = self._detect_amd_gpu()
        gpus.extend(amd_gpus)
        
        # Try Apple Silicon detection
        if self.system == "Darwin":
            apple_gpu = self._detect_apple_silicon()
            if apple_gpu:
                gpus.append(apple_gpu)
                
        return gpus
    
    def _detect_nvidia_gpu(self) -> List[Dict[str, Any]]:
        """Detect NVIDIA GPUs using nvidia-smi"""
        gpus = []
        
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) >= 3:
                        vram_str = parts[1]
                        vram_match = re.search(r"(\d+)", vram_str)
                        vram_mb = int(vram_match.group(1)) if vram_match else 0
                        
                        gpus.append({
                            "vendor": "NVIDIA",
                            "name": parts[0],
                            "vram_gb": round(vram_mb / 1024, 1),
                            "vram_mb": vram_mb,
                            "driver": parts[2],
                            "type": "cuda",
                        })
        except Exception:
            pass
            
        return gpus
    
    def _detect_amd_gpu(self) -> List[Dict[str, Any]]:
        """Detect AMD GPUs"""
        gpus = []
        
        try:
            if self.system == "Linux":
                # Check for AMD GPU in /sys
                amd_path = Path("/sys/class/drm")
                if amd_path.exists():
                    for card in amd_path.glob("card*/device"):
                        vendor_file = card / "vendor"
                        if vendor_file.exists():
                            vendor = vendor_file.read_text().strip()
                            if vendor == "0x1002":  # AMD vendor ID
                                name_file = card / "product_name"
                                if name_file.exists():
                                    gpus.append({
                                        "vendor": "AMD",
                                        "name": name_file.read_text().strip(),
                                        "vram_gb": "Unknown",
                                        "type": "rocm",
                                    })
        except Exception:
            pass
            
        return gpus
    
    def _detect_apple_silicon(self) -> Optional[Dict[str, Any]]:
        """Detect Apple Silicon GPU"""
        try:
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                brand = result.stdout.strip()
                if "Apple" in brand or "M1" in brand or "M2" in brand or "M3" in brand or "M4" in brand:
                    # Get unified memory
                    mem_result = subprocess.run(
                        ["sysctl", "-n", "hw.memsize"],
                        capture_output=True, text=True
                    )
                    total_mem = 0
                    if mem_result.returncode == 0:
                        total_mem = int(mem_result.stdout.strip())
                    
                    return {
                        "vendor": "Apple",
                        "name": brand,
                        "vram_gb": round(total_mem / 1024**3, 1),  # Unified memory
                        "type": "metal",
                    }
        except Exception:
            pass
            
        return None
    
    def _detect_storage(self) -> Dict[str, Any]:
        """Detect storage information"""
        storage_info = {
            "total_gb": 0,
            "free_gb": 0,
            "used_percent": 0,
        }
        
        try:
            if self.system == "Windows":
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                total_bytes = ctypes.c_ulonglong(0)
                total_free_bytes = ctypes.c_ulonglong(0)
                
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p("C:\\"),
                    ctypes.byref(free_bytes),
                    ctypes.byref(total_bytes),
                    ctypes.byref(total_free_bytes),
                )
                
                storage_info["total_gb"] = round(total_bytes.value / 1024**3, 1)
                storage_info["free_gb"] = round(free_bytes.value / 1024**3, 1)
            else:
                stat = os.statvfs("/")
                storage_info["total_gb"] = round(stat.f_blocks * stat.f_frsize / 1024**3, 1)
                storage_info["free_gb"] = round(stat.f_bavail * stat.f_frsize / 1024**3, 1)
                
            if storage_info["total_gb"] > 0:
                storage_info["used_percent"] = round(
                    (1 - storage_info["free_gb"] / storage_info["total_gb"]) * 100, 1
                )
                
        except Exception:
            pass
            
        return storage_info
    
    def _generate_recommendations(self) -> Dict[str, Any]:
        """Generate hardware-based recommendations"""
        recommendations = {
            "max_model_size_gb": 0,
            "suggested_quantization": "Q4_K_M",
            "suggested_framework": "auto",
            "warnings": [],
        }
        
        # Get hardware info
        memory = self._detect_memory()
        gpus = self._detect_gpu()
        
        total_vram = sum(gpu.get("vram_gb", 0) for gpu in gpus if isinstance(gpu.get("vram_gb"), (int, float)))
        system_ram = memory.get("total_gb", 0)
        
        # Calculate max model size
        if gpus and total_vram > 0:
            # GPU inference
            recommendations["max_model_size_gb"] = int(total_vram * 0.8)  # 80% of VRAM
            recommendations["suggested_framework"] = "cuda" if gpus[0].get("type") == "cuda" else "metal"
            
            if total_vram < 8:
                recommendations["suggested_quantization"] = "Q4_K_M"
                recommendations["warnings"].append("Limited VRAM, recommend Q4 quantization")
            elif total_vram < 16:
                recommendations["suggested_quantization"] = "Q5_K_M"
            else:
                recommendations["suggested_quantization"] = "Q8_0 or FP16"
        else:
            # CPU inference
            recommendations["max_model_size_gb"] = int(system_ram * 0.5)  # 50% of RAM
            recommendations["suggested_framework"] = "cpu"
            recommendations["warnings"].append("No GPU detected, using CPU inference (slower)")
            
            if system_ram < 16:
                recommendations["suggested_quantization"] = "Q4_K_M"
                recommendations["warnings"].append("Limited RAM, recommend Q4 quantization")
            elif system_ram < 32:
                recommendations["suggested_quantization"] = "Q5_K_M"
            else:
                recommendations["suggested_quantization"] = "Q8_0"
                
        return recommendations
