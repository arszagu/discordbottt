"""
Главный файл Discord бота для визуализации статистики сервера
"""
import sys
import io

# Установка UTF-8 кодировки для консоли Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import discord
from discord.ext import commands
import config
import os
from pathlib import Path

# Создание бота с намерениями
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix=config.PREFIKS_KOMAND,
    intents=intents,
    help_command=None
)


@bot.event
async def on_ready():
    """Событие, срабатывающее при подключении бота"""
    print(f"[OK] Бот {bot.user} успешно подключился!")
    print(f"[INFO] Бот зарегистрирован на {len(bot.guilds)} серверах")
    
    # Установка статуса
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"статистику | {config.PREFIKS_KOMAND}help"
        ),
        status=discord.Status.online
    )


@bot.command(name='help')
async def help_command(ctx):
    """Команда справки"""
    embed = discord.Embed(
        title="Справка - Доступные команды",
        description="Список всех доступных команд бота",
        color=config.CVETA['osnovnoy']
    )
    
    embed.add_field(
        name="Основные команды",
        value=f"""
`{config.PREFIKS_KOMAND}server_stats` - Основная статистика сервера
`{config.PREFIKS_KOMAND}member_graph` - График распределения участников
`{config.PREFIKS_KOMAND}channel_stats` - Статистика каналов
`{config.PREFIKS_KOMAND}role_list` - Список всех ролей сервера
`{config.PREFIKS_KOMAND}help` - Показать это сообщение
        """,
        inline=False
    )
    
    embed.add_field(
        name="Примеры использования",
        value=f"""
`{config.PREFIKS_KOMAND}stats` - Показать основную информацию
`{config.PREFIKS_KOMAND}member_graph` - Увидеть соотношение пользователей/ботов
`{config.PREFIKS_KOMAND}channel_stats` - Увидеть распределение каналов
        """,
        inline=False
    )
    
    embed.set_footer(text="Используйте команды в любом канале!")
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
    
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    """Обработчик ошибок команд"""
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Ошибка",
            description=f"Команда не найдена. Используйте `{config.PREFIKS_KOMAND}help` для справки",
            color=config.CVETA['oshibka']
        )
        await ctx.send(embed=embed, delete_after=5)
    
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Ошибка",
            description="У вас нет прав для использования этой команды",
            color=config.CVETA['oshibka']
        )
        await ctx.send(embed=embed, delete_after=5)
    
    else:
        embed = discord.Embed(
            title="Ошибка при выполнении команды",
            description=f"```{str(error)}```",
            color=config.CVETA['oshibka']
        )
        await ctx.send(embed=embed, delete_after=10)


async def load_cogs():
    """Загрузка всех расширений"""
    cogs_dir = Path("cogs")
    
    if not cogs_dir.exists():
        print("[ВНИМАНИЕ] Папка с расширениями не найдена!")
        return
    
    for cog_file in cogs_dir.glob("*.py"):
        if cog_file.name.startswith("_"):
            continue
        
        cog_name = cog_file.stem
        try:
            await bot.load_extension(f"cogs.{cog_name}")
            print(f"[OK] Расширение '{cog_name}' успешно загружено")
        except Exception as e:
            print(f"[ОШИБКА] Ошибка загрузки расширения '{cog_name}': {e}")


async def main():
    """Основная асинхронная функция"""
    
    # Проверка токена
    token = config.DISCORD_TOKEN.strip()
    
    if not token or token == 'YOUR_TOKEN_HERE':
        print("[ОШИБКА] Discord токен не найден в файле .env!")
        print("[ИНФОРМАЦИЯ] Пожалуйста, добавьте ваш токен в файл .env:")
        print("             DISCORD_TOKEN=your_token_here")
        print()
        print("Получите токен на: https://discord.com/developers/applications")
        return
    
    async with bot:
        # Загрузка расширений
        await load_cogs()
        
        # Запуск бота
        try:
            await bot.start(token)
        except discord.errors.LoginFailure:
            print("[ОШИБКА] Неверный Discord токен!")
            print("[ВНИМАНИЕ] Пожалуйста, проверьте ваш токен на:")
            print("           https://discord.com/developers/applications")
        except Exception as e:
            print(f"[ОШИБКА] Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
