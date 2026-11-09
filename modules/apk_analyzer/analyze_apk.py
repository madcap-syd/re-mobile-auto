#!/usr/bin/env python3
"""
Advanced APK Analyzer Module for re-mobile-auto framework
Automatically discovers hidden fragments, native bridges, navigation graphs, and potential flags.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class APKAnalyzer:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.src_dir = apk_path.replace('.apk', '_analyzed')
        self.findings = {
            'hidden_fragments': [],
            'native_bridges': [],
            'navigation_graphs': [],
            'suspicious_strings': [],
            'assets': []
        }
    
    def run_cmd(self, cmd, shell=True):
        """Выполняет команду и возвращает вывод"""
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    
    def decompile(self):
        """Декомпилирует APK через JADX"""
        print(f"[*] Декомпиляция {self.apk_path}...")
        os.makedirs(self.src_dir, exist_ok=True)
        code, out, err = self.run_cmd(f"jadx -d '{self.src_dir}' '{self.apk_path}' 2>/dev/null")
        if code == 0 or os.path.exists(self.src_dir):
            print("    ✅ Декомпиляция завершена")
            return True
        print("    ❌ Ошибка декомпиляции")
        return False
    
    def find_hidden_components(self):
        """Ищет скрытые фрагменты и классы"""
        print("\n[*] Поиск скрытых компонентов...")
        src_path = Path(self.src_dir) / 'sources'
        
        # Ищем все Java файлы в пакете приложения
        java_files = list(src_path.rglob('*.java'))
        
        suspicious_patterns = ['Fragment', 'Bridge', 'Console', 'Diagnostic', 'Stage', 'Admin', 'Secret', 'Hidden']
        
        for file in java_files:
            content = file.read_text(errors='ignore')
            for pattern in suspicious_patterns:
                if pattern in file.name and 'noob/ymuu/detour' in str(file):  # Фильтр по пакету
                    self.findings['hidden_fragments'].append({
                        'file': str(file),
                        'name': file.stem,
                        'content': content[:2000]  # Первые 2000 символов
                    })
                    print(f"    🎯 Найден: {file.name}")
    
    def analyze_native_bridge(self):
        """Анализирует NativeBridge и нативные методы"""
        print("\n[*] Анализ NativeBridge и JNI...")
        src_path = Path(self.src_dir) / 'sources'
        
        for file in src_path.rglob('*NativeBridge*.java'):
            content = file.read_text(errors='ignore')
            native_methods = []
            
            # Ищем native методы
            for line in content.split('\n'):
                if 'native' in line and ('public' in line or 'private' in line):
                    native_methods.append(line.strip())
            
            # Ищем константы
            consts = []
            for line in content.split('\n'):
                if 'CONST' in line or 'M1_' in line:
                    consts.append(line.strip())
            
            self.findings['native_bridges'].append({
                'file': str(file),
                'native_methods': native_methods,
                'constants': consts,
                'full_content': content
            })
            print(f"    ✅ Проанализирован: {file.name}")
            print(f"       Нативные методы: {len(native_methods)}")
    
    def find_navigation_graphs(self):
        """Ищет графы навигации"""
        print("\n[*] Поиск графов навигации...")
        res_path = Path(self.src_dir) / 'resources' / 'res' / 'navigation'
        
        if res_path.exists():
            for xml_file in res_path.rglob('*.xml'):
                content = xml_file.read_text(errors='ignore')
                destinations = []
                
                # Ищем destination в XML
                for line in content.split('\n'):
                    if 'android:name' in line or 'app:destination' in line:
                        destinations.append(line.strip())
                
                self.findings['navigation_graphs'].append({
                    'file': str(xml_file),
                    'destinations': destinations
                })
                print(f"    🗺️  Найден граф: {xml_file.name}")
                print(f"       Маршрутов: {len(destinations)}")
    
    def extract_suspicious_strings(self):
        """Ищет подозрительные строки (flag, htb, key, secret)"""
        print("\n[*] Поиск подозрительных строк...")
        keywords = ['flag', 'htb{', 'secret', 'key', 'password', 'token', 'route', 'hidden']
        src_path = Path(self.src_dir) / 'sources'
        
        for keyword in keywords:
            code, out, err = self.run_cmd(f"grep -ri '{keyword}' '{src_path}' 2>/dev/null | head -20")
            if out.strip():
                self.findings['suspicious_strings'].append({
                    'keyword': keyword,
                    'matches': out.strip()[:1000]
                })
                print(f"    🔍 '{keyword}': найдено совпадений")
    
    def list_assets(self):
        """Список ассетов приложения"""
        print("\n[*] Поиск ассетов (assets)...")
        assets_path = Path(self.src_dir) / 'resources' / 'assets'
        
        if assets_path.exists():
            for asset in assets_path.rglob('*'):
                if asset.is_file():
                    self.findings['assets'].append(str(asset.relative_to(assets_path)))
                    print(f"    📦 Asset: {asset.name}")
    
    def generate_report(self):
        """Генерирует отчет"""
        print("\n" + "="*80)
        print("📊 ОТЧЕТ АНАЛИЗА APK")
        print("="*80)
        
        print(f"\n Скрытые компоненты ({len(self.findings['hidden_fragments'])}):")
        for frag in self.findings['hidden_fragments']:
            print(f"   • {frag['name']}")
        
        print(f"\n🔌 Native Bridge ({len(self.findings['native_bridges'])}):")
        for bridge in self.findings['native_bridges']:
            print(f"   • {os.path.basename(bridge['file'])}")
            for method in bridge['native_methods']:
                print(f"     - {method}")
        
        print(f"\n🗺️  Графы навигации ({len(self.findings['navigation_graphs'])}):")
        for graph in self.findings['navigation_graphs']:
            print(f"   • {os.path.basename(graph['file'])}")
            for dest in graph['destinations'][:5]:  # Первые 5
                print(f"     → {dest}")
        
        print(f"\n🔑 Подозрительные строки:")
        for item in self.findings['suspicious_strings']:
            if item['matches']:
                print(f"   • '{item['keyword']}':")
                for line in item['matches'].split('\n')[:3]:
                    print(f"     {line[:100]}")
        
        print("\n" + "="*80)
        print("💡 РЕКОМЕНДАЦИИ:")
        print("="*80)
        
        if self.findings['hidden_fragments']:
            print("1. Изучи скрытые фрагменты - они могут содержать флаг!")
        if self.findings['native_bridges']:
            print("2. Проанализируй нативные методы - флаг может быть в .so библиотеке")
        if self.findings['assets']:
            print("3. Проверь ассеты (особенно config.dat, data.bin и т.д.)")
        
        print("="*80)

def main():
    if len(sys.argv) < 2:
        print("Использование: python3 modules/apk_analyzer/analyze_apk.py <path_to_apk>")
        sys.exit(1)
    
    apk_path = sys.argv[1]
    analyzer = APKAnalyzer(apk_path)
    
    if analyzer.decompile():
        analyzer.find_hidden_components()
        analyzer.analyze_native_bridge()
        analyzer.find_navigation_graphs()
        analyzer.extract_suspicious_strings()
        analyzer.list_assets()
        analyzer.generate_report()
    else:
        print("❌ Не удалось декомпилировать APK")
        sys.exit(1)

if __name__ == "__main__":
    main()
