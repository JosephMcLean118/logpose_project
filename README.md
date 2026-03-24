# Logpose

## Overview

Logpose is a game review platform powered by Django. Anyone can browse, search, and filter game reviews, but logged-in users can contribute to the community by writing reviews, rating games (1–5 stars), and customising their profile.

The app is designed to help gamers discover new titles, read honest community reviews, and keep track of the most popular and highest-rated games — all in one place.

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS + Bootstrap 5, JavaScript
- **Database:** SQLite (Django ORM)
- **Image Processing:** Pillow

## Local Setup

To run Logpose locally, follow the steps below. Please make sure you have Python 3.11+ installed.

### Clone the repository

```bash
git clone git@github.com:JosephMcLean118/logpose_project.git
cd logpose_project
```

### Create a virtual environment

**macOS/Linux**

```bash
python3 -m venv .venv
```

**Windows**

```bash
py -m venv .venv
```

### Activate the virtual environment

You'll need to do this each time you reopen the project.

**macOS/Linux**

```bash
source .venv/bin/activate
```

**Windows (PowerShell)**

```bash
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run migrations

```bash
python manage.py migrate
```

### Populate the database

This seeds the database with sample genres, games, users, and reviews.

```bash
python populate_logpose.py
```

### Run the server

```bash
python manage.py runserver
```

### Run tests

```bash
python manage.py test
```

### Open in browser

```
http://127.0.0.1:8000
```

## Git Workflow

Our `main` branch is protected. Changes should be made on a separate branch and merged via a Pull Request (PR) with 1 approval.

### How to build a feature

1. **Create a new branch for your task**
   Choose a short, descriptive name (e.g. `feat-review-search`, `fix-login-form`).

   ```bash
   git checkout main
   git pull
   git checkout -b feat/your-branch-name
   ```

2. **Make your changes and commit regularly**

   ```bash
   git add .
   git commit -m "Short description of what you changed"
   ```

3. **Push your branch to GitHub**

   ```bash
   git push -u origin feat/your-branch-name
   ```

4. **Open a Pull Request**
   Open a PR from your branch to `main`. Request a teammate to review and approve your code before merging. When merging, choose **Squash and merge**.

## Acknowledgements & External Sources

To be updated — we will list any code snippets, images, and data sources used during development.
