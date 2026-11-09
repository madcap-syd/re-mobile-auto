#!/usr/bin/env python3
"""
OWASP UnCrackable Level 4 Automated Bypass Module
Part of the re-mobile-auto framework (github.com/madcap-syd/re-mobile-auto)

Этот модуль автоматически применяет 3 хирургических Smali-патча для обхода защиты:
1. Удаление деления на ноль в onCreate (ArithmeticException trap).
2. Удаление ловушки notify() в onClick (IllegalMonitorStateException trap).
3. Замена вызова нативного метода gXftm3iswpkVgBNDUp на хардкод байт-массива 
   (обход SIGSEGV в libnative-lib.so).
"""

import os
import sys
import subprocess
import re

def run_cmd(cmd, cwd=None):
    """Выполняет команду и возвращает вывод"""
    print(f"[*] Выполняю: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Ошибка: {result.stderr}")
        sys.exit(1)
    return result.stdout

def patch_level4(apk_path):
    if not os.path.exists(apk_path):
        print(f"❌ Файл {apk_path} не найден!")
        sys.exit(1)

    app_name = os.path.basename(apk_path).replace(".apk", "")
    decomp_dir = f"{app_name}_patched_src"
    
    print(f"\n[+] Шаг 1: Декомпиляция {apk_path} через apktool...")
    run_cmd(["apktool", "d", "-f", "-o", decomp_dir, apk_path])

    print("[+] Шаг 2: Применение хирургических Smali-патчей...")
    
    # ПАТЧ 1: Удаление деления на ноль в MainActivity.smali
    main_smali = os.path.join(decomp_dir, "smali", "re", "pwnme", "MainActivity.smali")
    if os.path.exists(main_smali):
        with open(main_smali, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Заменяем опасную конструкцию на безопасную
        content = re.sub(
            r'const/16\s+v1,\s+0x539\s*\n\s*div-int/lit8\s+v1,\s+v1,\s+0x0', 
            'const/16 v1, 0x1\n\n    nop  # [FRAMEWORK] Div-by-zero trap removed', 
            content
        )
        
        with open(main_smali, "w", encoding="utf-8") as f:
            f.write(content)
        print("   ✅ Патч 1: Деление на ноль в onCreate удалено.")
    else:
        print("   ⚠️ MainActivity.smali не найден. Проверьте имя пакета.")

    # ПАТЧ 2 и 3: Модификация onClick в MainActivity$a.smali
    click_smali = os.path.join(decomp_dir, "smali", "re", "pwnme", "MainActivity$a.smali")
    if os.path.exists(click_smali):
        with open(click_smali, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Патч 2: Удаляем notify() ловушку
        content = content.replace(
            "invoke-virtual {v7}, Ljava/lang/Object;->notify()V", 
            "nop  # [FRAMEWORK] Anti-debug notify() trap removed"
        )
        
        # Патч 3: Заменяем вызов нативного метода на хардкод массива байт (0x99 = зеленый цвет)
        old_native = "invoke-virtual {v7, v0, v8}, Lre/pwnme/MainActivity;->gXftm3iswpkVgBNDUp([BB)[B"
        new_hardcode = """# [FRAMEWORK PATCH] Bypass native SIGSEGV in libnative-lib.so
    const/16 v7, 0x10
    new-array v7, v7, [B
    const/16 v8, 0x99
    const/4 v9, 0x0
    :fill_loop
    aput-byte v8, v7, v9
    add-int/lit8 v9, v9, 0x1
    const/16 v10, 0x10
    if-lt v9, v10, :fill_loop"""
        
        content = content.replace(old_native, new_hardcode)
        
        with open(click_smali, "w", encoding="utf-8") as f:
            f.write(content)
        print("   ✅ Патч 2: Ловушка notify() в onClick удалена.")
        print("   ✅ Патч 3: Нативный вызов заменен на хардкод байт-массива.")
    else:
        print("   ⚠️ MainActivity$a.smali не найден.")

    print("[+] Шаг 3: Сборка патченного APK...")
    patched_apk = f"{app_name}_bypassed.apk"
    run_cmd(["apktool", "b", decomp_dir, "-o", patched_apk])
    
    print(f"\n🎉 ГОТОВО! Патченный APK сохранен как: {os.path.abspath(patched_apk)}")
    print("⚠️ Не забудьте подписать его перед установкой (например, через uber-apk-signer или apksigner).")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 modules/owasp_level4/bypass.py <path_to_apk>")
        print("Пример: python3 modules/owasp_level4/bypass.py UnCrackable-Level4.apk")
        sys.exit(1)
    
    patch_level4(sys.argv[1])
