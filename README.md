<div align="center">

```
██████   ██████  ██████  ████████  █████  ██
██   ██ ██    ██ ██   ██    ██    ██   ██ ██
██████  ██    ██ ██████     ██    ███████ ██
██      ██    ██ ██   ██    ██    ██   ██ ██
██       ██████  ██   ██    ██    ██   ██ ███████
```

**// BOOKMARKS — terminal link vault**

A cyberpunk-style minimalist bookmark management website built with Flask and SQLite, featuring button-driven reordering, multi-column layout, light/dark theme switching, keyboard shortcuts, and one-click Docker deployment.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-embedded-003B57?style=flat-square&logo=sqlite)](https://sqlite.org)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-00ff88?style=flat-square)](LICENSE)

</div>

---

## ✦ Preview

![Preview](https://raw.githubusercontent.com/Evlos/uploads/refs/heads/main/%20BOOKMARKS%20-%20Google%20Chrome_2026-03-30_13-56-35.jpg)

![Preview](https://raw.githubusercontent.com/Evlos/uploads/refs/heads/main/%20BOOKMARKS%20-%20Google%20Chrome_2026-06-04_18-49-20.jpg)

---


## ✦ Features

- **CRUD operations** — Add, edit, and delete bookmarks with custom titles.
- **Edit mode** — Click `EDIT` in the top-right corner to enter edit mode; the button turns yellow. Only in edit mode are the per-item EDIT / DEL / MOVE controls visible. Click again, or press `E`, to exit.
- **Add mode** — Click `+ ADD` in the top-right corner to reveal the ADD NEW ENTRY form. `CANCEL` exits add mode without submitting. Add mode and edit mode are mutually exclusive.
- **Multi-column layout** — Switch the entry list between 1 / 2 / 3 / 4 column grid layouts via the toolbar next to the entry count, or with the `1`–`4` keys. Column preference is persisted across sessions. Cards adapt on their own via container queries: in dense layouts the host chip and index are dropped so titles stay readable, and on small screens the grid collapses to a single column regardless of the saved preference.
- **Container width** — Switch the shell between 760 / 960 / 1024 / 98% via the toolbar. Persisted across sessions.
- **Light / Dark theme** — Toggle between the warm paper palette and the phosphor-green terminal palette via the `DARK` / `LIGHT` button. Theme preference is persisted across sessions, and is applied before first paint so the page never flashes.
- **Persistent preferences** — Column layout, container width, and theme selections are saved to `localStorage` and automatically restored on every page load.
- **Delete confirmation** — Deleting a bookmark requires a second confirmation via a modal overlay, preventing accidental removal.
- **Button-driven reordering** — In edit mode, click `MOVE` on an entry and then `BEFORE` / `AFTER` on any other entry. The new order is written to the database immediately. Works in any column count, since it reorders the DOM rather than relying on drag coordinates.
- **Modal editing** — Click EDIT to open a dialog prefilled with the current title and URL; changes are written in place without a page reload.
- **Seamless inserts** — Newly added entries appear in the list immediately instead of triggering a full page reload.
- **Keyboard shortcuts** — `N` new entry · `E` edit mode · `T` theme · `1`–`4` columns · `Esc` close dialog / cancel move. Shortcuts stay out of the way while you are typing in a field.
- **Accessibility** — Dialogs use `inert` to trap focus and restore it on close, carry `role="dialog"` / `aria-modal`, close on `Esc` or backdrop click, and every control has a visible focus ring.
- **Toast notifications** — Lightweight, terminal-style pop-ups appear after every action.
- **Zero frontend dependencies** — No frameworks, no build step, and no CDN: the page ships hand-written CSS and vanilla JS, so it renders instantly and works offline.
- **SQLite persistence** — Data is securely stored in a local file without needing an external database.
- **One-click Docker deployment** — The multi-stage Alpine build keeps the container image extremely small.
- **Comprehensive test coverage** — Full workflow testing with pytest covers the homepage, adding, deleting, editing, and reordering.


## ✦ UI Modes

| Mode | Trigger | Effect |
| :-- | :-- | :-- |
| **Normal** | Default | Read-only view; per-item actions hidden; multi-column layout available |
| **Edit mode** | `EDIT` button or `E` | Shows the EDIT / DEL / MOVE row on every entry; your column choice is respected |
| **Add mode** | `+ ADD` button or `N` | Reveals the ADD NEW ENTRY form; `CANCEL` hides it again |
| **Move mode** | `MOVE` on an entry (edit mode) | Marks the source entry and offers `BEFORE` / `AFTER` targets on the others |
| **Light / Dark** | `DARK` / `LIGHT` button or `T` | Switches between the paper and phosphor-green palettes; preference saved automatically |

> Edit mode and add mode are mutually exclusive — activating one automatically exits the other.


## ✦ Tech Stack

| Layer | Technology |
| :-- | :-- |
| Backend framework | Python 3.12 · Flask |
| Data storage | SQLite (`data/bookmarks.db`) |
| Template engine | Jinja2 |
| Frontend interaction | Vanilla JS (event delegation) · no libraries |
| UI style | Cyberpunk terminal, hand-written CSS custom properties |
| Preference persistence | `localStorage` (`bmTheme`, `bmCols`, `bmWidth`) |
| Containerization | Docker (Alpine multi-stage build) |
| Testing framework | pytest · Flask Test Client |

## ✦ Quick Start

### Method 1: GitHub Container Registry (Simplest)

```bash
# Pull and run the pre-built image directly
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  --name portal \
  ghcr.io/evlos/portal:latest
```

Visit [http://localhost:5000](http://localhost:5000) to start using the app.

### Method 2: Local Docker Build

```bash
# Build the image
docker build -t portal .

# Run the container with a mounted volume for persistent data
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  --name portal \
  portal
```

Visit [http://localhost:5000](http://localhost:5000) to start using the app.

### Method 3: Run Locally

```bash
# Clone the repository
git clone <repo-url>
cd portal

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```


## ✦ API Endpoints

| Method | Path | Description |
| :-- | :-- | :-- |
| `GET` | `/` | Home page, renders the bookmark list |
| `POST` | `/add` | Add a new bookmark (form submission) — returns JSON including the new `id` |
| `POST` | `/edit/<id>` | Edit a bookmark (JSON) |
| `POST` | `/delete/<id>` | Delete a bookmark (returns JSON) |
| `POST` | `/reorder` | Update sorting order (JSON array of IDs) |

## ✦ Project Structure

```
portal/
├── app.py                 # Main Flask app, routing and database logic
├── templates/
│   └── index.html         # Single-page frontend, Jinja2 + vanilla JS
├── tests/
│   ├── conftest.py        # pytest fixtures, isolated test database
│   └── test_app.py        # Complete test cases
├── Dockerfile             # Alpine multi-stage build
├── requirements.txt       # Python dependencies
└── LICENSE                # GPL v3
```


## ✦ Run Tests

```bash
pip install pytest
pytest tests/ -v
```


## ✦ License

This project is open-sourced under the [GNU General Public License v3.0](LICENSE).
