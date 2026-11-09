Java.perform(function() {
    console.log("[*] === NATIVE BYPASS SCRIPT ACTIVE ===");
    var targetLibs = ["libdetour.so", "libfoo.so", "libnative-lib.so", "libtool-checker.so"];
    
    for (var i = 0; i < targetLibs.length; i++) {
        var libName = targetLibs[i];
        var libBase = Module.findBaseAddress(libName);
        if (libBase) {
            console.log("[+] Found " + libName + " at " + libBase);
            var exports = Module.enumerateExports(libName);
            for (var j = 0; j < exports.length; j++) {
                var name = exports[j].name;
                if (name.indexOf("check") !== -1 || name.indexOf("verify") !== -1 || 
                    name.indexOf("init") !== -1 || name.indexOf("Java_") !== -1 ||
                    name.indexOf("validate") !== -1) {
                    console.log("[!] FOUND CANDIDATE: " + name + " @ " + exports[j].address);
                    Interceptor.attach(exports[j].address, {
                        onEnter: function(args) {
                            console.log("[*] Entered: " + name);
                        },
                        onLeave: function(retval) {
                            console.log("[+] FORCING RETURN TO TRUE (1) for: " + name);
                            retval.replace(1);
                        }
                    });
                }
            }
        }
    }
    console.log("[+] === ALL NATIVE HOOKS ACTIVE ===");
});