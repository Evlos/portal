<div align="center">

```
██████   ██████  ██████  ████████  █████  ██
██   ██ ██    ██ ██   ██    ██    ██   ██ ██
██████  ██    ██ ██████     ██    ███████ ██
██      ██    ██ ██   ██    ██    ██   ██ ██
     ██       ██████  ██   ██    ██    ██   ██ ███████
```

**// BOOKMARKS — terminal link vault**

A cyberpunk-style minimalist bookmark management website built with Flask and SQLite, featuring drag-and-drop sorting and one-click Docker deployment.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-embedded-003B57?style=flat-square&logo=sqlite)](https://sqlite.org)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-00ff88?style=flat-square)](LICENSE)

</div>

---

## ✦ Preview

![Preview](https://raw.githubusercontent.com/Evlos/uploads/refs/heads/main/%20BOOKMARKS%20-%20Google%20Chrome_2026-03-29_12-43-08.jpg)

---


## ✦ Features

- **CRUD operations** — Add, edit, and delete bookmarks with custom titles.
- **Drag-and-drop sorting** — Drag items to instantly save their order using SortableJS, with no data lost on refresh.
- **Inline editing** — Click EDIT to expand the editing panel directly in the list, eliminating the need for page redirects.
- **Toast notifications** — Lightweight, terminal-style pop-ups appear after every action.
- **Zero frontend dependencies** — The project only imports SortableJS via CDN, avoiding heavy frontend frameworks.
- **SQLite persistence** — Data is securely stored in a local file without needing an external database.
- **One-click Docker deployment** — The multi-stage Alpine build keeps the container image extremely small.
- **Comprehensive test coverage** — Full workflow testing with pytest covers the homepage, adding, deleting, editing, and reordering.


## ✦ Tech Stack

| Layer | Technology |
| :-- | :-- |
| Backend framework | Python 3.12 · Flask |
| Data storage | SQLite (`data/bookmarks.db`) |
| Template engine | Jinja2 |
| Frontend interaction | Vanilla JS · SortableJS 1.15 |
| UI style | Cyberpunk terminal, pure CSS variables |
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
