import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, *, msg):
        """Create a poll with thumbs up/down reactions."""
        embed = discord.Embed(title="New poll", description=msg)
        poll_message = await ctx.send(embed=embed)
        await poll_message.add_reaction('👍')
        await poll_message.add_reaction('👎')

async def setup(bot):
    await bot.add_cog(Fun(bot))
