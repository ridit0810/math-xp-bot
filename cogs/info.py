import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):
        """Display information about the server."""
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.blue())
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Member Count", value=guild.member_count, inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        """Display information about a user."""
        if member is None:
            member = ctx.author

        embed = discord.Embed(title=f"User Info: {member.name}", color=member.color)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Created Account", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.set_thumbnail(url=member.display_avatar.url)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
