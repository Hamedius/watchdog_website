# watchdog_website

A simple **website uptime monitor** built with **Python** and **GitHub Actions**.

This repository periodically checks a list of URLs and stores their status in a JSON file.  
It’s designed to be lightweight and easy to run completely from GitHub (no external server).

---

## Features

-  **Automatic checks via GitHub Actions**  
  A workflow in `.github/workflows/` runs `watchdog.py` on a schedule.

-  **Multiple websites**  
  The list of target URLs is stored in `status.json`.

-  **Status tracking**  
  For each website, the script updates:
  - HTTP status (up / down)  
  - Status code (e.g., 200, 404, 500)  
  - Last check timestamp  

-  **Static JSON output**  
  `status.json` can be used by another frontend or dashboard.

---

## Repository structure

```text
watchdog_website/
├─ README.md
├─ status.json
└─ watchdog.py
```

---

## How it works

### 1. Configuration
- `status.json` contains the list of websites to monitor.  
- Each entry includes at least `url`, and optionally `name`, `description`, etc.

### 2. Check run
- `watchdog.py` reads `status.json`.  
- For each URL:
  - Sends an HTTP request.  
  - Determines UP/DOWN state.  
  - Updates status, code, and last-checked time.

### 3. GitHub Actions
- Runs `watchdog.py` on a schedule (cron).  
- Commits updated `status.json` back into the repository automatically.

Your repo will always contain the latest status results.

---

## Getting started (local run)

### 1. Clone the repository
```bash
git clone https://github.com/Hamedius/watchdog_website.git
cd watchdog_website
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, simply create one containing:
```
requests
```

### 4. Configure `status.json`

Example format:

```json
[
  {
    "name": "Example",
    "url": "https://example.com",
    "status": "",
    "status_code": null,
    "last_check": null
  }
]
```

### 5. Run the script
```bash
python watchdog.py
```

After running, `status.json` will be updated.

---

## GitHub Actions setup

The workflow in `.github/workflows/`:

- Uses a Python runner (e.g., `ubuntu-latest`)  
- Installs dependencies  
- Runs `python watchdog.py`  
- Commits the updated `status.json` back to the repo  

To change frequency, modify the cron expression:

```yaml
on:
  schedule:
    - cron: "*/30 * * * *"   # every 30 minutes
```

---

## Possible improvements

- Add Telegram / Slack / email notifications  
- Track history instead of only the latest check  
- Create a frontend dashboard to visualize uptime  
- Export metrics to monitoring services  

---

## Author

**Hamed Nahvi**  
GitHub: @Hamedius
