# ポケカ シティリーグ通知Bot

関東（東京・神奈川・千葉・埼玉）の **ポケモンカード シティリーグ（募集中）** をチェックして、  
新しいイベントが公開されたら **Discordに自動通知** してくれるBotです。  

通知例：
🆕 新規シティリーグ
イベント名
ショップ名
開催日
https://players.pokemon-card.com/event/xxxxx


---

## 🚀 使い方（友だち向け）

### 1. Discordサーバーに参加
管理者が用意したDiscordサーバーに入るだけでOKです。  

### 2. 通知を受け取る
新しいシティリーグイベントが公開されると、自動で通知されます。  
操作は不要です。

---

## ⚙️ 仕組み（技術メモ）

- GitHub Actions が 15分ごとに `check.py` を実行  
- 新規イベントのみ Discord にWebhook通知  
- 初回実行時は「既存イベントを記録するだけ」で通知なし  

---

## 📦 セットアップ（管理者向け）

1. リポジトリをForkまたはClone  
2. DiscordでWebhook URLを取得してGitHub Secretsに登録  
   - Name: `DISCORD_WEBHOOK_URL`  
   - Value: 発行したWebhook URL  
3. GitHub Actionsを有効化すると自動通知が始まります ✅  

---

## 💡 注意点

- GitHub Actions無料枠（2000分/月）で十分動作  
- このBotは**非公式**です（ポケモンカード公式とは無関係）  
- 県やイベント形式の変更は `check.py` のURLパラメータを編集してください  

---

## 📝 ライセンス

MIT License
