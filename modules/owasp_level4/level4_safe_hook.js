Java.perform(function() {
    console.log("[*] === LEVEL 4 SAFE HOOK ACTIVE ===");

    // 1. JAVA BYPASS (на всякий случай)
    try {
        // Пытаемся найти классы проверки, если они есть
        var RootCheck = Java.use("b.a.a.b"); // Из нашего JSON отчета
        if (RootCheck) {
            RootCheck.a.implementation = function() { return false; };
            RootCheck.b.implementation = function() { return false; };
            console.log("[+] Java root checks bypassed");
        }
    } catch(e) {}

    // 2. ПЕРЕХВАТ ЗАГРУЗКИ БИБЛИОТЕК (dlopen)
    var dlopen = Module.findExportByName(null, "android_dlopen_ext") || Module.findExportByName(null, "dlopen");
    if (dlopen) {
        Interceptor.attach(dlopen, {
            onEnter: function(args) {
                this.path = args[0].readCString();
            },
            onLeave: function(retval) {
                if (this.path && (this.path.indexOf("libtool-checker.so") !== -1 || this.path.indexOf("libnative-lib.so") !== -1)) {
                    console.log("[+] Library loaded: " + this.path);
                    var libName = this.path.split('/').pop();
                    hookNativeLib(libName);
                }
            }
        });
        console.log("[+] Hooked dlopen to wait for native libs");
    }

    // Функция для хука экспортов после загрузки
    function hookNativeLib(libName) {
        console.log("[*] Enumerating exports in " + libName);
        var exports = Module.enumerateExports(libName);
        var hookedCount = 0;
        
        for (var i = 0; i < exports.length; i++) {
            var name = exports[i].name;
            // Ищем функции проверки, инициализации или JNI
            if (name.indexOf("check") !== -1 || name.indexOf("init") !== -1 || 
                name.indexOf("Java_") !== -1 || name.indexOf("validate") !== -1) {
                
                console.log("[!] Hooking: " + name + " @ " + exports[i].address);
                try {
                    Interceptor.attach(exports[i].address, {
                        onEnter: function(args) {
                            console.log("[*] Entered: " + name);
                        },
                        onLeave: function(retval) {
                            console.log("[+] Forcing TRUE for: " + name);
                            retval.replace(1);
                        }
                    });
                    hookedCount++;
                } catch(e) {
                    console.log("[-] Failed to hook " + name + ": " + e);
                }
            }
        }
        console.log("[+] Hooked " + hookedCount + " functions in " + libName);
    }

    console.log("[+] === WAITING FOR LIBRARY LOAD ===");
});
