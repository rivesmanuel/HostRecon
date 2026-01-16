# HostRecon

A small Python tool to quickly check how your computer/server is doing (CPU, memory, disk, services, and ports).

## What it does
- Shows CPU, RAM, and disk usage with a simple OK/WARNING/CRITICAL status.
- Checks common services (Linux and Windows) and prints whether they are running.
- Checks if selected local ports on `127.0.0.1` are open or closed.
- Can run in two ways:
  - Interactive menu (you type what to check).
  - Automatic mode (`--auto`) for scheduled runs.

## Project files
- `hostrecon.py` — main script.
- `funtions.py` — system checks (CPU/RAM/disk/services/ports).
- `config.py` — default services and ports to check.
- `logs/` — log folder (created automatically).

## Requirements
- Python 3
- `psutil`

## Install:
```bash
pip install -r requierements.txt
```
## How to run

### Interactive mode:
```bash
python hostrecon.py
```
This shows basic system info and then a menu to check services or ports.

### Automatic mode (one run):
```bash
python hostrecon.py --auto
```
This runs the checks using the default services/ports from `config.py`

## Help & Version
```bash
python hostrecon.py --help
python hostrecon.py --version
```

## Automation (Run it Automatically)
You can set this script to run every 5 minutes (or any other interval) so you always have a history of your system's health.

### On linux (Using crontab)
#### 1. Open your terminal and type:
```bash
crontab -e
```

#### 2. Add the following line at the bottom of the file.
Replace `/path/to/your/project` with the actual folder location.
```bash
*/5 * * * * cd /path/to/your/project && /usr/bin/python3 hostrecon.py --auto >> logs/cron.log 2>&1
```
What this does:

- `*/5 * * * *`: Runs every 5 minutes.

- `cd ...`: Go to the project folder first.

- `python3 ...`: Runs the script in automatic mode.

### On Windows (using Task Scheduler)

#### 1. Press `Win + R`, type `taskschd.msc`, and press Enter.

#### 2. Click Create Basic Task on the right side.

#### 3. Name: "Health hostrecon".

#### 4. Trigger: Choose Daily.

- Set the start time.

- You can edit it later to repeat every 5 minutes (in the Properties > Triggers tab).

#### 5. Action: Choose Start a program.

- Program/script: Type `python.exe` (or the full path to your python executable).

- Add arguments: Type `hostrecon.py --auto`.

- Start in: Paste the full path to your project folder (e.g., `C:\Users\Name\HostRecon`).

#### 6. Click Finish

Tip: To make it run every 5 minutes, right-click your new task, go to Properties > Triggers, edit the trigger, and check "Repeat task every: 5 minutes".

## License.

MIT License
Copyright (c) 2026