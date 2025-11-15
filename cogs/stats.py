"""
Модуль для визуализации статистики сервера
"""
import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
from datetime import datetime, timedelta
import config

# Используем Agg backend для работы без GUI
matplotlib.use('Agg')


class Stats(commands.Cog):
    """Команды для получения и визуализации статистики сервера"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='server_stats', aliases=['stats', 'server'])
    async def server_stats(self, ctx):
        """Показывает основную статистику сервера"""
        guild = ctx.guild
        
        # Получение информации о сервере
        total_members = guild.member_count
        bots = sum(1 for member in guild.members if member.bot)
        humans = total_members - bots
        
        online = sum(1 for member in guild.members if member.status != discord.Status.offline)
        channels = len(guild.channels)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        roles = len(guild.roles)
        
        # Создание встраиваемого сообщения
        embed = discord.Embed(
            title=f"📊 Статистика сервера: {guild.name}",
            description=f"Полная информация о сервере",
            color=config.CVETA['osnovnoy'],
            timestamp=datetime.now()
        )
        
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        
        # Основная информация
        embed.add_field(name="👥 Члены", value=f"Всего: **{total_members}**\nЛюди: **{humans}**\nБоты: **{bots}**\nОнлайн: **{online}**", inline=False)
        
        embed.add_field(name="💬 Каналы", value=f"Текстовых: **{text_channels}**\nГолосовых: **{voice_channels}**\nВсего: **{channels}**", inline=False)
        
        embed.add_field(name="🏷️ Роли", value=f"Всего ролей: **{roles}**", inline=False)
        
        embed.add_field(name="📅 Информация", value=f"ID сервера: `{guild.id}`\nВладелец: {guild.owner.mention}\nСоздан: <t:{int(guild.created_at.timestamp())}:F>", inline=False)
        
        embed.set_footer(text=f"Запрос от {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='member_graph')
    async def member_graph(self, ctx):
        """Показывает график распределения пользователей и ботов"""
        guild = ctx.guild
        
        total_members = guild.member_count
        bots = sum(1 for member in guild.members if member.bot)
        humans = total_members - bots
        
        # Создание графика
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=config.NASTROJKI_GRAFIKOV['razmer'])
        fig.patch.set_facecolor('#2C2F33')
        
        # График 1: Круговая диаграмма
        labels = ['👤 Люди', '🤖 Боты']
        sizes = [humans, bots]
        colors = ['#5865F2', '#FFA500']
        explode = (0.05, 0)
        
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90, textprops={'color': 'white', 'fontsize': 12})
        ax1.set_title('Распределение участников', color='white', fontsize=14, fontweight='bold')
        
        # График 2: Столбчатая диаграмма
        categories = ['Люди', 'Боты']
        values = [humans, bots]
        bars = ax2.bar(categories, values, color=['#5865F2', '#FFA500'], edgecolor='white', linewidth=2)
        
        # Добавление значений на столбцы
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', color='white', fontsize=12, fontweight='bold')
        
        ax2.set_ylabel('Количество', color='white', fontsize=12)
        ax2.set_title('Количество участников', color='white', fontsize=14, fontweight='bold')
        ax2.tick_params(colors='white')
        ax2.spines['bottom'].set_color('white')
        ax2.spines['left'].set_color('white')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        plt.tight_layout()
        
        # Сохранение в буфер
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=config.NASTROJKI_GRAFIKOV['dpi'], facecolor='#2C2F33')
        buffer.seek(0)
        plt.close()
        
        # Отправка файла
        file = discord.File(buffer, filename='member_stats.png')
        embed = discord.Embed(
            title="📊 График распределения участников",
            color=config.CVETA['osnovnoy'],
            timestamp=datetime.now()
        )
        embed.set_image(url='attachment://member_stats.png')
        embed.set_footer(text=f"Запрос от {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed, file=file)
    
    @commands.command(name='channel_stats')
    async def channel_stats(self, ctx):
        """Показывает статистику по каналам"""
        guild = ctx.guild
        
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        total_channels = text_channels + voice_channels
        
        # Создание графика
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#2C2F33')
        
        labels = ['💬 Текстовые каналы', '🔊 Голосовые каналы']
        sizes = [text_channels, voice_channels]
        colors = ['#5865F2', '#43B581']
        explode = (0.05, 0.05)
        
        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors, 
                                           autopct='%1.1f%%', shadow=True, startangle=90,
                                           textprops={'color': 'white', 'fontsize': 12})
        
        ax.set_title(f'Распределение каналов ({total_channels} всего)', 
                    color='white', fontsize=14, fontweight='bold')
        
        # Стилизация текста
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(11)
        
        plt.tight_layout()
        
        # Сохранение в буфер
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=config.NASTROJKI_GRAFIKOV['dpi'], facecolor='#2C2F33')
        buffer.seek(0)
        plt.close()
        
        # Отправка файла
        file = discord.File(buffer, filename='channel_stats.png')
        embed = discord.Embed(
            title="📊 Статистика каналов",
            description=f"Текстовых: **{text_channels}**\nГолосовых: **{voice_channels}**",
            color=config.CVETA['uspeh'],
            timestamp=datetime.now()
        )
        embed.set_image(url='attachment://channel_stats.png')
        embed.set_footer(text=f"Запрос от {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed, file=file)
    
    @commands.command(name='role_list')
    async def role_list(self, ctx):
        """Показывает список ролей сервера"""
        guild = ctx.guild
        roles = guild.roles[1:]  # Исключаем роль @everyone
        roles.reverse()  # От выше к ниже
        
        if not roles:
            embed = discord.Embed(
                title="ℹ️ Информация",
                description="На этом сервере нет ролей (кроме @everyone)",
                color=config.CVETA['info']
            )
            await ctx.send(embed=embed)
            return
        
        # Разделение на страницы (10 ролей на страницу)
        page_size = 10
        pages = []
        
        for i in range(0, len(roles), page_size):
            page_roles = roles[i:i + page_size]
            role_text = "\n".join([f"{idx + 1}. {role.mention} (`{role.id}`)" 
                                  for idx, role in enumerate(page_roles)])
            pages.append(role_text)
        
        # Создание встраиваемого сообщения
        embed = discord.Embed(
            title=f"🏷️ Роли сервера ({len(roles)} всего)",
            description=pages[0] if pages else "Нет ролей",
            color=config.CVETA['osnovnoy'],
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Страница 1/{len(pages)} • Запрос от {ctx.author}", 
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Загрузка расширения в бот"""
    await bot.add_cog(Stats(bot))
