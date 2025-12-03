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

## Repository structure

```text
watchdog_website/
├─ .github/
│  └─ workflows/
│      └─ <workflow_file>.yml    # CI workflow that runs watchdog.py on a schedule
├─ status.json                    # List of websites and their latest status
├─ watchdog.py                    # Main Python script for checking websites
└─ README.md

Note: Adjust file names above if they are slightly different in your repo.

⸻

How it works

1. Configuration
	•	status.json contains the list of websites you want to monitor and (optionally) existing status data.
	•	Each entry typically includes at least a url field. You can add more fields as needed (name, description, etc.).

2. Check run
	•	watchdog.py reads status.json.
	•	For each URL:
	•	Sends an HTTP request.
	•	Determines if it is up or down based on the response.
	•	Updates the JSON data (status, status code, last checked time).

3. GitHub Actions
	•	The workflow in .github/workflows/ runs watchdog.py on a schedule (using cron).
	•	After each run, the updated status.json is committed back to the repository.

This means your repo always contains the latest status of each website.

⸻

Getting started (local run)

1. Clone the repository

git clone https://github.com/Hamedius/watchdog_website.git
cd watchdog_website

2. Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

If you don’t have a requirements.txt yet, create one containing at least:

requests



4. Configure status.json

Edit status.json and add your own websites. Example structure:

[
  {
    "name": "Example",
    "url": "https://example.com",
    "status": "",
    "status_code": null,
    "last_check": null
  }
]

Adjust the fields to match what watchdog.py expects.

5. Run the script

python watchdog.py

After running, status.json should be updated with the latest status information.

⸻

GitHub Actions setup

The workflow file in .github/workflows/:
	•	Uses a Python runner (e.g. ubuntu-latest).
	•	Installs dependencies (pip install -r requirements.txt).
	•	Runs python watchdog.py.
	•	Commits and pushes the updated status.json back to the repository.

If you want to change how often checks run, modify the cron expression:

on:
  schedule:
    - cron: "*/30 * * * *"   # every 30 minutes, example


⸻

Possible improvements
	•	Add notification integration (e.g. email, Telegram, Slack webhook) when a site goes down.
	•	Expose status.json to a static frontend to visualize uptime history.
	•	Store a history of checks instead of only the latest status.
	•	Export metrics to a time-series database or a monitoring service.

⸻

Author

Hamed Nahvi
GitHub: @Hamedius
