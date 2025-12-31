# Shiori Bot

**Shiori Bot** is a personal Discord bot project built using **Python** and the **Google Sheets API**. The main goal was to experiment with Google Sheets integration and automate tracking tasks via Discord.

> ⚠️ **Note:** This project is not meant to be reused or deployed by others, as it relies on private Google Sheets credentials that only I have access to.

## 🎯 Features

> 📝 These features and terms are specific to the game **Princess Connect Re:Dive**.

- **Overtime Hit Calculation** – Automatically processes and logs OT hits  
- **Player Hit Tracking** – Tracks player activity

## 🛠 Setup & Usage

For future me: If you ever need to get this running again, follow these steps.

```bash
# 1. Clone the repository
git clone https://github.com/naixsu/Shiori-Bot.git
cd Shiori-Bot

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Run the bot (with watcher tracking - recommended)
python run.py

# Optional: Run without watcher tracking (not recommended)
python main.py
```

## 🐳 Docker

This repo expects:
- `creds.json` in the project root (Google service account credentials)
- `.env` containing at least:
  - `DISCORD_TOKEN`
  - `SHEET_ID`
  - `APPLICATION_ID`, `GUILD_ID`

### Run (recommended)

```bash
docker compose up --build -d
docker compose logs -f
```

### Run with auto-reload (dev)

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

## 📁 Notes

- Your **Google Sheets credentials** must be available in the correct location for this bot to function. Just have it in the root directory and call it `creds.json`.
- `run.py` includes a file watcher that automatically reloads the bot when changes are detected—handy for active development.
- `main.py` simply starts the bot without any reloading or watching.

## 🧪 Personal Use Only

This repo serves as a reference for myself. If you're here out of curiosity, feel free to explore the code—but it won't run without my private credentials.
