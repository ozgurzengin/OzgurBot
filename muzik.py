```python
    import discord
    from discord.ext import commands
    import youtube_dl
    from .utils import get_rgb_color

    class Muzik(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        @commands.command(name='play', help='YouTube’dan müzik çalar (Rythm).')
        async def play(self, ctx, url: str):
            if not ctx.author.voice:
                embed = discord.Embed(description="Bir ses kanalında olmalısın!", color=get_rgb_color())
                await ctx.send(embed=embed)
                return
            channel = ctx.author.voice.channel
            if ctx.guild.voice_client is None:
                await channel.connect()
            ydl_opts = {'format': 'bestaudio'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                ctx.guild.voice_client.play(discord.FFmpegPCMAudio(url2))
            embed = discord.Embed(description=f"Çalınıyor: {info['title']}", color=get_rgb_color())
            await ctx.send(embed=embed)

        @commands.command(name='stop', help='Müziği durdurur (Rythm).')
        async def stop(self, ctx):
            if ctx.guild.voice_client:
                ctx.guild.voice_client.stop()
                await ctx.guild.voice_client.disconnect()
                embed = discord.Embed(description="Müzik durduruldu!", color=get_rgb_color())
                await ctx.send(embed=embed)

    async def setup(bot):
        await bot.add_cog(Muzik(bot))
    ```
