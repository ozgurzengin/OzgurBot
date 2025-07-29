import discord
from discord.ext import commands
import json
from .utils import get_rgb_color

class Sosyal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='creategroup', help='Oyun grubu oluşturur (Gankster Groups).')
    async def creategroup(self, ctx, game: str):
        with open('groups.json', 'r') as f:
            groups = json.load(f)
        guild_id = str(ctx.guild.id)
        if guild_id not in groups:
            groups[guild_id] = []
        group_id = f"{ctx.author.id}-{int(time.time())}"
        groups[guild_id].append({"id": group_id, "game": game, "creator": ctx.author.id, "members": [ctx.author.id]})
        with open('groups.json', 'w') as f:
            json.dump(groups, f)
        embed = discord.Embed(description=f"{ctx.author.mention}, {game} için grup oluşturuldu! ID: {group_id}", color=get_rgb_color())
        await ctx.send(embed=embed)

    @commands.command(name='thank', help='Kullanıcıya teşekkür eder ve puan verir (Cortex Bot Yazılım).')
    async def thank(self, ctx, member: discord.Member, amount: int = 1):
        with open('points.json', 'r') as f:
            points = json.load(f)
        user_id = str(member.id)
        if user_id not in points:
            points[user_id] = 0
        points[user_id] += amount
        with open('points.json', 'w') as f:
            json.dump(points, f)
        embed = discord.Embed(description=f"{ctx.author.mention}, {member.mention}'a {amount} puan teşekkür olarak verdi!", color=get_rgb_color())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Sosyal(bot))