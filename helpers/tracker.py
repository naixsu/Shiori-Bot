import gspread, os
import helpers.data as data

from google.oauth2.service_account import Credentials
from datetime import datetime, timezone, timedelta
from typing import Union

# https://docs.gspread.org/en/v6.0.0/user-guide.html#updating-cells

# Authentication
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("creds.json", scopes=scopes)
client = gspread.authorize(creds)
sheet_id = os.getenv("SHEET_ID", 0)
sheet = client.open_by_key(sheet_id)

class Tracker():
    def __init__(self, worksheet_no: int = 0): # This defaults to the first worksheet
        self.worksheet = sheet.get_worksheet(worksheet_no)
        self.cache = {}
        self.last_check = None # "Player-Boss-Date-Time"

        # Initialize dates
        self.start_date, self.end_date = self._process_dates()


    def _reset_worksheet_no(self):
        self.worksheet = sheet.get_worksheet(0)
        print("Worksheet has been reset")


    def _process_dates(self) -> tuple[datetime, datetime]:
        # Reset this just in case
        self._reset_worksheet_no()

        start_date_str = self.worksheet.get_values(data.CB_START_DATE)[0][0]

        start_date_obj = datetime.strptime(start_date_str, "%m/%d/%Y")
        start_date = datetime(
            year=start_date_obj.year,
            month=start_date_obj.month,
            day=start_date_obj.day,
            hour=5,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=data.TIME_ZONE_JST
        )

        end_date = start_date + timedelta(
            days=4,
            hours=18,
            minutes=59,
            seconds=59,
        )

        print(f"_process_dates() ==> {start_date} | {end_date}")
        return start_date, end_date


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


    def get_current_day(self) -> int:
        # TODO: clean this up when it's ok lol
        # # Debug
        now_utc = datetime.now()
        # now_utc = now_utc.replace(
        #     day=25, hour=4, minute=1, second=0
        # )
        now_jst = now_utc.astimezone(data.TIME_ZONE_JST)
        time_difference = now_jst - self.start_date
        days_elapsed, seconds = divmod(time_difference.total_seconds(), 86400)  # 86400 seconds in a day
        current_day = int(days_elapsed)

        if seconds > 0:
            current_day += 1

        print(f"get_current_day() ==> {now_utc} | {now_jst} | {time_difference} | {days_elapsed} | {current_day}")

        return current_day


    def _get_remaining_hits(self, lst):
        return 3 - sum(1 for item in lst if item.strip())


    def _get_remaining_ots(self, lst):
        return sum(1 for item in lst if item.lower() == "ot")


    def _process_hits(self) -> None:
        current_day = self.get_current_day()

        if current_day == 0:
            current_day += 1

        print(f"==> Processing player hits {datetime.now(timezone.utc)} for day {current_day}")
        hit_range = data.HIT_DATA[current_day]
        hit_data = self.worksheet.get_values(hit_range)
        players_list = self.worksheet.get_values(data.PLAYERS_RANGE)

        # Rebuild cache from the current sheet state so replaced/removed players
        # don't linger in memory across refreshes.
        old_cache = self.cache
        new_cache: dict[str, dict[str, int]] = {}

        for i in range(0, len(players_list), 2):
            player = (players_list[i][0] if players_list[i] else "").strip()
            if not player:
                # Player cell is blank; skip so we don't create cache entries for non-players.
                print(f"Skipping blank player row index={i} (sheet row offset={6 + i})")
                continue
            try:
                hits, ots = hit_data[i], hit_data[i+1]
            except IndexError:
                hits, ots = [], []
                print(
                    f"Hit data missing for player={player} at index={i} (range={hit_range}); "
                    f"defaulting hits/ots to empty"
                )

            rem_hits = self._get_remaining_hits(hits)
            rem_ots = self._get_remaining_ots(ots)

            print(f"=> Processing {player}\nHits: {hits} | OTs {ots}")

            new_cache[player] = {
                "Hits": rem_hits,
                "OTs": rem_ots,
            }

        # Swap cache atomically after processing so consumers never see partial state.
        self.cache = new_cache

        removed_players = set(old_cache.keys()) - set(new_cache.keys())
        added_players = set(new_cache.keys()) - set(old_cache.keys())

        if removed_players:
            print(f"Removed {len(removed_players)} stale player(s) from cache: {sorted(removed_players)}")
        if added_players:
            print(f"Added {len(added_players)} new player(s) to cache: {sorted(added_players)}")

        print(f"Cache refresh complete: {len(new_cache)} player(s)")
        print("==> Done processing\n")


    def rem(self) -> tuple[Union[dict, str], str | None]:
        # Process dates again just in case something weird happens
        self.start_date, self.end_date = self._process_dates()

        print(f"/rem used => {self.start_date}, {self.end_date}")
        print(f"/rem used; start_date={self.start_date} end_date={self.end_date}")

        # Compute once to avoid inconsistent results across calls
        day = self.get_current_day()

        # Treat day 0 as Day 1 (CB has started)
        if day == 0:
            day = 1

        if day < 0:
            # CB not started; reset state so we don't serve stale data.
            self.cache = {}
            self.last_check = None
            print("CB hasn't started yet; cleared cache and last_check")
            return "CB hasn't started yet", None
        elif day > 5:
            # CB ended; reset state so we don't serve stale data.
            self.cache = {}
            self.last_check = None
            print("CB has already ended; cleared cache and last_check")
            return "CB has already ended", None

        last_check = self._get_last_check()

        print(f"self.last_check: {self.last_check} | last_check: {last_check}")

        if last_check != self.last_check:
            self.last_check = last_check

            print(f"last_check changed; refreshing hits cache (last_check={last_check})")

            self._process_hits()

        return self.cache, last_check
