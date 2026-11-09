Java.perform(function() {
    console.log("[*] === LEVEL 4 BULLETPROOF BYPASS ===");

    // 1. НЕЙТРАЛИЗУЕМ ПРОВЕРКИ ROOT/DEBUG (чтобы 1337/0 НИКОГДА не выполнилось)
    try {
        var RootCheck = Java.use("b.a.a.b");
        
        // Хукаем j()
        if (RootCheck.j) {
            RootCheck.j.implementation = function() { return false; };
        }
        
        // Хукаем e()
        if (RootCheck.e) {
            RootCheck.e.implementation = function() { return false; };
        }

        // Хукаем ВСЕ перегрузки метода a(), чтобы точно перехватить нужную
        var overloads = RootCheck.a.overloads;
        for (var i = 0; i < overloads.length; i++) {
            overloads[i].implementation = function() {
                return false;
            };
        }
        console.log("[+] Root/Debug checks neutralized. 1337/0 will NOT execute.");
    } catch (e) {
        console.log("[-] RootCheck hook warning: " + e);
    }

    // 2. ПЕРЕХВАТ НАТИВНОГО МЕТОДА НА УРОВНЕ JAVA (обходим всю обфускацию .so)
    try {
        var MainActivity = Java.use("re.pwnme.MainActivity");
        
        // Сигнатура из jadx: public native byte[] gXftm3iswpkVgBNDUp(byte[] bArr, byte b2)
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

    console.log("[+] === ALL DEFENSES ACTIVE. APP WILL LOAD NORMALLY! ===");
});
