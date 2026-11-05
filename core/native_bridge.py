import os
import subprocess
from pathlib import Path
from rich.console import Console
import json

console = Console()

GHIDRA_ANALYZER = os.environ.get("GHIDRA_ANALYZER", "/app/core/ghidra_analyzer.py")

def analyze_native_libs(unpacked_dir: Path, report_dir: Path):
    console.print("[*] Scanning for native libraries (.so)...")
    so_files = list(unpacked_dir.rglob("*.so"))
    
    if not so_files:
        console.print("[yellow][*] No native libraries found.[/yellow]")
        return []
        
    console.print(f"[green][+][/green] Found {len(so_files)} native library(ies).")
    
    native_intel = []
    for so_file in so_files:
        rel_path = so_file.relative_to(unpacked_dir)
        console.print(f"  -> [cyan]{rel_path}[/cyan]")
        
        try:
            result = subprocess.run(["file", str(so_file)], capture_output=True, text=True)
            arch_info = "Unknown"
            if "ARM aarch64" in result.stdout or "ARM 64" in result.stdout:
                arch_info = "ARM64"
            elif "ARM" in result.stdout:
                arch_info = "ARM32"
            elif "x86-64" in result.stdout:
                arch_info = "x86_64"
            elif "x86" in result.stdout:
                arch_info = "x86"
                
            lib_data = {
                "file": str(rel_path),
                "absolute_path": str(so_file.absolute()),
                "architecture": arch_info,
                "ghidra_findings": []
            }
            
            # Запускаем наш рабочий ghidra_analyzer.py
            if Path(GHIDRA_ANALYZER).exists() and arch_info == "ARM64": # Для теста берем ARM64
                console.print(f"    [*] Running Ghidra analyzer on {rel_path}...")
                ghidra_out = subprocess.run(
                    ["python3", GHIDRA_ANALYZER, str(so_file.absolute())],
                    capture_output=True, text=True, timeout=300
                )
                
                # Парсим вывод для сохранения в JSON (ищем строки с "->")
                for line in ghidra_out.stdout.split('\n'):
                    if "->" in line and "@" in line:
                        lib_data["ghidra_findings"].append(line.strip())
                        
            native_intel.append(lib_data)
        except Exception as e:
            native_intel.append({"file": str(rel_path), "error": str(e)})

    return native_intel
