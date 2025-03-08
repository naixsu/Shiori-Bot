from discord import Interaction
from discord.ext import commands
from discord import app_commands
from helpers.responses import send_message
from helpers.tracker import Tracker


class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tracker = Tracker(worksheet_no=0)

    @app_commands.command(name="test", description="tests command")
    async def test(self, interaction: Interaction):
        await interaction.response.send_message("Test")

    @app_commands.command(name="update_cell", description="Updates a cell in the tracker")
    @app_commands.describe(row="Row number", column="Column number", value="New value to insert")
    async def update_cell(self, interaction: Interaction, row: int, column: int, value: str):
        """Handles the /update_cell command"""
        cell_position = (row, column)
        response = self.tracker.update_cell(cell_position, value)
        await interaction.response.send_message(response)


async def setup(bot):
    await bot.add_cog(Bot(bot))
