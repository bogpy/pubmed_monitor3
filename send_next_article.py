import os, sys
import requests

from queue_operations import load_queue, save_queue

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = "@estetika_radar"

queue = load_queue()

if not queue:
    print("Очередь пуста")
    exit()

article = queue.pop(0)

score = article["score"]

summary = article["summary"]

summary = summary.replace("🧠 Главная мысль\n", "<b>", 1)
summary = summary.replace("\n\n🎯 Цель", "</b>\n\n🎯 Цель", 1)

message = f"""
{summary}

━━━━━━━━━━━━━━

🆔 <b>PMID:</b> <a href="{article["link"]}">{article["pmid"]}</a>
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
)

print(response.status_code)
print(response.text)

save_queue(queue)

print(f"Отправлена статья {article['pmid']}")
print(f"Осталось в очереди: {len(queue)}")