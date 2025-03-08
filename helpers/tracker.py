import gspread, re
from google.oauth2.service_account import Credentials
# https://docs.gspread.org/en/v6.0.0/user-guide.html#updating-cells

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file(
    "creds.json", scopes=scopes
)
client = gspread.authorize(creds)
# Everything after /d, before /edit
sheet_id = "1KhbXANYNqZuG-a3l17uFtYFkj7JlGGVhv6GJpHfQ3MM"
sheet = client.open_by_key(sheet_id)


class Tracker():
    # Defaults first sheet
    def __init__(self, worksheet_no: int = 0):
        self.worksheet = sheet.get_worksheet(worksheet_no)

    def update_cell(self, coords: tuple[int, int], value: str) -> str:
        """Updates the cell with the value of a (row, col) coordinate

        Args:
            coords (tuple[int, int]):   A tuple of ints specifying the row
                                        and col of the cell.
            value (str):                The desired value of the cell.
                                        This will turn uppercase in the sheet.

        Raises:
            ValueError: If coords are not a tuple of two integers.
            ValueError: If value does not contain a letter followed by a number.
            ValueError: If value is empty.
        """

        # Validate coords
        if not (isinstance(coords, tuple) and len(coords) == 2 and 
                all(isinstance(i, int) for i in coords)):
            raise ValueError("coords must be a tuple of two integers (row, col).")

        # Validate value
        if not isinstance(value, str) or not value:
            raise ValueError("value must be a non-empty string.")

        if not re.match(r"^[A-Za-z]+\d+$", value):
            raise ValueError("value must contain a letter followed by a number (e.g., 'D1').")

        # Convert value to uppercase
        self.worksheet.update_cell(coords[0], coords[1], value.upper())

        return f"Updated cell {coords} with {value.upper()}"


    def rem(self):
        pass
