import discord
from discord.ext import commands
import json
from .utils import get_rgb_color

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ticket', help='Ticket oluşturur veya yönetir (Ticket Tool).')
    async def ticket(self, ctx, action: str = None, target: discord.Member = None):
        with open('tickets.json', 'r') as f:
            tickets = json.load(f)
        guild_id = str(ctx.guild.id)
        if guild_id not in tickets:
            tickets[guild_id] = {}

        if action == "create":
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            channel = await ctx.guild.create_text_channel(f"ticket-{ctx.author.name}", overwrites=overwrites)
            tickets[guild_id][str(channel.id)] = {"owner": ctx.author.id, "status": "open"}
            with open('tickets.json', 'w') as f:
                json.dump(tickets, f)
            embed = discord.Embed(description=f"Ticket oluşturuldu: {channel.mention}", color=get_rgb_color())
            await ctx.send(embed=embed)

        elif action == "close":
            if str(ctx.channel.id) in tickets[guild_id] and tickets[guild_id][str(ctx.channel.id)]["status"] == "open":
                tickets[guild_id][str(ctx.channel.id)]["status"] = "closed"
                with open('tickets.json', 'w') as f:
                    json.dump(tickets, f)
                embed = discord.Embed(description="Ticket kapatıldı!", color=get_rgb_color())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description="Bu kanal bir ticket değil veya zaten kapalı!", color=get_rgb_color())
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ticket(bot))