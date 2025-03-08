import gspread, re
from google.oauth2.service_account import Credentials

# Authentication
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("creds.json", scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "1KhbXANYNqZuG-a3l17uFtYFkj7JlGGVhv6GJpHfQ3MM"
sheet = client.open_by_key(sheet_id)

class Tracker():
    def __init__(self, worksheet_no: int = 0): # This defaults to the first worksheet
        self.worksheet = sheet.get_worksheet(worksheet_no)

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

    def _col_number_to_letter(self, col: int) -> str:
        """Converts a column number (1-based) to a letter (A, B, C, etc.)."""
        letter = ""
        while col:
            col, remainder = divmod(col - 1, 26)
            letter = chr(65 + remainder) + letter
        return letter


    def rem(self):
        pass
