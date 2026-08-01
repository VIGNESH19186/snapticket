from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = "change-this-secret-key-in-production"

# Hardcoded admin credentials (replace with a proper admin table in production)
ADMIN_EMAIL = "admin@snapticket.com"
ADMIN_PASSWORD = "admin123"


# ---------- Helpers ----------
def login_required(view_name="login"):
    return "user_id" in session


# ---------- Public routes ----------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.")
            return redirect(url_for("register"))

        conn = get_db_connection()
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if existing:
            conn.close()
            flash("An account with that email already exists.")
            return redirect(url_for("register"))

        hashed = generate_password_hash(password)
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed),
        )
        conn.commit()
        conn.close()

        flash("Account created! Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ---------- User dashboard & booking ----------
@app.route("/dashboard")
def dashboard():
    if not login_required():
        flash("Please log in first.")
        return redirect(url_for("login"))
    return render_template("dashboard.html", user_name=session.get("user_name"))


@app.route("/booking", methods=["GET", "POST"])
def booking():
    if not login_required():
        flash("Please log in first.")
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":
        event_name = request.form.get("event_name", "").strip()
        event_date = request.form.get("event_date", "").strip()
        quantity = request.form.get("quantity", "1").strip()

        if not event_name or not event_date or not quantity.isdigit():
            flash("Please fill in all booking fields correctly.")
        else:
            conn.execute(
                "INSERT INTO bookings (user_id, event_name, event_date, quantity) VALUES (?, ?, ?, ?)",
                (session["user_id"], event_name, event_date, int(quantity)),
            )
            conn.commit()
            flash("Ticket booked successfully!")

    my_bookings = conn.execute(
        "SELECT * FROM bookings WHERE user_id = ? ORDER BY created_at DESC",
        (session["user_id"],),
    ).fetchall()
    conn.close()

    return render_template("booking.html", bookings=my_bookings)


# ---------- Admin routes ----------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))

        flash("Invalid admin credentials.")
        return redirect(url_for("admin_login"))

    return render_template("admin_login.html")


@app.route("/admin_dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        flash("Please log in as admin first.")
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at DESC").fetchall()
    bookings = conn.execute("""
        SELECT bookings.id, bookings.event_name, bookings.event_date, bookings.quantity,
               bookings.created_at, users.name AS user_name, users.email AS user_email
        FROM bookings
        JOIN users ON bookings.user_id = users.id
        ORDER BY bookings.created_at DESC
    """).fetchall()
    conn.close()

    return render_template("admin_dashboard.html", users=users, bookings=bookings)


@app.route("/admin_logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)