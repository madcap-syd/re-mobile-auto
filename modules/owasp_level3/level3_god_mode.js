Java.perform(function() {
    console.log("[*] === LEVEL 3 GOD MODE ACTIVATED ===");

    // === ЧАСТЬ 1: JAVA ROOT DETECTION BYPASS ===
    try {
        var RootDetection = Java.use("sg.vantagepoint.util.RootDetection");
        RootDetection.checkRoot1.implementation = function() { return false; };
        RootDetection.checkRoot2.implementation = function() { return false; };
        RootDetection.checkRoot3.implementation = function() { return false; };
        console.log("[+] Java Root Detection bypassed");
    } catch(e) {}

    // === ЧАСТЬ 2: ANTI-FRIDA BYPASS ===
    var strstrPtr = Module.findExportByName("libc.so", "strstr");
    if (strstrPtr) {
        Interceptor.attach(strstrPtr, {
            onEnter: function(args) {
                this.haystack = args[0].readCString();
                this.needle = args[1].readCString();
            },
            onLeave: function(retval) {
                if (this.needle && (this.needle.indexOf("frida") !== -1 || 
                                    this.needle.indexOf("gum") !== -1 || 
                                    this.needle.indexOf("xposed") !== -1)) {
                    retval.replace(ptr(0));
                }
            }
        });
        console.log("[+] strstr hooked to hide Frida");
    }

    var propGetPtr = Module.findExportByName("libc.so", "__system_property_get");
    if (propGetPtr) {
        Interceptor.attach(propGetPtr, {
            onEnter: function(args) {
                this.name = args[0].readCString();
                this.value = args[1];
            },
            onLeave: function(retval) {
                if (this.name && this.name.indexOf("debuggable") !== -1) {
                    Memory.writeUtf8String(this.value, "0");
                }
            }
        });
        console.log("[+] __system_property_get hooked");
    }

    // Нейтрализация goodbye()
    setTimeout(function() {
        var libfoo = Module.findBaseAddress("libfoo.so");
        if (libfoo) {
            var goodbyeAddr = libfoo.add(0x3000);
            Interceptor.replace(goodbyeAddr, new NativeCallback(function() {
                console.log("[!] goodbye() neutralized");
            }, 'void', []));
        }
    }, 500);

    // === ЧАСТЬ 3: NATIVE PASSWORD CHECK BYPASS ===
    console.log("[*] Searching for password check function...");
    
    // Пробуем найти функцию проверки по имени экспорта
    var checkPtr = Module.findExportByName("libfoo.so", "Java_sg_vantagepoint_uncrackable3_CodeCheck_bar");
    
    if (checkPtr) {
        console.log("[+] Found CodeCheck_bar at: " + checkPtr);
        Interceptor.attach(checkPtr, {
            onEnter: function(args) {
                console.log("[*] Password verification called!");
                // Пытаемся прочитать входную строку
                try {
                    var env = Java.vm.getEnv();
                    var inputStr = env.getStringUtfChars(args[2], null).readCString();
                    console.log("[*] User input: " + inputStr);
                } catch(e) {}
            },
            onLeave: function(retval) {
                console.log("[+] FORCING PASSWORD CHECK TO RETURN TRUE (1)");
                retval.replace(1);
            }
        });
    } else {
        console.log("[-] CodeCheck_bar not found by name, trying alternative methods...");
        // Если не нашли по имени, перехватываем memcmp (сравнение строк)
        var memcmpPtr = Module.findExportByName("libc.so", "memcmp");
        if (memcmpPtr) {
            Interceptor.attach(memcmpPtr, {
                onEnter: function(args) {
                    var s1 = args[0].readCString(32);
                    var s2 = args[1].readCString(32);
                    if (s1 && s2 && (s1.indexOf("test") !== -1 || s2.indexOf("test") !== -1)) {
                        console.log("[!] String comparison detected!");
                        console.log("    String 1: " + s1);
                        console.log("    String 2: " + s2);
                    }
                }
            });
        }
    }

    console.log("[+] === GOD MODE READY ===");
    console.log("[*] Enter ANY text and press VERIFY to win!");
});
