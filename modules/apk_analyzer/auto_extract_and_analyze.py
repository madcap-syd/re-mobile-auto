#!/usr/bin/env python3
"""
Auto Extract & Analyze Module for re-mobile-auto framework
Automates the extraction of nested/encrypted APKs and performs initial keyword reconnaissance.
"""

import os
import sys
import subprocess
import glob

COMMON_PASSWORDS = ["hackthebox", "infected", "password", "123456", "android"]

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def extract_nested_apk(filepath):
    print(f"[*] Попытка извлечь вложенный APK из: {filepath}")
    dir_path = os.path.dirname(os.path.abspath(filepath))
    
    for pwd in COMMON_PASSWORDS:
        print(f"    Пробую пароль: '{pwd}'...")
        # Используем 7z, так как он лучше работает с зашифрованными ZIP, чем unzip
        code, out, err = run_cmd(f"7z x '{filepath}' -p{pwd} -y -o'{dir_path}'")
        
        if code == 0 and "Everything is Ok" in out:
            print(f"    ✅ Успех! Пароль: '{pwd}'")
            # Ищем извлеченный файл (он будет иметь то же имя или мы найдем новый .apk)
            apks = glob.glob(os.path.join(dir_path, "*.apk"))
            # Фильтруем, чтобы найти тот, который НЕ является исходным зашифрованным архивом
            # (обычно 7z извлекает файл с тем же именем, перезаписывая или создавая новый)
            # Для надежности проверим размер: вложенный APK должен быть больше (распакованный)
            for apk in apks:
                if os.path.getsize(apk) > os.path.getsize(filepath):
                    return apk
            return apks[0] if apks else None
            
    print("    ❌ Не удалось подобрать пароль из списка.")
    return None

def decompile_and_search(apk_path):
    print(f"\n[*] Декомпиляция {apk_path} через JADX...")
    out_dir = apk_path.replace(".apk", "_src")
    
    # Очищаем старую папку, если есть
    run_cmd(f"rm -rf '{out_dir}'")
    
    code, out, err = run_cmd(f"jadx -d '{out_dir}' '{apk_path}' 2>/dev/null")
    if code == 0 or os.path.exists(out_dir):
        print("    ✅ Декомпиляция успешна!")
    else:
        print("    ⚠️ JADX выдал ошибки, но продолжаем анализ...")

    print("\n[*] Поиск ключевых слов (route, process, ticket, support, record, standard, http, flag)...")
    keywords = "route|process|ticket|support|record|standard|http|flag"
    code, out, err = run_cmd(f"grep -rinE '{keywords}' '{out_dir}/' 2>/dev/null | head -40")
    
    if out.strip():
        print("    🎯 НАЙДЕНО:")
        print("-" * 60)
        print(out.strip())
        print("-" * 60)
    else:
        print("    Ничего не найдено по ключевым словам.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 modules/apk_analyzer/auto_extract_and_analyze.py <path_to_encrypted_apk>")
        sys.exit(1)
    
    target = sys.argv[1]
    extracted_apk = extract_nested_apk(target)
    
    if extracted_apk:
        print(f"\n[+] Извлеченный APK: {extracted_apk}")
        decompile_and_search(extracted_apk)
    else:
        print("\n❌ Не удалось извлечь APK для анализа.")
