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

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    application_id=APPLICATION_ID,
    help_command=None,
)

@bot.command(name="help")
async def custom_help(ctx):
    embed = discord.Embed(
        title="Shiori is here to help you!",
        description="List of available commands:",
        color=discord.Color.green(),
    )

    embed.add_field(name="!help", value="Shows this help message.", inline=False)

    embed.add_field(
        name="/rem",
        value="Displays remaining hits for today. Only works during CB period.",
        inline=False
    )

    embed.add_field(
        name="/get_ot",
        value=(
            "**Calculates the Overkill Time (OT).**\n"
            "**Arguments:**\n"
            "- `boss_hp`: Boss HP in millions (e.g., `400`)\n"
            "- `first_hit`: First hit's damage in millions (optional, e.g., `200`)\n"
            "- `second_hit`: Second hit's damage in millions (optional, e.g., `180`)"
        ),
        inline=False
    )

    embed.add_field(
        name="/update_cell",
        value=(
            "**Beta (idk if I'll work on this lol)**\n"
            "**Updates a cell in the tracker.** *(Requires `Cult Quintet` role)*\n"
            "**Arguments:**\n"
            "- `cell`: Cell position in A1 notation (e.g., `'C3'`) or tuple `(row, col)`\n"
            "- `value`: Boss notation (e.g., `'D1'`)"
        ),
        inline=False
    )

    await ctx.send(embed=embed)

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