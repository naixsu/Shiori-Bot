import re

from discord import Interaction, Embed, Color
from discord.ext import commands
from discord import app_commands
from discord.app_commands import checks

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
    # TODO: change this `tested` role to `Cult Quintet` in Hoshizuku
    @checks.has_role("tested")
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

    # Error Handler for Missing Role
    @update_cell.error
    async def update_cell_error(self, interaction: Interaction, error):
        if isinstance(error, app_commands.errors.MissingRole):
            await interaction.response.send_message(
                "You need the **Cult Quintet** role to use this command!", ephemeral=True
            )


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


    @app_commands.command(name="rem", description="Displays remaining hits for the current day.")
    async def rem(self, interaction: Interaction):
        await interaction.response.defer()
        remaining_hits = self.tracker.rem()

        # CB hasn't started yet
        if isinstance(remaining_hits, str):
            await interaction.followup.send(remaining_hits, ephemeral=True)
            return

        # Create an embed for better formatting
        embed = Embed(
            title="Remaining Hits for Today",
            color=Color.green()
        )

        # Sort players by remaining hits
        sorted_hits = sorted(remaining_hits.items(), key=lambda x: x[1], reverse=True)

        # Format player data into columns
        hit_lines = []
        for player, hits in sorted_hits:
            if hits == 0: # Ignore no remaining hits
                continue

            hit_word = "hit" if hits == 1 else "hits"
            hit_lines.append(f"**{player}**: `{hits}` {hit_word} left")

        # Add formatted player data to embed
        embed.description = "\n".join(hit_lines) if hit_lines else "No players found."

        # Send the embed
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Bot(bot))
