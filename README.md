# Pomodoro App — Focus Dashboard

A desktop focus app built with Python and Tkinter. It combines a Pomodoro-style
focus timer with distraction detection, ambient background music, session
statistics, and a simple gamification system.

The app is designed for Windows: when a focus session starts it launches a
background watcher (`backend.pyw`) that monitors the active window and logs
distracting apps and websites while the timer runs.

## Features

- **Focus timer** — configurable session length (10–180 minutes), live
  countdown, progress bar, and motivational quotes.
- **Distraction logging** — the background watcher writes detections (window
  title + timestamp) to `distractionHistory.json`; the built-in viewer shows the
  full history, a total count, and the most frequent distraction.
- **Daily summary** — total focused minutes and distractions for today, shown on
  the timer screen.
- **XP and levels** — earn XP for focused time (1 XP per 6 minutes), level up
  every 100 XP, and view progress and achievements in the gamification panel.
- **Ambient music player** — five bundled ambient tracks with play/pause, stop,
  previous/next, volume control, and animated bars.
- **Modern UI** — card-based layout with a Windows 11-inspired light theme.

## Project structure

```
pomodoro-app/
├── main.py                      # Tkinter GUI and app entry point
├── backend.pyw                  # Background distraction watcher (started per session)
├── userData.json                # Session length + whether the watcher is active
├── userSessions.json            # Completed session durations and timestamps
├── userXP.json                  # Accumulated XP
├── distractionHistory.json      # Detected distractions
├── assets/music/                # Ambient 1-5.mp3
└── Updated_Project_Report.md    # Detailed project report
```

The JSON data files are created automatically with default values the first time
the app starts.

## Requirements

- Python 3.10+
- Tkinter (included with standard Windows Python installs)
- [pygame](https://www.pygame.org/) for music playback
- The distraction watcher additionally needs the packages it monitors windows
  with (for example `pywinauto` and `pywin32`)

Install the Python dependency:

```bash
pip install pygame
```

## Running the app

From the project root:

```bash
python main.py
```

The dashboard opens with four actions:

1. **View Distraction History** — browse logged distractions and the summary.
2. **Customize Settings** — change the session length or export the bundled music
   files to another folder.
3. **Gamification & Rewards** — see current level, XP progress, and achievements.
4. **Open Timer Screen** — start a focus session.

Starting a session begins the countdown and launches `backend.pyw` in a
subprocess, setting `backendActive` to `true` in `userData.json`. Stopping the
session, finishing it, or closing the timer sets `backendActive` back to `false`
and records the session and XP.

> **Note:** `backend.pyw` is referenced by `main.py` but is not included in this
> repository. Without it the timer, music, stats, and XP still work, but no new
> distractions will be detected.

## Data files

| File | Contents |
| --- | --- |
| `userData.json` | `Session Time` (minutes) and `backendActive` flag |
| `userSessions.json` | `Sessions`: list of `[duration_minutes, "dd/mm/yy HH:MM:SS"]` |
| `userXP.json` | `XP`: total experience points |
| `distractionHistory.json` | `Distractions`: list of `[window_title, timestamp]` |

## How it fits together

```
main.py (Tkinter UI)
   │  start session
   ├──► userData.json  (backendActive = true)
   ├──► backend.pyw    (monitors active window)
   │        └──► distractionHistory.json
   ├──► timer tick     (countdown, progress, quotes)
   └──► stop/finish
            ├──► userSessions.json  (duration + timestamp)
            ├──► userXP.json        (duration / 6)
            └──► userData.json      (backendActive = false)
```

See `Updated_Project_Report.md` for a full write-up of the design and features.
