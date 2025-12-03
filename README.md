# watchdog_website

A simple **website uptime monitor** built with **Python** and **GitHub Actions**.

This repository periodically checks a list of URLs and stores their status in a JSON file.  
It’s designed to be lightweight and easy to run completely from GitHub (no external server).

---

## Features

- 🔁 **Automatic checks via GitHub Actions**  
  A workflow in `.github/workflows/` runs `watchdog.py` on a schedule (e.g. every few minutes / hours).

- 🌐 **Multiple websites**  
  A list of target URLs is stored in `status.json`. The script loops through them and sends HTTP requests.

- ✅ **Status tracking**  
  For each website, the script updates fields like:
  - HTTP status (up / down)
  - Status code (e.g. 200, 404, 500)
  - Last check timestamp

- 📄 **Static JSON output**  
  The `status.json` file can be used by a separate frontend (static site) to show a simple status dashboard.

---

## Project structure

```text
watchdog_website/
├─ README.md
├─ status.json
└─ watchdog.py
```

---

## How it works

1. `status.json` contains the list of websites you want to monitor.  
2. `watchdog.py` loads this list and sends HTTP requests.  
3. For each URL, it updates status, HTTP code and last-check time.  
4. When run in GitHub Actions, the updated `status.json` is committed back to the repository.

---

## Getting started (local)

```bash
git clone https://github.com/Hamedius/watchdog_website.git
cd watchdog_website
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python watchdog.py
```

---

## Author

**Hamed Nahvi**  
GitHub: [@Hamedius](https://github.com/Hamedius)
