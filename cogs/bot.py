import re

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

    # TODO: validate the `cell` to only match the valid cells of the player
    # TODO: validste the `value` to only allow valid boss notations
    @app_commands.command(name="update_cell", description="Updates a cell in the tracker")
    @app_commands.describe(
        cell="Cell position in A1 notation (e.g., 'C3') or (row, col) || row,col tuple",
        value="Boss notation (e.g., 'D1')"
    )
    async def update_cell(self, interaction: Interaction, cell: str, value: str):
        # Validate and process cell input
        cell_position = self._parse_cell_input(cell)

        if not cell_position:
            await interaction.response.send_message(
                "Invalid cell format. Provide either A1 notation (e.g., 'C3') or a (row, col) tuple.",
                ephemeral=True,
            )
            return

        # Update the cell
        response = self.tracker.update_cell(cell_position, value)
        await interaction.response.send_message(response)

    def _parse_cell_input(self, cell: str) -> tuple[int, int] | str | None:
        """Parses the cell input as either A1 notation or (row, col) tuple."""
        if re.match(r"^[A-Za-z]+\d+$", cell):  # A1 notation
            return cell.upper()

        try:
            row, col = eval(cell)
            if isinstance(row, int) and isinstance(col, int):
                return (row, col)
        except:
            pass

        return None


async def setup(bot):
    await bot.add_cog(Bot(bot))
