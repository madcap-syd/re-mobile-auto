Java.perform(function() {
    console.log("[*] === LEVEL 4 SYSTEM BYPASS ===");

    // 1. БЛОКИРУЕМ ЗАГРУЗКУ ВРЕДОНОСНЫХ НАТИВНЫХ БИБЛИОТЕК
    var System = Java.use("java.lang.System");
    var originalLoadLibrary = System.loadLibrary;
    
    System.loadLibrary.implementation = function(libname) {
        console.log("[*] System.loadLibrary called for: " + libname);
        if (libname === "native-lib" || libname === "tool-checker") {
            console.log("[+] BLOCKED loading of: " + libname + " (bypassing native anti-frida)");
            return; // Возвращаем управление, НЕ вызывая оригинальную функцию!
        }
        return originalLoadLibrary.call(this, libname);
    };
    console.log("[+] System.loadLibrary hooked.");

    // 2. ПОДМЕНЯЕМ НАТИВНЫЙ МЕТОД НА УРОВНЕ JAVA
    // Поскольку библиотека не загружена, этот хук спасет приложение от UnsatisfiedLinkError
    var MainActivity = Java.use("re.pwnme.MainActivity");
    MainActivity.gXftm3iswpkVgBNDUp.implementation = function(bArr, b2) {
        console.log("[*] Intercepted native call: gXftm3iswpkVgBNDUp");
        console.log("[*] Input length: " + bArr.length);
        
        // Создаем поддельный byte array, где первый байт = 81 (ASCII 'Q')
        var fakeResult = Java.array('byte', [81, 49, 50, 51, 52]); // 'Q', '1', '2', '3', '4'
        
        console.log("[+] Returning fake success byte array (first byte = 81)");
        return fakeResult;
    };
    console.log("[+] Native method gXftm3iswpkVgBNDUp hooked at Java level!");

    // 3. НЕЙТРАЛИЗУЕМ ПРОВЕРКИ ROOT/DEBUG
    try {
        var RootCheck = Java.use("b.a.a.b");
        if (RootCheck.j) RootCheck.j.implementation = function() { return false; };
        if (RootCheck.e) RootCheck.e.implementation = function() { return false; };
        
        var overloads = RootCheck.a.overloads;
        for (var i = 0; i < overloads.length; i++) {
            overloads[i].implementation = function() { return false; };
        }
        console.log("[+] Root/Debug checks neutralized.");
    } catch(e) {
        console.log("[-] RootCheck hook warning: " + e);
    }

    console.log("[+] === ALL DEFENSES ACTIVE. APP WILL LOAD NORMALLY! ===");
});
