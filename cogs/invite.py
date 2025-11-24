import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        """Get the invite link to add this bot to your server."""
        invite_url = "https://discord.com/oauth2/authorize?client_id=1442208496975085658&permissions=8&integration_type=0&scope=bot"
        
        embed = discord.Embed(
            title="📨 Invite Me to Your Server!",
            description=f"Click the link below to add me to your server:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Invite Link", value=f"[Click Here]({invite_url})", inline=False)
        embed.set_footer(text="Thanks for using this bot!")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Invite(bot))
