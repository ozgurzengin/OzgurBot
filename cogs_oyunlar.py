import discord
from discord.ext import commands
import random
from .utils import get_rgb_color

class Oyunlar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}  # Kanal bazında oyun verileri

    @commands.command(name='roll', help='Zar atar (CortexPal2000).')
    async def roll(self, ctx, dice: str):
        try:
            dice_list = dice.split()
            results = []
            for die in dice_list:
                if die.startswith('d'):
                    sides = int(die[1:])
                    result = random.randint(1, sides)
                    results.append(f"d{sides}: **{result}**")
            embed = discord.Embed(
                description=f"Zar sonuçları: {', '.join(results)}",
                color=get_rgb_color()
            )
            await ctx.send(embed=embed)
        except ValueError:
            embed = discord.Embed(description="Geçersiz zar formatı! Örnek: `d6 d8`", color=get_rgb_color())
            await ctx.send(embed=embed)

    @commands.command(name='hunt', help='Canavar avına çıkar (OwO).')
    async def hunt(self, ctx):
        rewards = ["100 coin", "Kılıç", "Zırh", "Nadir Canavar"]
        reward = random.choice(rewards)
        embed = discord.Embed(description=f"{ctx.author.mention} avdan {reward} kazandı!", color=get_rgb_color())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Oyunlar(bot))