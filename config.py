"""
Файл конфигурации для Discord бота
"""
import os
from dotenv import load_dotenv

# Загрузка из .env файла
load_dotenv()

# Токен Discord из .env
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', '')

# Префикс команд
PREFIKS_KOMAND = '/'

# Цвета для встраиваемых сообщений
CVETA = {
    'osnovnoy': 0x5865F2,      # Discord синий
    'uspeh': 0x57F287,         # Зелёный
    'preduprezhdenie': 0xFEE75C,  # Жёлтый
    'oshibka': 0xED4245,       # Красный
    'info': 0x00AFF4           # Голубой
}

# Настройки для графиков
NASTROJKI_GRAFIKOV = {
    'dpi': 100,
    'razmer': (10, 6),
    'stil': 'seaborn-v0_8-darkgrid'
}
