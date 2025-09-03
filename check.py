import requests
import os
import json

URL = "https://players.pokemon-card.com/event_search?prefecture[]=12&prefecture[]=14&prefecture[]=13&prefecture[]=11&event_type[]=3:2&league_type[]=1&offset=0&accepting=true&order=1"
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
SAVE_FILE = "known_ids.json"

def send_discord(msg: str):
    if not DISCORD_WEBHOOK_URL:
        print("DISCORD_WEBHOOK_URL が設定されていません。")
        return
    data = {"content": msg}
    r = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if r.status_code != 204:
        print("Discord送信エラー:", r.status_code, r.text)

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

def check_update():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Accept": "application/json"
    }
    res = requests.get(URL, headers=headers)

    if not res.text.strip():
        print("⚠️ 空のレスポンス（イベント未公開かもしれません）")
        return

    try:
        data = res.json()
    except ValueError:
        print("⚠️ JSONではないレスポンス:", res.text[:200])
        return

    known_ids = load_known_ids()
    current_ids = {str(ev["id"]) for ev in data.get("event", [])}

    # 差分（今回新しく出たイベント）
    new_ids = current_ids - known_ids

    for ev in data.get("event", []):
        ev_id = str(ev["id"])
        if ev_id in new_ids:
            ev_name = ev["event_title"]
            ev_shop = ev["shop_name"]
            ev_date = ev["event_date"]
            ev_url = f"https://players.pokemon-card.com/event/{ev_id}"
            msg = f"🆕 新規シティリーグ\n{ev_name}\n{ev_shop}\n{ev_date}\n{ev_url}"
            send_discord(msg)

    # 既知イベント一覧を更新
    if new_ids:
        save_known_ids(known_ids | current_ids)

if __name__ == "__main__":
    check_update()
