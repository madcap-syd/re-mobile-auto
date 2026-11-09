#!/usr/bin/env python3
"""
SSL Pinning Bypass Module for re-mobile-auto framework
Uses 'dumpsys' to find PID and attaches via '-p'. 
This completely bypasses the Frida 16.x 'system_server' spawn bug on Android 13 emulators,
while 'debuggable=true' guarantees ptrace access is allowed.
"""

import os
import sys
import subprocess
import time
import re

def find_pid_via_dumpsys(package_name):
    """Находит PID приложения через dumpsys (обходит hidepid=2 в Android 13+)"""
    result = subprocess.run(
        ["adb", "shell", "dumpsys", "activity", "processes"],
        capture_output=True, text=True
    )
    
    # Ищем строку вида "1234:re.pwnme/u0a..."
    pattern = r"(\d+):\s*" + re.escape(package_name)
    match = re.search(pattern, result.stdout)
    
    if match:
        return match.group(1)
    return None

def run_ssl_bypass(package_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    js_script = os.path.join(script_dir, "unpinning.js")
    
    if not os.path.exists(js_script):
        print(f"❌ Скрипт не найден: {js_script}")
        sys.exit(1)

    print(f"[*] Подготовка обхода SSL Pinning для: {package_name}")
    print("[*] Приложение является отлаживаемым (debuggable=true).")
    print("[*] Используем подключение по PID (-p), чтобы обойти баг 'system_server' во Frida 16.x.")
    
    # 1. Запускаем приложение
    print("[*] Запуск приложения через ADB...")
    activity = f"{package_name}/.MainActivity" if "pwnme" in package_name else package_name
    subprocess.run(["adb", "shell", "am", "start", "-n", activity], capture_output=True)
    time.sleep(3) # Даем время на полный запуск
    
    # 2. Ищем PID через dumpsys
    print("[*] Поиск PID через dumpsys...")
    pid = find_pid_via_dumpsys(package_name)
    
    if not pid:
        print(f"❌ Не удалось найти PID для {package_name}.")
        print("💡 Ручная проверка: adb shell dumpsys activity processes | grep " + package_name)
        sys.exit(1)
        
    print(f"[+] Приложение успешно запущено, найден PID: {pid}")
    
    # 3. Инжектим Frida по PID (это обходит баг эмулятора со spawn)
    print("[*] Инжекция Frida-скрипта по PID...")
    cmd = ["frida", "-U", "-p", pid, "-l", js_script]
    
    print(f"[*] Выполняю: {' '.join(cmd)}\n")
    print("="*60)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[!] Сеанс Frida завершен пользователем.")
    except FileNotFoundError:
        print("❌ Ошибка: Frida не найдена. Убедитесь, что она установлена (pip install frida-tools).")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 modules/ssl_pinning/bypass.py <package_name>")
        sys.exit(1)
    
    run_ssl_bypass(sys.argv[1])
