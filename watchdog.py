import requests
import smtplib
import os
import json
import traceback
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz
import sys

# ===== پیکربندی =====
websites = [
    "https://www.artancompany.ir",
    "https://www.elintfh.com",
    "https://www.google.com"
]
STATUS_FILE = "status.json"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def is_blank_page(html):
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body
    if not body:
        return True
    for tag in body(["script", "style", "noscript"]):
        tag.decompose()
    text = body.get_text(strip=True)
    return len(text) < 20

def send_telegram(msg):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⛔ تلگرام تنظیم نشده")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        r = requests.post(url, data=data)
        print(f"Telegram: {r.status_code}, {r.text}")
    except Exception as e:
        print("Telegram error:", e)

def send_email(subject, body):
    if not EMAIL_FROM or not EMAIL_TO or not EMAIL_PASS:
        print("⛔ ایمیل تنظیم نشده")
        return
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASS)
            server.send_message(msg)
        print("📧 ایمیل ارسال شد")
    except Exception as e:
        print("Email error:", e)

def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_status(st):
    with open(STATUS_FILE, "w") as f:
        json.dump(st, f, indent=2)

def check_websites(mode="change-only"):
    old = load_status()
    new = {}
    changes = []

    for site in websites:
        try:
            r = requests.get(site, timeout=10)
            status = "UP" if r.status_code == 200 and not is_blank_page(r.text) else "BLANK"
        except Exception as e:
            print("❌", site, "error:", e)
            traceback.print_exc()
            status = "DOWN"
        new[site] = status
        if old.get(site) != status:
            changes.append((site, old.get(site, "UNKNOWN"), status))

    save_status(new)
    tztime = datetime.now(pytz.timezone("Europe/Rome")).strftime("%Y-%m-%d %H:%M:%S")

    if mode == "change-only":
        for site, o, n in changes:
            msg = f"⚠️ تغییر وضعیت: {site}\n{o} → {n}"
            send_telegram(msg)
            send_email(f"Website status change: {site}", msg)

    elif mode == "daily-report":
        if changes:
            msg = "\n".join([f"{s}: {o} → {n}" for s, o, n in changes])
        else:
            msg = "همه سایت‌ها سالم هستند ✅"
        full = f"🕓 گزارش {tztime}\n{msg}"
        send_telegram(full)
        send_email("Daily website report", full)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "change-only"
    check_websites(mode)
