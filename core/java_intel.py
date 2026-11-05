import re
from pathlib import Path
from rich.console import Console

console = Console()

PATTERNS = {
    "api_keys": re.compile(r'(?i)(api[_-]?key|token|secret|password|auth)[\s]*[:=][\s]*["\']([A-Za-z0-9_\-]{8,})["\']'),
    "urls": re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s"\'>]*'),
    "crypto": re.compile(r'(?i)(javax\.crypto\.|MessageDigest|Cipher|SecretKeySpec|AES|RSA)'),
    "root_detection": re.compile(r'(?i)(root|superuser|\bsu\b|test-keys|build\.fingerprint|isDeviceRooted)'),
    "hardcoded_ips": re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
}

def scan_directory_for_secrets(source_dir: Path) -> dict:
    console.print(f"[*] Scanning {source_dir} for secrets...")
    findings = {key: [] for key in PATTERNS.keys()}
    files_scanned = 0
    for java_file in source_dir.rglob("*.java"):
        files_scanned += 1
        try:
            with open(java_file, "r", encoding="utf-8", errors="ignore") as f_in:
                content = f_in.read()
            for pattern_name, pattern in PATTERNS.items():
                for match in pattern.findall(content):
                    val = match[1] if isinstance(match, tuple) and len(match) > 1 else match
                    val_str = str(val).strip()
                    if val_str and val_str not in [x["value"] for x in findings[pattern_name]]:
                        findings[pattern_name].append({"file": str(java_file.relative_to(source_dir)), "value": val_str[:100]})
        except Exception:
            continue
    console.print(f"[green][+][/green] Scanned {files_scanned} Java files.")
    return {k: v for k, v in findings.items() if v}
