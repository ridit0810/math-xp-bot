import discord
from discord.ext import commands
import random

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """Says hello back to you."""
        await ctx.send("Hello!")

    @commands.command()
    async def ping(self, ctx):
        """Check the bot's latency."""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        """Displays a user's avatar."""
        if member is None:
            member = ctx.author
        await ctx.send(member.display_avatar.url)

    @commands.command()
    async def roll(self, ctx, sides: int = 6):
        """Roll a dice with N sides (default 6)."""
        await ctx.send(f'You rolled a {random.randint(1, sides)}')

async def setup(bot):
    await bot.add_cog(Utility(bot))
