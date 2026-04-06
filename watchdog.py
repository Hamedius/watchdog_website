import requests
import smtplib
import os
import json
import traceback
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === Configuration ===
websites = [
    "https://www.artancompany.ir",
    "https://www.elintfh.com",
    "https://www.google.com",
    "https://web.bale.ai",
    "https://web.splus.ir",
    "https://web.rubika.ir"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WebsiteWatchdog/1.0)"
}

STATUS_FILE = "status.json"

# Telegram & Email
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def is_page_visibly_blank(html):
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body
    if not body:
        return True
    for tag in body(["script", "style", "noscript"]):
        tag.decompose()
    visible_text = body.get_text(strip=True)
    return len(visible_text) < 20

def fetch_status(url):
    try:
        r = requests.head(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return "UP"
    except Exception:
        pass
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return "BLANK" if is_page_visibly_blank(r.text) else "UP"
        return f"DOWN-{r.status_code}"
    except requests.exceptions.SSLError:
        return "SSL_ERROR"
    except Exception:
        return "ERROR"

def send_telegram(message):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        chat_ids = [c.strip() for c in TELEGRAM_CHAT_ID.split(",")]

        for chat_id in chat_ids:
            data = {"chat_id": chat_id, "text": message}
            try:
                requests.post(url, data=data)
            except Exception as e:
                print(f"Telegram error: {e}")
                
def send_email(subject, body):
    if EMAIL_FROM and EMAIL_TO and EMAIL_PASS:
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_FROM
            recipients = [e.strip() for e in EMAIL_TO.split(",")]
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()
                smtp.login(EMAIL_FROM, EMAIL_PASS)
                smtp.sendmail(EMAIL_FROM, recipients, msg.as_string())
        except Exception as e:
            print(f"Email error: {e}")

def load_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_status(statuses):
    with open(STATUS_FILE, "w") as f:
        json.dump(statuses, f, indent=2)

def is_time_to_report():
    now = datetime.now(pytz.timezone("Europe/Rome"))
    return now.hour in [7, 19] and now.minute == 0

def check_websites():
    old_status = load_status()
    new_status = {}
    changed = False

    for site in websites:
        status = fetch_status(site)
        new_status[site] = status
        old = old_status.get(site)

        if old != status:
            msg = f"{site} ⚠️ STATUS CHANGED: {old or 'UNKNOWN'} → {status}"
            print(msg)
            send_telegram(msg)
            send_email("Website Status Changed", msg)
            changed = True
        else:
            print(f"{site} ✅ No Change: {status}")

    save_status(new_status)

    if is_time_to_report():
        now = datetime.now(pytz.timezone("Europe/Rome")).strftime("%Y-%m-%d %H:%M:%S")
        statuses = [f"{site}: {new_status[site]}" for site in websites]
        msg = f"🕓 {now} – Daily Report:\n" + "\n".join(statuses)
        send_telegram(msg)
        send_email("Daily Website Status", msg)

if __name__ == "__main__":
    check_websites()
