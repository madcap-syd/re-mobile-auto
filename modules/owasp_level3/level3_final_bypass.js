Java.perform(function() {
    console.log("[*] === LEVEL 3 FINAL COMBINED BYPASS ===");

    // === ЧАСТЬ 1: JAVA LAYER (Root Detection Bypass) ===
    console.log("[*] Hooking Java Root Detection...");
    
    try {
        var RootDetection = Java.use("sg.vantagepoint.util.RootDetection");
        RootDetection.checkRoot1.implementation = function() {
            console.log("[+] Bypassed checkRoot1 - returning false");
            return false;
        };
        RootDetection.checkRoot2.implementation = function() {
            console.log("[+] Bypassed checkRoot2 - returning false");
            return false;
        };
        RootDetection.checkRoot3.implementation = function() {
            console.log("[+] Bypassed checkRoot3 - returning false");
            return false;
        };
        console.log("[+] Java Root Detection bypassed!");
    } catch(e) {
        console.log("[-] RootDetection hook failed: " + e);
    }

    // === ЧАСТЬ 2: NATIVE LAYER (Anti-Frida Bypass) ===
    console.log("[*] Hooking Native Anti-Frida checks...");

    // 1. strstr hook
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
                    retval.replace(ptr(0));
                }
            }
        });
        console.log("[+] Hooked strstr to hide Frida");
    }

    // 2. __system_property_get hook
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
        console.log("[+] Hooked __system_property_get");
    }

    // 3. goodbye() neutralization
    setTimeout(function() {
        var libfoo = Module.findBaseAddress("libfoo.so");
        if (libfoo) {
            var goodbyeAddr = libfoo.add(0x3000);
            Interceptor.replace(goodbyeAddr, new NativeCallback(function() {
                console.log("[!] Neutralized goodbye() crash");
            }, 'void', []));
        }
    }, 500);

    console.log("[+] === ALL HOOKS ACTIVE ===");
    console.log("[*] Click OK on dialog, then enter ANY text and press Verify!");
});
