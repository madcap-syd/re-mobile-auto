#!/usr/bin/env python3
"""
Deep APK Inspector Module for re-mobile-auto framework
Detects fake APKs, encrypted entries, and non-standard formats to bypass basic analysis blocks.
"""

import os
import sys
import subprocess

def inspect_file(filepath):
    if not os.path.exists(filepath):
        print(f"❌ Файл {filepath} не найден!")
        sys.exit(1)

    print(f"[*] Глубокий анализ: {filepath}")
    print("="*60)

    # 1. Проверка магических чисел через xxd
    print("[1] Проверка магических чисел (Magic Bytes):")
    result = subprocess.run(['xxd', filepath], capture_output=True, text=True)
    first_line = result.stdout.split('\n')[0] if result.stdout else ""
    print(f"    {first_line}")
    
    if "7f 45 4c 46" in first_line:
        print("    ⚠️ ВНИМАНИЕ: Обнаружена сигнатура ELF (.ELF)! Это не APK, а Linux-бинарник!")
        print("    💡 Рекомендация: Используй radare2, ghidra или strings для анализа.")
        return "ELF"
    elif "50 4b 03 04" in first_line:
        print("    ✅ Сигнатура ZIP/APK подтверждена.")
    else:
        print("    ⚠️ Неизвестная сигнатура!")

    # 2. Попытка прочитать содержимое через 7z
    print("\n[2] Анализ структуры через 7z:")
    result_7z = subprocess.run(['7z', 'l', filepath], capture_output=True, text=True)
    if "encrypted" in result_7z.stderr.lower() or "encrypted" in result_7z.stdout.lower():
        print("    ⚠️ ВНИМАНИЕ: Обнаружены зашифрованные записи внутри архива!")
        print("    💡 Рекомендация: Попробуй подобрать пароль через zip2john или найти ключ в другом файле.")
    else:
        print("    ✅ Архив читается без шифрования.")
        # Выводим первые 10 файлов для контекста
        lines = result_7z.stdout.split('\n')
        print("    Первые файлы в архиве:")
        for line in lines[15:25]: # Пропускаем заголовок 7z
            if line.strip():
                print(f"      {line.strip()}")

    # 3. Проверка через file
    print("\n[3] Системная утилита file:")
    result_file = subprocess.run(['file', filepath], capture_output=True, text=True)
    print(f"    {result_file.stdout.strip()}")

    print("="*60)
    print("[✅] Анализ завершен.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 modules/apk_analyzer/deep_inspect.py <path_to_file>")
        sys.exit(1)
    
    inspect_file(sys.argv[1])
