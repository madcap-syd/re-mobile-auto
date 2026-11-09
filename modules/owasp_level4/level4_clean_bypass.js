Java.perform(function() {
    console.log("[*] === LEVEL 4 CLEAN JAVA BYPASS ACTIVE ===");

    // 1. НЕЙТРАЛИЗУЕМ ПРОВЕРКУ ROOT/DEBUG (чтобы 1337/0 никогда не выполнилось)
    try {
        var RootCheck = Java.use("b.a.a.b"); // Класс проверки из jadx
        
        // Хукаем методы, которые проверяют среду. Заставляем их всегда возвращать false
        var methodsToBypass = ["a", "e", "j"]; 
        
        methodsToBypass.forEach(function(methodName) {
            if (RootCheck[methodName]) {
                RootCheck[methodName].implementation = function() {
                    return false;
                };
            }
        });
        console.log("[+] Root/Debug checks neutralized. 1337/0 will NOT execute.");
    } catch (e) {
        console.log("[-] RootCheck hook warning: " + e);
    }

    // 2. ХУКАЕМ НАТИВНЫЙ МЕТОД ПРЯМО НА УРОВНЕ JAVA (обходим всю нативную обфускацию)
    try {
        var MainActivity = Java.use("re.pwnme.MainActivity");
        
        // Сигнатура из jadx: public native byte[] gXftm3iswpkVgBNDUp(byte[] bArr, byte b2);
        MainActivity.gXftm3iswpkVgBNDUp.implementation = function(bArr, b2) {
            console.log("[*] Intercepted native call: gXftm3iswpkVgBNDUp");
            console.log("[*] Input data length: " + bArr.length);
            
            // Создаем поддельный byte array, где первый байт = 81 (ASCII 'Q')
            // Это точное условие успеха из Java-кода: if (ret == 81)
            var fakeResult = Java.array('byte', [81, 49, 50, 51, 52]); // 'Q', '1', '2', '3', '4'
            
            console.log("[+] Returning fake success byte array (first byte = 81)");
            return fakeResult;
        };
        console.log("[+] Native method gXftm3iswpkVgBNDUp hooked at Java level!");
    } catch (e) {
        console.log("[-] MainActivity native hook warning: " + e);
    }

    console.log("[+] === ALL DEFENSES ACTIVE. APP SHOULD SHOW GREEN TOKEN! ===");
});
