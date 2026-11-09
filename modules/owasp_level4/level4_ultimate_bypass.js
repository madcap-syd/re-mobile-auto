Java.perform(function() {
    console.log("[*] === LEVEL 4 ULTIMATE BYPASS ACTIVE ===");

    // 1. НЕЙТРАЛИЗАЦИЯ DIVIDE BY ZERO В OnCreate
    try {
        var MainActivity = Java.use("re.pwnme.MainActivity");
        var originalOnCreate = MainActivity.onCreate;
        
        MainActivity.onCreate.implementation = function(bundle) {
            console.log("[*] Intercepted MainActivity.onCreate");
            try {
                // Пытаемся выполнить оригинальный код
                originalOnCreate.call(this, bundle);
            } catch (e) {
                // Если произошло деление на ноль или другая ошибка - просто ловим и игнорируем!
                console.log("[+] Caught and neutralized crash in onCreate: " + e);
            }
        };
        console.log("[+] MainActivity.onCreate hooked to swallow crashes");
    } catch (e) {
        console.log("[-] Could not hook MainActivity: " + e);
    }

    // 2. БЛОКИРОВКА ГЛОБАЛЬНОГО ОБРАБОТЧИКА ИСКЛЮЧЕНИЙ (на всякий случай)
    try {
        var Thread = Java.use("java.lang.Thread");
        Thread.setDefaultUncaughtExceptionHandler.implementation = function(handler) {
            console.log("[+] Blocked setDefaultUncaughtExceptionHandler");
            // Ничего не делаем, чтобы приложение не могло установить свой обработчик крашей
        };
    } catch (e) {}

    // 3. ПЕРЕХВАТ ЗАГРУЗКИ НАТИВНЫХ БИБЛИОТЕК (dlopen)
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

    function hookNativeLib(libName) {
        console.log("[*] Enumerating exports in " + libName);
        var exports = Module.enumerateExports(libName);
        var hookedCount = 0;
        
        for (var i = 0; i < exports.length; i++) {
            var name = exports[i].name;
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
                } catch(e) {}
            }
        }
        console.log("[+] Hooked " + hookedCount + " functions in " + libName);
    }

    console.log("[+] === ALL DEFENSES ACTIVE. APP SHOULD SURVIVE! ===");
});
