from pathlib import Path

def generate_ssl_bypass(report_dir: Path):
    """Генерирует универсальный SSL Pinning bypass скрипт"""
    script = """// Auto-generated SSL Pinning Bypass by re-mobile-auto
// Supports: OkHttp3, HttpsURLConnection, TrustManager, CertificatePinner

Java.perform(function() {
    console.log("[*] Starting SSL Pinning Bypass...");
    
    // 1. Bypass OkHttp3 CertificatePinner
    try {
        var CertificatePinner = Java.use("okhttp3.CertificatePinner");
        CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function() {
            console.log("[+] Bypassed OkHttp3 CertificatePinner.check(String, List)");
        };
        CertificatePinner.check.overload('java.lang.String', 'java.security.cert.Certificate').implementation = function() {
            console.log("[+] Bypassed OkHttp3 CertificatePinner.check(String, Certificate)");
        };
        console.log("[+] OkHttp3 CertificatePinner hooked");
    } catch(e) {
        console.log("[-] OkHttp3 not found: " + e);
    }
    
    // 2. Bypass TrustManager (accept all certificates)
    try {
        var TrustManagerImpl = Java.use("com.android.org.conscrypt.TrustManagerImpl");
        TrustManagerImpl.checkTrustedRecursive.implementation = function() {
            console.log("[+] Bypassed TrustManagerImpl.checkTrustedRecursive");
            return [];
        };
        console.log("[+] TrustManagerImpl hooked");
    } catch(e) {
        console.log("[-] TrustManagerImpl not found: " + e);
    }
    
    // 3. Bypass HttpsURLConnection
    try {
        var HttpsURLConnection = Java.use("javax.net.ssl.HttpsURLConnection");
        HttpsURLConnection.setDefaultHostnameVerifier.implementation = function() {
            console.log("[+] Bypassed HttpsURLConnection.setDefaultHostnameVerifier");
        };
        console.log("[+] HttpsURLConnection hooked");
    } catch(e) {
        console.log("[-] HttpsURLConnection not found: " + e);
    }
    
    console.log("[+] SSL Pinning Bypass complete!");
});
"""
    
    script_file = report_dir / "frida_ssl_bypass.js"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script)
    
    return script_file
