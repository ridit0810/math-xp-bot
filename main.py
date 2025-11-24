import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random



load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = '.', intents=intents, help_command=None)

@bot.command(name="help")
async def help_command(ctx):
    """Displays this help message."""
    embed = discord.Embed(title="Bot Commands", description="Here are the available commands:", color=discord.Color.green())
    
    for command in bot.commands:
        if not command.hidden:
            help_text = command.help or "No description provided."
            embed.add_field(name=f".{command.name}", value=help_text, inline=False)
            
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f'We are Ready, {bot.user.name}')


@bot.event
async def on_member_join(member):
    await member.send(f"welcome to server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

async def load_extensions():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

import asyncio
asyncio.run(main())
