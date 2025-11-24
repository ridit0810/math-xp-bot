import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}  # Temporary warning storage: {user_id: warnings_count}

    # ==========================
    # KICK COMMAND
    # ==========================
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_command(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member from the server."""
        if member == ctx.author:
            return await ctx.send("You cannot kick yourself.")
        await member.kick(reason=reason)
        await ctx.send(f"🚨 {member.mention} was kicked.\n📝 Reason: **{reason}**")

    @kick_command.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have permission to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `.kick @user <reason>`")

    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if member == interaction.user:
            return await interaction.response.send_message("You cannot kick yourself.", ephemeral=True)
        await member.kick(reason=reason)
        await interaction.response.send_message(f"🚨 {member.mention} was kicked.\n📝 Reason: **{reason}**")

    # ==========================
    # BAN COMMAND
    # ==========================
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_command(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member from the server."""
        if member == ctx.author:
            return await ctx.send("You cannot ban yourself.")
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} was banned.\n📝 Reason: **{reason}**")

    @ban_command.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have permission to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `.ban @user <reason>`")

    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if member == interaction.user:
            return await interaction.response.send_message("You cannot ban yourself.", ephemeral=True)
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 {member.mention} was banned.\n📝 Reason: **{reason}**")

    # ==========================
    # UNBAN COMMAND
    # ==========================
    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban_command(self, ctx, user_id: int):
        """Unban a user by their ID."""
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.send(f"♻️ {user.name} has been unbanned.")
        except discord.NotFound:
            await ctx.send("❌ User not found.")
        except discord.HTTPException:
            await ctx.send("❌ Failed to unban user.")

    @unban_command.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have permission to use this command.")

    @app_commands.command(name="unban", description="Unban a user by their ID")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban_slash(self, interaction: discord.Interaction, user_id: str):
        try:
            user = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"♻️ {user.name} has been unbanned.")
        except ValueError:
            await interaction.response.send_message("❌ Invalid user ID.", ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message("❌ User not found.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("❌ Failed to unban user.", ephemeral=True)

    # ==========================
    # WARN COMMAND
    # ==========================
    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn_command(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Warn a member."""
        if member == ctx.author:
            return await ctx.send("You cannot warn yourself.")
        self.warnings[member.id] = self.warnings.get(member.id, 0) + 1
        await ctx.send(f"⚠️ {member.mention} warned. Total: **{self.warnings[member.id]}**\n📝 Reason: **{reason}**")

    @warn_command.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You lack `Manage Messages` permission.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `.warn @user <reason>`")

    @app_commands.command(name="warn", description="Warn a member")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if member == interaction.user:
            return await interaction.response.send_message("You cannot warn yourself.", ephemeral=True)
        self.warnings[member.id] = self.warnings.get(member.id, 0) + 1
        await interaction.response.send_message(f"⚠️ {member.mention} warned. Total: **{self.warnings[member.id]}**\n📝 Reason: **{reason}**")

    # ==========================
    # MUTE (TIMEOUT) COMMAND
    # ==========================
    @commands.command(name="mute")
    @commands.has_permissions(moderate_members=True)
    async def mute_command(self, ctx, member: discord.Member, duration: int, *, reason="No reason provided"):
        """Mute a member for X minutes."""
        if member == ctx.author:
            return await ctx.send("You cannot mute yourself.")
        await member.timeout(datetime.timedelta(minutes=duration), reason=reason)
        await ctx.send(f"🔇 {member.mention} muted for **{duration} min**\n📝 Reason: **{reason}**")

    @mute_command.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You lack `Moderate Members` permission.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `.mute @user <minutes> <reason>`")

    @app_commands.command(name="mute", description="Mute a member for X minutes")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute_slash(self, interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason provided"):
        if member == interaction.user:
            return await interaction.response.send_message("You cannot mute yourself.", ephemeral=True)
        await member.timeout(datetime.timedelta(minutes=duration), reason=reason)
        await interaction.response.send_message(f"🔇 {member.mention} muted for **{duration} min**\n📝 Reason: **{reason}**")

    # ==========================
    # UNMUTE COMMAND
    # ==========================
    @commands.command(name="unmute")
    @commands.has_permissions(moderate_members=True)
    async def unmute_command(self, ctx, member: discord.Member):
        """Remove mute from a member."""
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} has been unmuted.")

    @unmute_command.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You lack `Moderate Members` permission.")

    @app_commands.command(name="unmute", description="Remove mute from a member")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute_slash(self, interaction: discord.Interaction, member: discord.Member):
        await member.timeout(None)
        await interaction.response.send_message(f"🔊 {member.mention} has been unmuted.")

    # ==========================
    # PURGE/CLEAR COMMAND
    # ==========================
    @commands.command(name="purge", aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge_command(self, ctx, amount: int = 5):
        """Delete a specified number of messages (default 5)."""
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"🧹 Deleted **{amount}** messages.")
        await msg.delete(delay=5)

    @purge_command.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")

    @app_commands.command(name="purge", description="Delete multiple messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge_slash(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"🧹 Deleted **{amount}** messages.", ephemeral=True)

    # ==========================
    # LOCK CHANNEL COMMAND
    # ==========================
    @commands.command(name="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock_command(self, ctx):
        """Lock the current channel."""
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Channel locked.")

    @lock_command.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You lack `Manage Channels` permission.")

    @app_commands.command(name="lock", description="Lock the current channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock_slash(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await interaction.response.send_message("🔒 Channel locked.")

    # ==========================
    # UNLOCK CHANNEL COMMAND
    # ==========================
    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock_command(self, ctx):
        """Unlock the current channel."""
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Channel unlocked.")

    @unlock_command.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You lack `Manage Channels` permission.")

    @app_commands.command(name="unlock", description="Unlock the current channel")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock_slash(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        await interaction.response.send_message("🔓 Channel unlocked.")

    # ==========================
    # SLOWMODE COMMAND
    # ==========================
    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode_command(self, ctx, seconds: int):
        """Set channel slowmode delay in seconds."""
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send("🐢 Slowmode disabled.")
        else:
            await ctx.send(f"🐢 Slowmode set to **{seconds} sec**.")

    @slowmode_command.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You lack `Manage Channels` permission.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `.slowmode <seconds>`")

    @app_commands.command(name="slowmode", description="Set channel slowmode")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode_slash(self, interaction: discord.Interaction, seconds: int):
        await interaction.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await interaction.response.send_message("🐢 Slowmode disabled.")
        else:
            await interaction.response.send_message(f"🐢 Slowmode set to **{seconds} sec**.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
