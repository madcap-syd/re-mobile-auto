Java.perform(function() {
    console.log("[*] Level 3 Anti-Frida & Native Bypass Active");

    // 1. НЕЙТРАЛИЗУЕМ КРАШ
    var goodbyePtr = Module.findExportByName("libfoo.so", "goodbye");
    if (goodbyePtr) {
        console.log("[+] Found 'goodbye' at: " + goodbyePtr);
        Interceptor.replace(goodbyePtr, new NativeCallback(function() {
            console.log("[!] 'goodbye()' triggered by anti-debug! Neutralizing crash...");
            // Просто возвращаем управление, не вызывая raise(SIGABRT)
        }, 'void', []));
    } else {
        console.log("[-] 'goodbye' export not found. Trying alternative...");
    }

    // 2. ОБХОДИМ ПРОВЕРКУ ПАРОЛЯ
    var checkPtr = Module.findExportByName("libfoo.so", "Java_sg_vantagepoint_uncrackable3_CodeCheck_bar");
    if (checkPtr) {
        console.log("[+] Found 'CodeCheck_bar' at: " + checkPtr);
        Interceptor.attach(checkPtr, {
            onEnter: function(args) {
                console.log("[*] Native verification called!");
            },
            onLeave: function(retval) {
                console.log("[+] Forcing CodeCheck_bar to return TRUE (1)");
                retval.replace(1);
            }
        });
    } else {
        console.log("[-] 'CodeCheck_bar' export not found.");
    }
    
    console.log("[+] All hooks active! App should stay alive.");
});
