# 📱 re-mobile-auto

**Автоматизированный фреймворк для реверс-инжиниринга Android APK**

## 🚀 Возможности

- 📦 **Умная распаковка**: apktool + jadx
- 🔍 **Статический анализ**: Поиск crypto, root detection, secrets
- 🧠 **Ghidra Headless**: Авто-анализ нативных .so библиотек  
- 🕷 **Frida генерация**: Авто-создание frida_bypass.js и frida_native_bypass.js
- 🐳 **Docker**: 100% воспроизводимость окружения

## 🛠 Быстрый старт

### Docker (рекомендуется)
\`\`\`bash
docker build -t re-mobile-auto:latest .
docker run --rm -v $(pwd)/reports:/app/reports re-mobile-auto:latest target.apk
\`\`\`

### Локально
\`\`\`bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 main.py target.apk
\`\`\`

## 📂 Результаты

После анализа в `reports/<target>/`:
- `initial_intel.json` - полный JSON с уязвимостями
- `frida_bypass.js` - хуки для Java
- `frida_native_bypass.js` - хуки для Native
- `jadx_sources/` - декомпилированный Java код

## 🏢 Применение

    * Аудит безопасности Android приложений
    * Анализ вредоносного ПО  
    ️* Валидация RASP-защит
    * Обход SSL Pinning
