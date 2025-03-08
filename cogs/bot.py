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


    # TODO: figure out the math of RoboNinon's `!of`
    # !of <BossHP> - Calculates damage needed to get full carry-over assuming both hits do the same amount of damage
    # !of <BossHP> <FirstHit> - Calculates the damage needed for the second hit to get full carry-over
    # !of <BossHP> <FirstHit> <SecondHit> - Calculates the carry-over the second hit will get with the given damage
    # !of <BossHP> <FirstHit> <SecondHit> <Duration>s - Calculates carry-over for battles that kill the boss before the 90 seconds end. Duration is the time it took to kill the boss during the second hit. The duration parameter must end in "s"!
    @app_commands.command(name="get_ot", description="Calculates the Overkill Time (OT)")
    @app_commands.describe(
        boss_hp="Boss HP in millions (e.g., 400)",
        first_hit="First hit's damage in millions (optional, e.g., 200)",
        second_hit="Second hit's damage in millions (optional, e.g., 180)"
    )
    async def get_ot(
        self, interaction: Interaction,
        boss_hp: float, first_hit: float, second_hit: float
    ):
        """Calls the get_ot function from Tracker and sends the result."""
        response = self.tracker.get_ot(boss_hp, first_hit, second_hit)
        await interaction.response.send_message(response)


async def setup(bot):
    await bot.add_cog(Bot(bot))
