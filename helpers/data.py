# Change this every cb
import pytz
from datetime import datetime, timedelta

# Player data
PLAYERS = {
    "Aidown": "C6:Q6",
    "Cierra": "C8:Q8",
    "cnet128": "C10:Q10",
    "Daniel": "C12:Q12",
    "FoxKou": "C14:Q14",
    "Frost": "C16:Q16",
    "Grenouille": "C18:Q18",
    "Kaichou (alt)": "C20:Q20",
    "Kaichou (main)": "C22:Q22",
    "Kinkin": "C24:Q24",
    "Lolly": "C26:Q26",
    "Maokuss": "C28:Q28",
    "Melody": "C30:Q30",
    "naixsu": "C32:Q32",
    "Puchikii (ぷちきい)": "C34:Q34",
    "Quietus": "C36:Q36",
    "RdvL": "C38:Q38",
    "Rein (レイン)": "C40:Q40",
    "Rinku": "C42:Q42",
    "SaielaM": "C44:Q44",
    "Slifer1993": "C46:Q46",
    "Sora (ソラ)": "C48:Q48",
    "ThotSimp": "C50:Q50",
    "Toycon": "C52:Q52",
    "UF": "C54:Q54",
    "UMI": "C56:Q56",
    "xFuRiiOs": "C58:Q58",
    "Xyrus": "C60:Q60",
    "Yusha": "C62:Q62",
    "Yuuki": "C64:Q64",
}

# CB date
TIME_ZONE_JST = pytz.timezone("Asia/Tokyo")
CB_START_DATE = datetime(
    year=2025,
    month=3,
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
