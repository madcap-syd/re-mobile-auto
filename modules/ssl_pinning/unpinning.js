/**
 * Universal Android SSL Pinning Bypass
 * Part of the re-mobile-auto framework
 * Hooks: Java TrustManager, OkHttp CertificatePinner, and Conscrypt
 */

console.log("[*] Loading SSL Pinning Bypass Script...");

// 1. Bypass Java's TrustManager (Standard HTTPS)
try {
    var TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    var SSLContext = Java.use('javax.net.ssl.SSLContext');

    var TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');
    TrustManagerImpl.checkTrustedRecursive.implementation = function() {
        console.log("[+] Bypassed TrustManagerImpl.checkTrustedRecursive");
        return [];
    };

    var X509TrustManager = Java.registerClass({
        name: 'com.remobileauto.CustomTrustManager',
        implements: [TrustManager],
        methods: {
            checkClientTrusted: function(chain, authType) {},
            checkServerTrusted: function(chain, authType) {},
            getAcceptedIssuers: function() { return []; }
        }
    });

    var TrustManagers = [X509TrustManager.$new()];
    var SSLContext_init = SSLContext.init.overload(
        '[Ljavax.net.ssl.KeyManager;', '[Ljavax.net.ssl.TrustManager;', 'java.security.SecureRandom'
    );
    SSLContext_init.implementation = function(keyManager, trustManager, secureRandom) {
        console.log("[+] Bypassed SSLContext.init (Injected Custom TrustManager)");
        SSLContext_init.call(this, keyManager, TrustManagers, secureRandom);
    };
} catch (err) {
    console.log("[-] Java TrustManager bypass failed: " + err);
}

// 2. Bypass OkHttp 3.x CertificatePinner
try {
    var CertificatePinner = Java.use('okhttp3.CertificatePinner');
    CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function(hostname, pinnedCertificates) {
        console.log("[+] Bypassed OkHttp CertificatePinner.check for: " + hostname);
        return; // Do nothing, bypass the check
    };
    CertificatePinner.check.overload('java.lang.String', 'okhttp3.CertificatePinner$Chain').implementation = function(hostname, chain) {
        console.log("[+] Bypassed OkHttp CertificatePinner.check (Chain) for: " + hostname);
        return;
    };
} catch (err) {
    console.log("[-] OkHttp bypass failed (maybe not using OkHttp): " + err);
}

// 3. Bypass Conscrypt / Platform default
try {
    var Platform = Java.use('com.android.org.conscrypt.Platform');
    Platform.checkServerTrusted.implementation = function() {
        console.log("[+] Bypassed Conscrypt Platform.checkServerTrusted");
    };
} catch (err) {
    console.log("[-] Conscrypt bypass failed: " + err);
}

console.log("[✅] SSL Pinning Bypass Script Loaded Successfully!");
