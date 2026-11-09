Java.perform(function() {
    console.log("[*] Level 3 Ultimate Anti-Frida Bypass Active");

    // 1. Обманываем поиск строк "frida", "gum", "xposed" в памяти
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
                                    this.needle.indexOf("xposed") !== -1 ||
                                    this.needle.indexOf("linjector") !== -1)) {
                    // Возвращаем 0 (NULL), как будто строка не найдена
                    retval.replace(ptr(0));
                }
            }
        });
        console.log("[+] Hooked strstr to hide Frida artifacts");
    }

    // 2. Обманываем проверку свойства ro.debuggable (возвращаем "0" вместо "1")
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
                    console.log("[+] Spoofed ro.debuggable to 0");
                }
            }
        });
        console.log("[+] Hooked __system_property_get to hide debug mode");
    }

    // 3. Нейтрализуем саму функцию goodbye() по смещению из бэктрейса!
    // Из твоего лога: #03 pc 00003021 ... (goodbye()+33)
    // Значит, начало функции goodbye: 0x3021 - 33 (0x21) = 0x3000
    setTimeout(function() {
        var libfoo = Module.findBaseAddress("libfoo.so");
        if (libfoo) {
            var goodbyeAddr = libfoo.add(0x3000);
            console.log("[*] Neutralizing 'goodbye' at offset: " + goodbyeAddr);
            Interceptor.replace(goodbyeAddr, new NativeCallback(function() {
                console.log("[!] 'goodbye()' was called, but we neutralized it!");
                // Просто возвращаем управление, не вызывая краш
            }, 'void', []));
        }
    }, 500);

    console.log("[+] All stealth hooks active! App should stay alive.");
});
