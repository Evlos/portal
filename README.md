<div align="center">

```
██████   ██████  ██████  ████████  █████  ██
██   ██ ██    ██ ██   ██    ██    ██   ██ ██
██████  ██    ██ ██████     ██    ███████ ██
██      ██    ██ ██   ██    ██    ██   ██ ██
██       ██████  ██   ██    ██    ██   ██ ███████
```

**// BOOKMARKS — terminal link vault**

A minimalist bookmark management website built with Flask, SQLite, and Tailwind CSS, featuring multi-column layout, light/dark theme switching, and one-click Docker deployment.

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
- **Right-click context menu** — Right-click any bookmark to open its action menu: `Edit`, `Move`, `Copy link`, `Delete`. There is no separate edit mode. On touch devices each card also carries a `⋮` button that opens the same menu.
- **Add mode** — Click `Add bookmark` in the header to reveal the new-bookmark form, which focuses the URL field on open. A `Cancel` button inside the form exits add mode without submitting.
- **Multi-column layout** — Switch the entry list between 1 / 2 / 3 / 4 column grids via the toolbar. On narrow screens the grid always collapses to a single column while the saved choice is still reported. Column preference is persisted across sessions.
- **Content width** — Set the content column to 640 / 768 / 1024 / 1280 px from the toolbar. Preference is persisted across sessions. The header bar always spans the full viewport, so it never floats on a wide screen.
- **Light / Dark theme** — Toggle from the sun/moon button in the header. The saved theme is applied before first paint, so there is no flash of the wrong palette.
- **Persistent preferences** — Theme, column layout, and width are saved to `localStorage` and restored on every page load.
- **Delete confirmation** — Deleting a bookmark requires confirmation in a modal dialog, preventing accidental removal.
- **Reordering** — `Move` from the context menu highlights the entry and shows a banner; right-clicking any other bookmark then offers `Place before this` / `Place after this`. The new order is written to the database immediately.
- **Modal editing** — `Edit` opens a dialog for the entry; saving updates the row in place without a page reload.
- **Toast notifications** — Lightweight success/error toasts appear after every action, announced via `aria-live`.
- **Keyboard & screen reader support** — The context menu exposes `role="menu"` / `role="menuitem"` with arrow-key, `Home` / `End` and `Escape` handling; visible focus rings throughout; `Escape` closes any open menu or dialog; focus returns to the trigger on close; dialogs expose `role="dialog"` / `aria-modal`.
- **Responsive layout** — The header collapses to icon buttons and cards stack on phones; long titles and URLs truncate rather than overflow.
- **Zero build step** — Tailwind CSS runs from the Play CDN and all logic is vanilla JavaScript, so `python app.py` is the only thing needed to run the app.
- **SQLite persistence** — Data is securely stored in a local file without needing an external database.
- **One-click Docker deployment** — The multi-stage Alpine build keeps the container image extremely small.
- **Comprehensive test coverage** — Full workflow testing with pytest covers the homepage, adding, deleting, editing, and reordering.


## ✦ UI Modes

| Mode | Trigger | Effect |
| :-- | :-- | :-- |
| **Normal** | Default | Read-only view; per-item actions live in the right-click menu |
| **Context menu** | Right-click a bookmark (or its `⋮` button) | Shows `Edit` / `Move` / `Copy link` / `Delete` for that entry |
| **Move mode** | `Move` from the context menu | Highlights the entry and shows a banner; right-clicking another bookmark offers `Place before this` / `Place after this` |
| **Add mode** | `Add bookmark` button (header) | Reveals the new-bookmark form and focuses the URL field; `Cancel` hides it again |
| **Light mode** | Sun/moon button (header) | Switches to the light palette; preference saved automatically |

> `Escape` closes an open context menu first, then any open dialog, then add mode, then move mode.


## ✦ Tech Stack

| Layer | Technology |
| :-- | :-- |
| Backend framework | Python 3.12 · Flask |
| Data storage | SQLite (`data/bookmarks.db`) |
| Template engine | Jinja2 |
| Styling | Tailwind CSS 3 (Play CDN) + `@layer components` |
| Frontend interaction | Vanilla JavaScript (no framework, no build step) |
| Icons | Inline SVG sprite |
| Preference persistence | `localStorage` |
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
| `POST` | `/add` | Add a new bookmark (form submission) |
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
