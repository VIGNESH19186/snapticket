from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

# ================= ADMIN EMAIL =================
ADMIN_EMAILS = ["vignesh.k1918@gmail.com"]

# ================= DATABASE =================
users = {}

# ================= HOME =================
@app.route('/')
def home():
    return render_template('index.html')

# ================= ADMIN LOGIN =================
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        email = request.form.get('email')

        if email in ADMIN_EMAILS:
            session['admin'] = email
            return redirect('/dashboard')

        return "❌ Access Denied"

    return render_template('admin.html')

# ================= USER REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        users[email] = {
            "password": password,
            "bookings": [],
            "subscription": "No Plan"
        }

        return redirect('/login')

    return render_template('register.html')

# ================= USER LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users and users[email]["password"] == password:
            session['user'] = email
            return redirect('/dashboard')

        return "❌ Invalid Login"

    return render_template('user_login.html')

# ================= DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    if 'user' not in session and 'admin' not in session:
        return redirect('/')

    email = session.get('user')
    user_data = None

    if email:
        user_data = users.get(email)

    return render_template('dashboard.html', user_data=user_data, email=email)

# ================= BOOK =================
@app.route('/book/<service>')
def book(service):
    if 'user' not in session:
        return redirect('/login')

    email = session['user']
    users[email]["bookings"].append(service)

    return redirect('/dashboard')

# ================= SUBSCRIBE =================
@app.route('/subscribe', methods=['POST'])
def subscribe():
    if 'user' not in session:
        return redirect('/login')

    email = session['user']
    plan = request.form.get('plan')

    users[email]["subscription"] = plan

    return redirect('/dashboard')

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)