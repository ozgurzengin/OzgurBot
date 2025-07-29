import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import colorsys
import time
import json
from datetime import datetime, timedelta
import random

# Çevresel değişkenleri yükle
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot intentlerini ayarla
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True
intents.voice_states = True

# Botu başlat
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# RGB renk efekti
def get_rgb_color():
    t = time.time() % 6 / 6
    r, g, b = colorsys.hsv_to_rgb(t, 1, 1)
    return discord.Color.from_rgb(int(r * 255), int(g * 255), int(b * 255))

# Cog'ları yükle
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# Bot başlatıldığında
@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')
    await bot.change_presence(activity=discord.Game(name="!yardim | ÖzgürBot"))

# Yardım komutu
@bot.command(name='yardim', help='Tüm komut kategorilerini veya belirli bir komutun detaylarını gösterir.')
async def help_command(ctx, command: str = None):
    if command:
        cmd = bot.get_command(command)
        if cmd:
            embed = discord.Embed(
                title=f"Komut: !{command}",
                description=cmd.help or "Açıklama yok.",
                color=get_rgb_color()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"`!{command}` adında bir komut bulunamadı!", color=get_rgb_color())
            await ctx.send(embed=embed)
        return

    embed = discord.Embed(
        title="ÖzgürBot Yardım Menüsü",
        description="Tüm komut kategorileri ve örnek komutlar. Detay için `!yardim <komut>`.",
        color=get_rgb_color()
    )
    categories = {
        "Admin": ["ban", "clear", "kick", "mute", "automod", "slowmode"],
        "Eğlence": ["meme", "8ball", "hug", "coffee-meme", "coinflip", "duello"],
        "Müzik": ["play", "stop", "skip", "queue", "bassboost", "loop"],
        "Ekonomi": ["balance", "daily", "transfer", "gamble", "points"],
        "Seviye": ["rank", "setxp", "top", "leaderboard"],
        "Araçlar": ["serverinfo", "userinfo", "avatar", "ping", "code"],
        "Koruma": ["küfürengel", "reklamengel", "censor", "attachmentspam"],
        "Kayıt": ["kayıt", "otorol", "ototag"],
        "Oyunlar": ["roll", "hunt", "battle", "trivia", "connect4"],
        "Sosyal": ["membercount", "vent", "creategroup", "thank"],
        "Ticket": ["ticket create", "ticket close", "ticket setup"]
    }
    for category, commands in categories.items():
        embed.add_field(
            name=category,
            value=", ".join([f"`!{cmd}`" for cmd in commands[:5]]) + (f", ve daha fazlası..." if len(commands) > 5 else ""),
            inline=False
        )
    embed.set_footer(text="ÖzgürBot | !yardim <komut> ile detaylı bilgi.")
    await ctx.send(embed=embed)

# Hata yönetimi
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description="Bu komutu kullanmak için gerekli izinlere sahip değilsiniz!", color=get_rgb_color())
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description="Lütfen gerekli tüm parametreleri sağlayın!", color=get_rgb_color())
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(description="Geçersiz bir parametre girdiniz!", color=get_rgb_color())
    else:
        embed = discord.Embed(description=f"Bir hata oluştu: {error}", color=get_rgb_color())
    await ctx.send(embed=embed)

# Botu başlat
async def main():
    await load_cogs()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())