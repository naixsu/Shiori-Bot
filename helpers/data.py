# Change this every cb
import pytz
from datetime import datetime, timedelta

# Player data
PLAYERS_RANGE = "B6:B64"

# Hit data depending on CB day
HIT_DATA = {
    1: "C6:E65",
    2: "F6:H65",
    3: "I6:K65",
    4: "L6:N65",
    5: "O6:Q65",
}

EMOJIS = {
    "ShioriTotemoKawaii": "<a:ShioriTotemoKawaii:923837838901018665>",
}

# CB date
# TODO: turn this auto; get data from sheet or something
TIME_ZONE_JST = pytz.timezone("Asia/Tokyo")
CB_START_DATE = datetime(
    year=2025,
    month=4,
    day=25,
    hour=5,
    minute=0,
    second=0,
    microsecond=0,
    tzinfo=TIME_ZONE_JST
)

CB_END_DATE = CB_START_DATE + timedelta(
    days=4,
    hours=18,
    minutes=59,
    seconds=59,
)
