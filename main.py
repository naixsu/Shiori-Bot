import discord
import os
import asyncio

from typing import Final
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

# Load token
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
DISCORD_TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

# Bot startup with intents
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix='$', intents=intents)

# EVENT: Bot Ready
@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")


async def main():
    async with bot:
        await bot.load_extension('cogs.sheet')
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())