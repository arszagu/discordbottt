"""
Тестовый скрипт для проверки конфигурации бота
Запусти этот файл перед первым запуском основного бота
"""

import sys
import os

def check_python_version():
    """Проверка версии Python"""
    print("🐍 Проверка версии Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} - ОШИБКА (требуется 3.8+)")
        return False


def check_venv():
    """Проверка виртуального окружения"""
    print("\n🌍 Проверка виртуального окружения...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("   ✅ Виртуальное окружение активировано")
        return True
    else:
        print("   ⚠️  Виртуальное окружение НЕ активировано")
        print("   Активируй его командой: venv\\Scripts\\activate")
        return False


def check_dependencies():
    """Проверка установленных зависимостей"""
    print("\n📦 Проверка зависимостей...")
    
    required_packages = {
        'discord': 'discord.py',
        'dotenv': 'python-dotenv',
        'matplotlib': 'matplotlib',
        'PIL': 'pillow',
        'numpy': 'numpy'
    }
    
    missing_packages = []
    
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"   ✅ {package_name} установлен")
        except ImportError:
            print(f"   ❌ {package_name} НЕ установлен")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n   Установи недостающие пакеты командой:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True


def check_env_file():
    """Проверка файла .env"""
    print("\n⚙️  Проверка файла .env...")
    
    if not os.path.exists('.env'):
        print("   ❌ Файл .env не найден!")
        return False
    
    print("   ✅ Файл .env найден")
    
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'DISCORD_TOKEN' not in content:
            print("   ❌ Переменная DISCORD_TOKEN не найдена в .env")
            return False
        
        if 'YOUR_TOKEN_HERE' in content:
            print("   ⚠️  DISCORD_TOKEN ещё не установлен!")
            print("   Добавь свой токен в файл .env")
            print("   DISCORD_TOKEN=your_token_here")
            return False
        
        print("   ✅ DISCORD_TOKEN установлен")
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка при чтении .env: {e}")
        return False


def check_config():
    """Проверка файла config.py"""
    print("\n📄 Проверка файла config.py...")
    
    if not os.path.exists('config.py'):
        print("   ❌ Файл config.py не найден!")
        return False
    
    print("   ✅ Файл config.py найден")
    
    try:
        import config
        print("   ✅ config.py успешно импортирован")
        
        required_attrs = ['DISCORD_TOKEN', 'PREFIKS_KOMAND', 'CVETA', 'NASTROJKI_GRAFIKOV']
        for attr in required_attrs:
            if hasattr(config, attr):
                print(f"   ✅ Атрибут '{attr}' найден")
            else:
                print(f"   ❌ Атрибут '{attr}' не найден")
                return False
        
        return True
    except Exception as e:
        print(f"   ❌ Ошибка при импорте config.py: {e}")
        return False


def check_cogs():
    """Проверка папки cogs"""
    print("\n📦 Проверка папки cogs...")
    
    if not os.path.exists('cogs'):
        print("   ❌ Папка cogs не найдена!")
        return False
    
    print("   ✅ Папка cogs найдена")
    
    required_files = ['__init__.py', 'stats.py']
    missing_files = []
    
    for file in required_files:
        filepath = os.path.join('cogs', file)
        if os.path.exists(filepath):
            print(f"   ✅ Файл cogs/{file} найден")
        else:
            print(f"   ❌ Файл cogs/{file} не найден")
            missing_files.append(file)
    
    return len(missing_files) == 0


def main():
    """Главная функция"""
    print("=" * 50)
    print("   Discord Bot - Проверка конфигурации")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_venv(),
        check_dependencies(),
        check_env_file(),
        check_config(),
        check_cogs()
    ]
    
    print("\n" + "=" * 50)
    
    if all(checks):
        print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("Бот готов к запуску:")
        print("  python main.py")
        print("=" * 50)
        return 0
    else:
        print("❌ ОБНАРУЖЕНЫ ПРОБЛЕМЫ")
        print("Исправь ошибки выше и повтори проверку")
        print("=" * 50)
        return 1


if __name__ == "__main__":
    exit_code = main()
    input("\nНажми Enter для выхода...")
    sys.exit(exit_code)
