import requests
import os
import json

URL = "https://players.pokemon-card.com/event/search?prefecture=12&prefecture=14&prefecture=13&prefecture=11&event_type=3:2&offset=0&accepting=true&order=1"
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
SAVE_FILE = "known_ids.json"

def send_discord(msg: str):
    data = {"content": msg}
    r = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if r.status_code != 204:
        print("Discord送信エラー:", r.text)

def load_known_ids():
    if not os.path.exists(SAVE_FILE):
        return set()
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        try:
            return set(json.load(f))
        except json.JSONDecodeError:
            return set()

def save_known_ids(ids):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(ids), f, ensure_ascii=False)

def check_update(first_run=False):
    res = requests.get(URL)
    res.raise_for_status()
    data = res.json()
    known_ids = load_known_ids()
    new_ids = set()
    for ev in data.get("events", []):
        ev_id = str(ev["id"])
        if ev_id not in known_ids:
            if not first_run:
                ev_name = ev["title"]
                ev_shop = ev["shop_name"]
                ev_date = ev["date"]
                ev_url = f"https://players.pokemon-card.com/event/{ev_id}"
                msg = f"🆕 新規シティリーグ\n{ev_name}\n{ev_shop}\n{ev_date}\n{ev_url}"
                send_discord(msg)
            new_ids.add(ev_id)
    if new_ids:
        save_known_ids(known_ids | new_ids)

if __name__ == "__main__":
    first_run = not os.path.exists(SAVE_FILE)
    check_update(first_run=first_run)
