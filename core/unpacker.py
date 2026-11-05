"""
core/unpacker.py
Advanced APK unpacking using system or local apktool and jadx.
"""
import subprocess
import shutil
import re
from pathlib import Path
from rich.console import Console

console = Console()

class APKUnpacker:
    def __init__(self):
        self.apktool_cmd = self._find_tool("apktool", "tools/apktool.jar")
        self.jadx_cmd = self._find_tool("jadx", "jadx") # Твой точный путь

        if not self.apktool_cmd:
            raise EnvironmentError("Apktool not found! Place apktool.jar in tools/")
        if not self.jadx_cmd:
            raise EnvironmentError("Jadx not found!")
            
        console.print(f"[dim]Using apktool: {self.apktool_cmd}[/dim]")
        console.print(f"[dim]Using jadx: {self.jadx_cmd}[/dim]")

    def _find_tool(self, sys_name: str, local_path: str) -> str:
        local = Path(local_path)
        if local.exists():
            return str(local.resolve())
        sys_path = shutil.which(sys_name)
        return sys_path if sys_path else None

    def decode_with_apktool(self, apk_path: Path, output_dir: Path):
        console.print("[*] Running apktool to decode resources and manifest...")
        apktool_output = output_dir / "apktool_decoded"
        try:
            cmd = ["java", "-jar", self.apktool_cmd, "d", str(apk_path), "-o", str(apktool_output), "-f"]
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            console.print("[green][+][/green] Apktool decoding successful.")
            return apktool_output
        except subprocess.CalledProcessError as e:
            console.print(f"[red][ERROR][/red] Apktool failed: {e.stderr}")
            return None

    def decompile_with_jadx(self, apk_path: Path, output_dir: Path):
        console.print("[*] Running jadx to decompile to Java source...")
        jadx_output = output_dir / "jadx_sources"
        try:
            subprocess.run([self.jadx_cmd, "-d", str(jadx_output), "-j", "2", str(apk_path)], capture_output=True, text=True, check=True)
            console.print("[green][+][/green] Jadx decompilation successful.")
            return jadx_output
        except subprocess.CalledProcessError as e:
            console.print(f"[red][ERROR][/red] Jadx failed: {e.stderr}")
            return None

    def extract_manifest_info(self, apktool_output: Path) -> dict:
        manifest_path = apktool_output / "AndroidManifest.xml"
        if not manifest_path.exists():
            return {}
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        pkg = re.search(r'package="([^"]+)"', content)
        exported = re.findall(r'<activity[^>]*android:exported="true"[^>]*android:name="([^"]+)"', content)
        return {
            "package_name": pkg.group(1) if pkg else "unknown",
            "manifest_size_kb": round(manifest_path.stat().st_size / 1024, 2),
            "exported_activities_count": len(exported),
            "exported_activities": exported[:5]
        }
