import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
from .utils import get_rgb_color

class Moderasyon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ban', help='Kullanıcıyı sunucudan yasaklar (MEE6/ProBot/MC-AT).')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(description=f"{member} banlandı! Sebep: {reason or 'Belirtilmedi'}", color=get_rgb_color())
        await ctx.send(embed=embed)

    @commands.command(name='clear', help='1-400 mesaj siler (MC-AT).')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        if amount < 1 or amount > 400:
            await ctx.send(embed=discord.Embed(description="Lütfen 1 ile 400 arasında bir sayı girin.", color=get_rgb_color()))
            return
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(description=f"{amount} mesaj silindi!", color=get_rgb_color())
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name='automod', help='Otomatik moderasyon ayarlarını gösterir/ayarlar (Carl-bot).')
    @commands.has_permissions(manage_guild=True)
    async def automod(self, ctx, action: str = None, value: str = None):
        with open('automod.json', 'r') as f:
            settings = json.load(f)
        guild_id = str(ctx.guild.id)
        if guild_id not in settings:
            settings[guild_id] = {"küfür": False, "reklam": False, "spam": False}
        if action == "küfür":
            settings[guild_id]["küfür"] = value.lower() == "aç"
            embed = discord.Embed(description=f"Küfür filtresi {'açıldı' if settings[guild_id]['küfür'] else 'kapatıldı'}.", color=get_rgb_color())
        elif action == "reklam":
            settings[guild_id]["reklam"] = value.lower() == "aç"
            embed = discord.Embed(description=f"Reklam filtresi {'açıldı' if settings[guild_id]['reklam'] else 'kapatıldı'}.", color=get_rgb_color())
        else:
            embed = discord.Embed(
                title="Otomatik Moderasyon Ayarları",
                description=f"Küfür: {'Açık' if settings[guild_id]['küfür'] else 'Kapalı'}\nReklam: {'Açık' if settings[guild_id]['reklam'] else 'Kapalı'}",
                color=get_rgb_color()
            )
        with open('automod.json', 'w') as f:
            json.dump(settings, f)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderasyon(bot))