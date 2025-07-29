import discord
from discord.ext import commands
import random
import json
from datetime import datetime
from .utils import get_rgb_color

class Ekonomi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='balance', help='Kullanıcının bakiyesini gösterir (Dank Memer/Cafe/OwO).')
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        with open('economy.json', 'r') as f:
            economy = json.load(f)
        user_id = str(member.id)
        if user_id not in economy:
            economy[user_id] = {"pocket": 100, "bank": 0, "last_daily": None}
            with open('economy.json', 'w') as f:
                json.dump(economy, f)
        embed = discord.Embed(
            description=f"{member.mention} Bakiye:\nCüzdan: {economy[user_id]['pocket']} coin\nBanka: {economy[user_id]['bank']} coin",
            color=get_rgb_color()
        )
        await ctx.send(embed=embed)

    @commands.command(name='daily', help='Günlük ödül alır (Dank Memer/OwO).')
    async def daily(self, ctx):
        with open('economy.json', 'r') as f:
            economy = json.load(f)
        user_id = str(ctx.author.id)
        if user_id not in economy:
            economy[user_id] = {"pocket": 100, "bank": 0, "last_daily": None}
        last_daily = economy[user_id].get("last_daily")
        if last_daily and (datetime.utcnow() - datetime.fromisoformat(last_daily)).days < 1:
            embed = discord.Embed(description="Günlük ödül için 24 saat beklemelisin!", color=get_rgb_color())
            await ctx.send(embed=embed)
            return
        amount = random.randint(100, 500)
        economy[user_id]["pocket"] += amount
        economy[user_id]["last_daily"] = datetime.utcnow().isoformat()
        with open('economy.json', 'w') as f:
            json.dump(economy, f)
        embed = discord.Embed(description=f"{ctx.author.mention}, {amount} coin kazandın!", color=get_rgb_color())
        await ctx.send(embed=embed)

    @commands.command(name='transfer', help='Başka kullanıcıya coin gönderir (Cafe/OwO).')
    async def transfer(self, ctx, member: discord.Member, amount: int):
        with open('economy.json', 'r') as f:
            economy = json.load(f)
        sender_id = str(ctx.author.id)
        receiver_id = str(member.id)
        if sender_id not in economy or economy[sender_id]["pocket"] < amount:
            embed = discord.Embed(description="Yeterli coinin yok!", color=get_rgb_color())
            await ctx.send(embed=embed)
            return
        if receiver_id not in economy:
            economy[receiver_id] = {"pocket": 0, "bank": 0, "last_daily": None}
        economy[sender_id]["pocket"] -= amount
        economy[receiver_id]["pocket"] += amount
        with open('economy.json', 'w') as f:
            json.dump(economy, f)
        embed = discord.Embed(description=f"{ctx.author.mention}, {member.mention}'a {amount} coin gönderdi!", color=get_rgb_color())
        await ctx.send(embed=embed)

    @commands.command(name='points', help='Kullanıcının puanlarını gösterir (Cortex Bot Yazılım).')
    async def points(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        with open('points.json', 'r') as f:
            points = json.load(f)
        user_id = str(member.id)
        if user_id not in points:
            points[user_id] = 0
            with open('points.json', 'w') as f:
                json.dump(points, f)
        embed = discord.Embed(description=f"{member.mention}'ın puanı: {points[user_id]}", color=get_rgb_color())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ekonomi(bot))
