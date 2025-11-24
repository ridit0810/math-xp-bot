import discord
from discord.ext import commands
import asyncio
import re  # for parsing time formats

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="remindme")
    async def remindme(self, ctx, time: str, *, reminder: str):
        """
        Set a reminder using formats like:
        10s = 10 seconds
        5m = 5 minutes
        2h = 2 hours
        """
        
        # Regex to extract number + unit
        match = re.match(r"^(\d+)(s|m|h)$", time.lower())
        if not match:
            return await ctx.send(
                "❌ Invalid time format! Use examples like:\n"
                "`10s` (seconds), `5m` (minutes), `2h` (hours)"
            )

        value, unit = match.groups()
        value = int(value)

        # Convert to seconds
        if unit == "s":
            delay = value
        elif unit == "m":
            delay = value * 60
        elif unit == "h":
            delay = value * 3600

        await ctx.send(f"⏳ Okay! I will remind you in **{time}**.")

        # The actual wait
        await asyncio.sleep(delay)

        # Send reminder
        await ctx.send(f"⏰ **Reminder:** {ctx.author.mention} {reminder}")

async def setup(bot):
    await bot.add_cog(Reminder(bot))
