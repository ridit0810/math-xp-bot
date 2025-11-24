import discord
from discord.ext import commands
import asyncio
import json
import random
import os

class GradeSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="11th Grade", value="11"),
            discord.SelectOption(label="12th Grade", value="12")
        ]
        super().__init__(placeholder="Select your Grade", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Now select topic:", view=TopicView(), ephemeral=True)

class GradeView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(GradeSelect())

# ------------------ TOPIC ----------------------

class TopicSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Geometric Progression", value="gp")
        ]
        super().__init__(placeholder="Select Topic", options=options)

    async def callback(self, interaction: discord.Interaction):
        topic = self.values[0]
        # Pass the selected topic to the DifficultyView
        await interaction.response.send_message("Select difficulty:", view=DifficultyView(topic), ephemeral=True)

class TopicView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TopicSelect())

# ------------------ DIFFICULTY ----------------------

class DifficultySelect(discord.ui.Select):
    def __init__(self, topic):
        self.topic = topic
        options = [
            discord.SelectOption(label="Easy", value="easy"),
            discord.SelectOption(label="Medium", value="medium"),
            discord.SelectOption(label="Hard", value="hard")
        ]
        super().__init__(placeholder="Select Difficulty", options=options)

    async def callback(self, interaction: discord.Interaction):
        difficulty = self.values[0]
        await interaction.response.send_message(f"Difficulty selected: **{difficulty}**", ephemeral=True)

        # Dynamic File Loading
        filename = f"./data/{self.topic}.json"
        
        if not os.path.exists(filename):
             return await interaction.followup.send(f"❌ Error: Question file `{filename}` not found!")

        with open(filename, "r") as f:
            data = json.load(f)

        # Filter questions by difficulty if possible, or just pick random
        # For now, we pick random as per original logic, but we could filter here.
        question = random.choice(data["questions"])
        
        embed = discord.Embed(
            title="Math Question",
            description=question["question"],
            color=discord.Color.blue()
        )

        for i, option in enumerate(question["options"]):
            embed.add_field(name=f"Option {chr(65+i)}", value=option, inline=False)

        # Set Timer per difficulty
        if difficulty == "easy":
            timeout = 15
        elif difficulty == "medium":
            timeout = 45
        else:
            timeout = 120

        embed.set_footer(text=f"Type A, B, C, or D to answer! You have {timeout} seconds.")

        await interaction.followup.send(embed=embed)

        # Wait for answer
        def check(msg):
            return msg.author.id == interaction.user.id and msg.channel == interaction.channel

        try:
            msg = await interaction.client.wait_for("message", timeout=timeout, check=check)
        except asyncio.TimeoutError:
            return await interaction.followup.send("⏳ Time's up! No XP awarded.")

        # Check correctness
        correct = question["answer"].upper()
        user_answer = msg.content.upper().strip()

        if user_answer == correct:
            xp_cog = interaction.client.get_cog("XPSystem")
            if xp_cog:
                level_up = xp_cog.add_xp(interaction.user.id, 50)
                if level_up:
                    await interaction.followup.send("🎉 Correct! +50 XP\n⭐ **LEVEL UP!**")
                else:
                    await interaction.followup.send("✅ Correct! +50 XP")
            else:
                 await interaction.followup.send("✅ Correct! (XP System not loaded)")

        else:
            await interaction.followup.send(f"❌ Incorrect! The correct answer was **{correct}**.")


class DifficultyView(discord.ui.View):
    def __init__(self, topic):
        super().__init__()
        self.add_item(DifficultySelect(topic))

# ------------ COMMAND -------------

class MathGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def math(self, ctx):
        """Start the math game."""
        await ctx.send("Select your grade:", view=GradeView())

async def setup(bot):
    await bot.add_cog(MathGame(bot))
