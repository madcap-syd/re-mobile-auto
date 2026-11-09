#!/usr/bin/env python3
"""
Native Bridge State Reconstructor Module for re-mobile-auto framework
Automates the extraction, segmentation, and processing of native state tokens.
Pattern: token(asset) -> split -> feed(stage, segment) -> drain() -> mangle() -> unlock()
"""

import os
import sys
import subprocess
import tempfile

def run_frida_script(package_name, script_content):
    """Запускает Frida-скрипт и возвращает вывод"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(script_content)
        script_path = f.name
    
    try:
        cmd = ["frida", "-U", "-f", package_name, "-l", script_path, "--no-pause"]
        print(f"[*] Запуск Frida для {package_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "[!] Frida execution timed out (app might be waiting for input)."
    finally:
        os.unlink(script_path)

def generate_solver_script(package_name, asset_name="config.dat"):
    """Генерирует JS-скрипт для реконструкции состояния NativeBridge"""
    return f"""
Java.perform(function() {{
    console.log("[*] === АВТОМАТИЧЕСКИЙ РЕКОНСТРУКТОР NATIVE BRIDGE ===");
    var NB = Java.use("{package_name}.NativeBridge");
    var context = Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();

    try {{
        // 1. Читаем ассет
        var inputStream = context.getAssets().open("{asset_name}");
        var buffer = Java.array('byte', new Array(4096).fill(0));
        var bytesRead = inputStream.read(buffer);
        inputStream.close();
        console.log("[+] Прочитано " + bytesRead + " байт из {asset_name}");

        // 2. Получаем токен
        var tokenHex = NB.token(buffer);
        console.log("[+] Токен получен, длина: " + tokenHex.length + " символов");

        // 3. Разбиваем на 3 сегмента (предполагаем 3 этапа feed)
        var segLen = tokenHex.length / 3;
        var s1 = tokenHex.substring(0, segLen);
        var s2 = tokenHex.substring(segLen, segLen * 2);
        var s3 = tokenHex.substring(segLen * 2);
        
        console.log("[*] Сегментация: [" + s1.length + ", " + s2.length + ", " + s3.length + "]");

        // 4. Кормим этапы
        NB.feed(0, s1);
        NB.feed(1, s2);
        NB.feed(2, s3);
        console.log("[+] Данные переданы в feed()");

        // 5. Собираем и расшифровываем
        var d = NB.drain();
        if (d && d.length === 48) {{
            var mangled = NB.mangle(d);
            var finalResult = NB.unlock(mangled);
            console.log("\\n🚩🚩🚩 РЕЗУЛЬТАТ: " + finalResult + " 🚩🚩🚩\\n");
        }} else {{
            console.log("[-] drain() вернул неожиданный результат: " + (d ? d.length : "null"));
        }}
    }} catch (e) {{
        console.log("[-] Ошибка: " + e);
    }}
    
    // Завершаем процесс после выполнения
    setTimeout(function() {{ java.lang.System.exit(0); }}, 2000);
}});
"""

def main():
    if len(sys.argv) < 2:
        print("Использование: python3 modules/native_bridge_solver.py <package_name> [asset_name]")
        sys.exit(1)
    
    package = sys.argv[1]
    asset = sys.argv[2] if len(sys.argv) > 2 else "config.dat"
    
    script = generate_solver_script(package, asset)
    output = run_frida_script(package, script)
    
    print("\n" + "="*60)
    print("ВЫВОД FRIDA:")
    print("="*60)
    print(output)
    print("="*60)

if __name__ == "__main__":
    main()
