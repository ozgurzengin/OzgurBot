import discord
from discord.ext import commands
import random
from .utils import get_rgb_color

class Eglence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='meme', help='Rastgele bir meme gönderir (Dank Memer/Cafe).')
    async def meme(self, ctx, type: str = None):
        memes = ["https://i.imgur.com/example.jpg", "https://i.imgur.com/funny.jpg"]  # Gerçek meme API eklenebilir
        if type == "coffee":
            memes = ["https://i.imgur.com/coffee.jpg"]  # Cafe'nin coffee-meme özelliği
        embed = discord.Embed(title="İşte bir meme!", color=get_rgb_color())
        embed.set_image(url=random.choice(memes))
        await ctx.send(embed=embed)

    @commands.command(name='8ball', help='Magik 8ball’a soru sor (Dank Memer/Cafe).')
    async def eight_ball(self, ctx, *, question: str):
        responses = ["Kesinlikle!", "Hayır.", "Belki.", "Bilmiyorum, sen ne düşünüyorsun?"]
        embed = discord.Embed(
            title="8Ball Cevabı",
            description=f"Soru: {question}\nCevap: {random.choice(responses)}",
            color=get_rgb_color()
        )
        await ctx.send(embed=embed)

    @commands.command(name='hug', help='Birine sanal sarılma gönderir (OwO/Cafe).')
    async def hug(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"{ctx.author.mention}, {member.mention}'a sarıldı! 🤗", color=get_rgb_color())
        await ctx.send(embed=embed)

    @commands.command(name='duello', help='Birine düello teklif eder (ErensiBOT).')
    async def duello(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"{ctx.author.mention}, {member.mention}'a düello teklif etti! ⚔️", color=get_rgb_color())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Eglence(bot))
