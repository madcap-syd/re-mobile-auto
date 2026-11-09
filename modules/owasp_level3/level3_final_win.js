Java.perform(function() {
    console.log("[*] === LEVEL 3 GUARANTEED WIN SCRIPT ===");

    // 1. JAVA ROOT DETECTION BYPASS
    try {
        var RootDetection = Java.use("sg.vantagepoint.util.RootDetection");
        RootDetection.checkRoot1.implementation = function() { return false; };
        RootDetection.checkRoot2.implementation = function() { return false; };
        RootDetection.checkRoot3.implementation = function() { return false; };
        console.log("[+] Java Root Detection bypassed");
    } catch(e) { console.log("[-] RootDetection error: " + e); }

    // 2. ANTI-FRIDA BYPASS
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
        console.log("[+] strstr hooked");
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

    // 3. НЕЙТРАЛИЗАЦИЯ goodbye()
    setTimeout(function() {
        var libfoo = Module.findBaseAddress("libfoo.so");
        if (libfoo) {
            var goodbyeAddr = libfoo.add(0x3000);
            Interceptor.replace(goodbyeAddr, new NativeCallback(function() {
                console.log("[!] goodbye() neutralized");
            }, 'void', []));
        }
    }, 500);

    // 4. ПРЯМОЙ ХУК НА ФУНКЦИЮ ПРОВЕРКИ ПАРОЛЯ (мы знаем её имя!)
    setTimeout(function() {
        console.log("[*] Hooking password check function...");
        var checkPtr = Module.findExportByName("libfoo.so", "Java_sg_vantagepoint_uncrackable3_CodeCheck_bar");
        
        if (checkPtr) {
            console.log("[+] FOUND CodeCheck_bar at: " + checkPtr);
            Interceptor.attach(checkPtr, {
                onEnter: function(args) {
                    console.log("[*] Password check called!");
                    try {
                        var env = Java.vm.getEnv();
                        var inputStr = env.getStringUtfChars(args[2], null).readCString();
                        console.log("[*] User input: " + inputStr);
                    } catch(e) {}
                },
                onLeave: function(retval) {
                    console.log("[+] FORCING RETURN TO TRUE (1) - YOU WIN!");
                    retval.replace(1);
                }
            });
        } else {
            console.log("[-] CodeCheck_bar not found, trying enumerateExports...");
            // Fallback: перечисляем все экспорты
            var libfoo = Module.findBaseAddress("libfoo.so");
            if (libfoo) {
                var exports = Module.enumerateExports("libfoo.so");
                for (var i = 0; i < exports.length; i++) {
                    var name = exports[i].name;
                    if (name.indexOf("bar") !== -1 || name.indexOf("CodeCheck") !== -1) {
                        console.log("[!] FOUND CANDIDATE: " + name);
                        Interceptor.attach(exports[i].address, {
                            onLeave: function(retval) {
                                console.log("[+] FORCING RETURN TRUE");
                                retval.replace(1);
                            }
                        });
                    }
                }
            }
        }
    }, 1000);

    console.log("[+] === ALL HOOKS ACTIVE - ENTER TEXT AND PRESS VERIFY ===");
});
