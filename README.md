# 🎟️ SnapTicket

A Flask-based ticket booking platform for movies, buses, trains, rentals, and hotels, with user accounts, subscription plans, and an admin dashboard.

---

## Features

- **User accounts** — register, log in, log out (passwords hashed with Werkzeug)
- **Multi-category booking** — Movies 🎬, Buses 🚌, Trains 🚆, Rentals 🚗, Hotels 🏨
- **Subscription plans** — Free, Basic, Standard, Premium
- **Admin dashboard** — view all registered users and all bookings across categories
- **MySQL-backed** — persistent relational storage (see [Database](#database) below)

---

## Project Structure

```
SnapTicket/
│
├── app.py                  # Flask routes and app logic
├── database.py             # MySQL connection + table setup
├── requirements.txt        # Python dependencies
│
├── templates/
│   ├── index.html          # Landing page
│   ├── register.html       # User registration
│   ├── login.html          # User login
│   ├── admin_login.html    # Admin login
│   ├── dashboard.html      # User dashboard (booking categories + plans)
│   ├── admin_dashboard.html# Admin view of users & bookings
│   └── booking.html        # Category-specific booking form + history
│
└── static/
    ├── style.css            # All app styling
    └── script.js            # Auto-dismiss flash messages
```

---

## Requirements

- Python 3.9+
- MySQL Server (local or remote) — e.g. via [XAMPP](https://www.apachefriends.org) or [MySQL Community Server](https://dev.mysql.com/downloads/installer/)

---

## Setup

### 1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Create the database

Start your MySQL server, then either let the app create tables automatically (Step 4), or create them yourself first:

```sql
CREATE DATABASE snapticket;
USE snapticket;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    subscription VARCHAR(50) NOT NULL DEFAULT 'Free',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'event',
    event_name VARCHAR(255) NOT NULL,
    event_date VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 3. Configure your database credentials

Open `database.py` and update `DB_CONFIG` with your own MySQL details:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "snapticket",
}
```

### 4. Run the app

```bash
python app.py
```

Tables are created automatically on first run if they don't already exist. Visit:

```
http://127.0.0.1:5000
```

---

## Default Admin Login

| Field    | Value                     |
|----------|---------------------------|
| Email    | admin@snapticket.com      |
| Password | admin123                  |

> ⚠️ Hardcoded in `app.py` for development only — change or move to a proper admin table before deploying anywhere real.

Admin dashboard: `http://127.0.0.1:5000/admin_login`

---

## Routes

| Route                | Method    | Description                                  |
|-----------------------|-----------|-----------------------------------------------|
| `/`                   | GET       | Landing page                                  |
| `/register`           | GET/POST  | Create a new account                          |
| `/login`              | GET/POST  | Log in                                        |
| `/logout`             | GET       | Log out                                       |
| `/dashboard`          | GET       | User dashboard (categories + subscription)    |
| `/book/<category>`    | GET/POST  | Book movies, buses, trains, rentals, or hotels|
| `/subscribe?plan=...` | GET       | Upgrade subscription (`basic`/`standard`/`premium`) |
| `/admin_login`        | GET/POST  | Admin login                                   |
| `/admin_dashboard`    | GET       | View all users and bookings                  |
| `/admin_logout`       | GET       | Admin logout                                  |

---

## Notes

- Passwords are hashed with `werkzeug.security.generate_password_hash` — never stored in plain text.
- Session-based auth via Flask's built-in `session` — set a strong, unique `app.secret_key` before deploying.
- The background image referenced in `style.css` (`/static/SNAPTICKET.png`) is not included — add your own logo/background image to the `static/` folder with that filename.
- This is a development setup (`debug=True`). Disable debug mode and use a production WSGI server (e.g. Gunicorn) before deploying publicly.

---

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** MySQL (via `mysql-connector-python`)
- **Frontend:** Jinja2 templates, vanilla CSS/JS

---

## Author

**Vignesh K**
B.Tech, 1st Year — Information Technology (Data Analytics)
Alliance University# Snapticket
