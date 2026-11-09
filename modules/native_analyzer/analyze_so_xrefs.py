#!/usr/bin/env python3
"""
Native SO Analyzer Module for re-mobile-auto framework
Bulletproof string extraction with multiple fallbacks and binary-safe output handling.
"""

import os
import sys
import subprocess
import re
import shutil

def run_cmd_safe(cmd):
    """Выполняет команду и безопасно обрабатывает бинарный вывод"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, check=False)
        # Декодируем с заменой невалидных байтов
        return result.stdout.decode('utf-8', errors='replace')
    except Exception as e:
        return ""

def check_tool(name):
    """Проверяет наличие утилиты в PATH"""
    return shutil.which(name) is not None

def analyze_so(so_path):
    if not os.path.exists(so_path):
        print(f"❌ Файл не найден: {so_path}")
        sys.exit(1)

    print(f"[*] Анализ нативной библиотеки: {os.path.basename(so_path)}")
    print(f"    Размер: {os.path.getsize(so_path)} байт")
    print("=" * 70)
    
    keywords = ["htb{", "flag", "unavailable", "error", "success", "token", "secret", "key", "invalid", "noob", "detour", "service"]
    interesting_strings = []
    
    has_rabin2 = check_tool('rabin2')
    has_readelf = check_tool('readelf')
    has_r2 = check_tool('r2')
    
    print(f"[*] Доступные инструменты: rabin2={has_rabin2}, readelf={has_readelf}, r2={has_r2}")
    
    # 1. Пробуем rabin2
    if has_rabin2:
        print("[*] Извлечение строк через rabin2...")
        rabin2_out = run_cmd_safe(f"rabin2 -z '{so_path}'")
        if rabin2_out.strip():
            for line in rabin2_out.split('\n'):
                if any(kw in line.lower() for kw in keywords):
                    vaddr_match = re.search(r'vaddr=(0x[0-9a-fA-F]+)', line)
                    string_match = re.search(r'string=(.+)$', line)
                    if vaddr_match and string_match:
                        interesting_strings.append((vaddr_match.group(1), string_match.group(1).strip()))
            print(f"    [+] rabin2 нашел {len(interesting_strings)} совпадений")
    
    # 2. Fallback на readelf (если rabin2 не дал результатов)
    if not interesting_strings and has_readelf:
        print("[*] Извлечение строк через readelf (fallback)...")
        readelf_out = run_cmd_safe(f"readelf -p .rodata '{so_path}'")
        for line in readelf_out.split('\n'):
            if any(kw in line.lower() for kw in keywords):
                match = re.search(r'\[\s*\d+\]\s+([0-9a-fA-F]+)\s+(.+)', line)
                if match:
                    interesting_strings.append(("0x" + match.group(1), match.group(2).strip()))
        print(f"    [+] readelf нашел {len(interesting_strings)} совпадений")
    
    # 3. Fallback на strings (если ничего не нашли)
    if not interesting_strings:
        print("[*] Извлечение строк через strings (последний fallback)...")
        strings_out = run_cmd_safe(f"strings -t x '{so_path}'")
        for line in strings_out.split('\n'):
            line = line.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            if len(parts) == 2:
                offset, text = parts
                if any(kw in text.lower() for kw in keywords):
                    interesting_strings.append(("0x" + offset, text.strip()))
        print(f"    [+] strings нашел {len(interesting_strings)} совпадений")

    # Удаляем дубликаты
    interesting_strings = list(dict.fromkeys(interesting_strings))

    if not interesting_strings:
        print("    [-] Подозрительных строк не найдено.")
        return

    print(f"\n[+] Найдено {len(interesting_strings)} потенциально интересных строк:")
    print("-" * 70)
    
    for addr, text in interesting_strings:
        if len(text) < 4:
            continue
            
        print(f"\n🎯 Строка: '{text}'")
        print(f"   📍 Адрес (offset): {addr}")
        
        # Ищем XREFs через radare2
        if has_r2:
            xrefs = run_cmd_safe(f"r2 -q -c 'axt @ {addr}' '{so_path}'")
            if xrefs.strip() and "DATA" in xrefs:
                print("   🔗 Перекрестные ссылки (XREFs) найдены:")
                for xref_line in xrefs.strip().split('\n')[:5]:
                    print(f"      {xref_line.strip()}")
                
                first_xref = xrefs.strip().split('\n')[0]
                func_name = first_xref.split()[-1] if len(first_xref.split()) > 1 else "unknown"
                print(f"   💡 Ghidra Tip: Открой функцию '{func_name}' для анализа логики!")
            else:
                print("   ⚠️ Прямых XREFs не найдено (строка может быть data-only).")
                print(f"   💡 Ghidra Tip: В Ghidra нажми Search -> Memory -> введи {addr} и затем 'X' для поиска ссылок.")
        else:
            print("   ⚠️ radare2 (r2) не установлен, XREFs недоступны.")
            print(f"   💡 Ghidra Tip: В Ghidra нажми Search -> Memory -> введи {addr} и затем 'X' для поиска ссылок.")
    
    print("\n" + "=" * 70)
    print("✅ Анализ завершен.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 modules/native_analyzer/analyze_so_xrefs.py <path_to_.so>")
        print("Пример: python3 modules/native_analyzer/analyze_so_xrefs.py workspaces/htb_detour/extracted_libs/lib/x86_64/libdetour.so")
        sys.exit(1)
    analyze_so(sys.argv[1])
