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
APPLICATION_ID: Final[int] = int(os.getenv("APPLICATION_ID", 0))
GUILD_ID: Final[int] = int(os.getenv("GUILD_ID", 0))

# Bot startup with intents
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="/", intents=intents, application_id=APPLICATION_ID)

# EVENT: Bot Ready
@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")
    try:
        bot.tree.copy_global_to(guild=discord.Object(id=GUILD_ID))
        synced_commands = await bot.tree.sync(guild=discord.Object(id=GUILD_ID)) 
        print(f"Synced {len(synced_commands)} comamnds.")
    except Exception as e:
        print(f"Error syncing: {e}")


async def main():
    async with bot:
        await bot.load_extension("cogs.bot")
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())