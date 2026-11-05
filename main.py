#!/usr/bin/env python3
import argparse, json, shutil, zipfile
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

install(show_locals=True)
console = Console()

def analyze_apk(apk_path: Path, output_dir: Path):
    if not apk_path.exists():
        console.print(f"[red][ERROR][/red] File not found: {apk_path}")
        return False

    target_name = apk_path.stem
    target_report_dir = output_dir / target_name
    target_report_dir.mkdir(parents=True, exist_ok=True)

    console.print(Panel(f"Starting analysis of: [bold cyan]{apk_path.name}[/bold cyan]", title="re-mobile-auto"))

    shutil.copy(apk_path, target_report_dir / apk_path.name)
    
    try:
        with zipfile.ZipFile(apk_path, 'r') as zip_ref:
            zip_ref.extractall(target_report_dir / "unpacked")
        console.print("[green][+][/green] APK structure unpacked.")
    except zipfile.BadZipFile:
        console.print("[red][ERROR][/red] Invalid APK.")
        return False

    unpacked_dir = target_report_dir / "unpacked"
    intel = {
        "target_name": target_name,
        "dex_files": [str(p.relative_to(unpacked_dir)) for p in unpacked_dir.rglob("*.dex")],
        "native_libs": [str(p.relative_to(unpacked_dir)) for p in unpacked_dir.rglob("*.so")],
    }

    try:
        from core.unpacker import APKUnpacker
        unpacker = APKUnpacker()
        
        apktool_out = unpacker.decode_with_apktool(apk_path, target_report_dir)
        if apktool_out:
            intel["manifest_info"] = unpacker.extract_manifest_info(apktool_out)
            
        jadx_out = unpacker.decompile_with_jadx(apk_path, target_report_dir)
        if jadx_out:
            intel["jadx_output"] = str(jadx_out.relative_to(target_report_dir))
            
            # --- ЗАПУСК JAVA INTEL (Статический анализ) ---
            console.print("[*] Running static analysis (Java Intel)...")
            from core.java_intel import scan_directory_for_secrets
            secrets = scan_directory_for_secrets(jadx_out)
            if secrets:
                intel["static_analysis_findings"] = secrets
                console.print("[yellow][!][/yellow] Interesting patterns found! Check the JSON report.")
            else:
                console.print("[dim][*][/dim] No obvious secrets found in Java code.")
                
    except Exception as e:
        console.print(f"[red][ERROR][/red] Advanced unpacking failed: {e}")

    report_file = target_report_dir / "initial_intel.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(intel, f, indent=4)
    
    console.print(f"[green][+][/green] Intelligence saved to: [bold]{report_file}[/bold]")
    console.print("\n[bold]--- Initial Intel Summary ---[/bold]")
    if "manifest_info" in intel:
        console.print(f"[cyan]Package:[/cyan] {intel['manifest_info']['package_name']}")
        console.print(f"[cyan]Exported Activities:[/cyan] {intel['manifest_info']['exported_activities_count']}")
    console.print(f"[cyan]DEX files:[/cyan] {len(intel['dex_files'])}")
    console.print(f"[cyan]Native libs (.so):[/cyan] {len(intel['native_libs'])}")
    if "static_analysis_findings" in intel:
        console.print(f"[yellow]Secrets/Patterns found:[/yellow] {len(intel['static_analysis_findings'])} categories")
        


    # 7. Анализ нативных библиотек (Native Bridge)
    intel["native_libs_analysis"] = [] # Инициализируем пустым
    try:
        from core.native_bridge import analyze_native_libs
        native_findings = analyze_native_libs(unpacked_dir, target_report_dir)
        if native_findings:
            intel["native_libs_analysis"] = native_findings
            console.print(f"[green][+][/green] Ghidra findings added to intel.")
    except Exception as e:
        console.print(f"[red][ERROR][/red] Native bridge failed: {e}")
    except Exception as e:
        console.print(f"[red][ERROR][/red] Native bridge failed: {e}")


    # 8. Генерация Native Frida скрипта на основе Ghidra
    try:
        from core.native_frida_gen import generate_native_frida
        # Передаем словарь intel напрямую, чтобы избежать проблем с чтением файла
        generate_native_frida(target_report_dir, intel)
    except Exception as e:
        console.print(f"[red][ERROR][/red] Native Frida generation failed: {e}")

    # 6. Генерация Frida скрипта на основе находок
    try:
        from core.frida_gen import generate_frida_script
        generate_frida_script(target_report_dir)
    except Exception as e:
        console.print(f"[red][ERROR][/red] Frida generation failed: {e}")

        # Генерация HTML отчета и SSL bypass
    try:
        from core.report_generator import generate_html_report
        from core.ssl_bypass_gen import generate_ssl_bypass
        report_file_html = generate_html_report(intel, target_report_dir)
        console.print(f"[green][+][/green] HTML report saved to: {report_file_html}")
        ssl_file = generate_ssl_bypass(target_report_dir)
        console.print(f"[green][+][/green] SSL bypass script saved to: {ssl_file}")
    except Exception as e:
        console.print(f"[red][ERROR][/red] Report generation failed: {e}")

    return True

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description="re-mobile-auto")
    parser.add_argument("target", type=str, help="Path to APK")
    parser.add_argument("-o", "--output", type=str, default="reports")
    args = parser.parse_args()
    
    if analyze_apk(Path(args.target).resolve(), Path(args.output).resolve()):
        console.print("\n[bold green]✅ Phase 1 & 2 Complete.[/bold green]")
    else:
        console.print("\n[bold red]❌ Phase Failed.[/bold red]")
