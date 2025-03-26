import gspread, re
import helpers.data as data

from google.oauth2.service_account import Credentials
from datetime import datetime, timezone, timedelta
from typing import Union

# https://docs.gspread.org/en/v6.0.0/user-guide.html#updating-cells

# Authentication
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("creds.json", scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "1KhbXANYNqZuG-a3l17uFtYFkj7JlGGVhv6GJpHfQ3MM"
sheet = client.open_by_key(sheet_id)

class Tracker():
    def __init__(self, worksheet_no: int = 0): # This defaults to the first worksheet
        self.worksheet = sheet.get_worksheet(worksheet_no)
        self.cache = {}
        self.last_check = None # "Player-Boss-Date-Time"


    def _col_number_to_letter(self, col: int) -> str:
        """Converts a column number (1-based) to a letter (A, B, C, etc.)."""
        letter = ""
        while col:
            col, remainder = divmod(col - 1, 26)
            letter = chr(65 + remainder) + letter
        return letter


    def update_cell(self, cell: tuple[int, int] | str, value: str) -> str:
        """Updates a cell using either A1 notation ('C3') or (row, col) tuple."""

        # Validate value
        if not isinstance(value, str) or not value:
            raise ValueError("Value must be a non-empty string.")

        # Determine cell format
        if isinstance(cell, str):  # A1 notation
            self.worksheet.update(cell, value)
        elif isinstance(cell, tuple) and len(cell) == 2:
            row, col = cell
            self.worksheet.update_cell(row, col, value.upper())
            cell = f"{self._col_number_to_letter(col)}{row}"
        else:
            raise ValueError("Cell must be A1 notation (e.g., 'C3') or a (row, col) tuple.")

        return f"Updated cell {cell} with '{value.upper()}'"


    def get_ot(self, boss_hp: float, first_hit: float, second_hit: float) -> str:
        """Calculates the Overkill Time (OT) based on given boss HP and damage values."""

        # Validate input
        if boss_hp <= 0:
            return "Boss HP must be a positive number."
        if first_hit is not None and first_hit <= 0:
            return "First hit must be a positive number."
        if second_hit is not None and second_hit <= 0:
            return "Second hit must be a positive number."

        total_damage = first_hit + second_hit
        overkill = total_damage - boss_hp

        if overkill <= 0:
            return "There is no overkill. No carry-over time gained."

        ot_first_hit = 90 * (overkill / first_hit) + 20
        ot_second_hit = 90 * (overkill / second_hit) + 20

        return (
            f"**Carry-over times:**\n"
            f"If **First Hit** takes OT: **{ot_first_hit:.2f}s**\n"
            f"If **Second Hit** takes OT: **{ot_second_hit:.2f}s**"
        )


    def _get_last_check(self) -> str:
        values_list = self.worksheet.get_values("V26:X32")
        player = values_list[0].pop()
        boss = values_list[2].pop()
        date = values_list[4].pop() # %Y/%m/%d
        time = values_list[6].pop() # %H:%M

        last_check = f"{player.upper()}-{boss.upper()}-{date}-{time}"

        return last_check


    def _get_current_day(self) -> int:
        # TODO: clean this up when it's ok lol
        # # Debug
        # now_utc = now_utc.replace(
        #     day=25, hour=4, minute=1, second=0
        # )
        now_utc = datetime.now()
        print("now_utc", now_utc)
        now_jst = now_utc.astimezone(data.TIME_ZONE_JST)
        print("now_jst", now_jst)
        time_difference = now_jst - data.CB_START_DATE
        print("time_difference", time_difference)
        days_elapsed, _ = divmod(time_difference.total_seconds(), 86400)  # 86400 seconds in a day
        print("days_elapsed", days_elapsed)
        # if now_jst.hour < data.CB_START_DATE.hour: # 05:00 JST reset
        #     current_day = int(days_elapsed)
        # else:
        #     current_day = int(days_elapsed) + 1

        current_day = int(days_elapsed)

        return current_day


    def _process_hits(self) -> None:
        current_day = self._get_current_day()

        if current_day == 0:
            current_day += 1

        print(f"==> Processing player hits {datetime.now(timezone.utc)} for day {current_day}")

        for player, range in data.PLAYERS.items():
            row_player_hits = self.worksheet.get_values(range)
            start = (current_day - 1) * 3
            day_player_hits = row_player_hits[start:start + 3]
            print(f"=> Processing {player}\nStart: {start} | {row_player_hits}")

            if not len(day_player_hits):
                self.cache[player] = 3
            else:
                self.cache[player] = 3 - len(day_player_hits[0])

        print("==> Done processing")


    def rem(self) -> Union[dict, str]:
        if self._get_current_day() < 0:
            return "CB hasn't started yet"

        last_check = self._get_last_check()

        print(f"self.last_check: {self.last_check} | last_check: {last_check}")

        if last_check != self.last_check:
            self.last_check = last_check
            self._process_hits()

        return self.cache
