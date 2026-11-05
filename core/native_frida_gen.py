import json
import re
from pathlib import Path
from rich.console import Console

console = Console()

def generate_native_frida(report_dir: Path, intel_dict: dict):
    # Берем данные напрямую из переданного словаря
    native_libs = intel_dict.get("native_libs_analysis", [])
    
    if not native_libs:
        console.print("[yellow][*] No native libs analysis found in intel dict. Skipping.[/yellow]")
        return
        
    console.print("[*] Generating Native Frida bypass script from Ghidra findings...")
    
    js_lines = []
    js_lines.append("/* Auto-generated Native Frida Script by re-mobile-auto */")
    js_lines.append("Java.perform(function() {")
    
    hooks_generated = 0
    for lib in native_libs:
        lib_name = Path(lib["file"]).name
        findings = lib.get("ghidra_findings", [])
        
        if not findings:
            continue
            
        js_lines.append(f'    console.log("[*] Preparing hooks for {lib_name}...");')
        
        for finding in findings:
            match = re.search(r'->\s+(\S+)\s+@\s+([0-9a-fA-F]+)', finding)
            if match:
                func_name = match.group(1)
                address = match.group(2)
                hooks_generated += 1
                
                js_lines.append(f"    // Hooking: {func_name}")
                js_lines.append("    try {")
                js_lines.append(f'        var exportAddr = Module.findExportByName("{lib_name}", "{func_name}");')
                js_lines.append("        if (exportAddr) {")
                js_lines.append(f'            console.log("[+] Found export {func_name} at " + exportAddr);')
                js_lines.append("            Interceptor.attach(exportAddr, {{")
                js_lines.append("                onEnter: function(args) {{")
                js_lines.append(f'                    console.log("[*] Entered {func_name}");')
                js_lines.append("                }},")
                js_lines.append("                onLeave: function(retval) {{")
                js_lines.append('                    console.log("[+] Bypassing! Forcing return value to 1 (true).");')
                js_lines.append("                    retval.replace(ptr(1));")
                js_lines.append("                }}")
                js_lines.append("            }});")
                js_lines.append("        } else {")
                js_lines.append(f'            console.log("[-] Export {func_name} not found. Falling back to offset {address}");')
                js_lines.append('            var baseAddr = Module.findBaseAddress("' + lib_name + '");')
                js_lines.append("            if (baseAddr) {")
                js_lines.append('                var targetAddr = baseAddr.add(ptr("' + address + '"));')
                js_lines.append("                Interceptor.attach(targetAddr, {{")
                js_lines.append("                    onLeave: function(retval) {{ retval.replace(ptr(1)); }}")
                js_lines.append("                }});")
                js_lines.append("            }")
                js_lines.append("        }")
                js_lines.append("    } catch(e) {{")
                js_lines.append(f'        console.log("[-] Hook failed for {func_name}: " + e);')
                js_lines.append("    }}")
                js_lines.append("")

    js_lines.append("});")
    
    if hooks_generated > 0:
        output_file = report_dir / "frida_native_bypass.js"
        with open(output_file, "w", encoding="utf-8") as f_out:
            f_out.write("\n".join(js_lines))
        console.print(f"[green][+][/green] Native Frida script saved to: [bold]{output_file}[/bold]")
        console.print(f"[cyan][i][/cyan] Generated {hooks_generated} native hooks!")
    else:
        console.print("[yellow][*] No hookable native functions found in Ghidra output.[/yellow]")
