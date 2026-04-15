from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DATABASE
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    # OLD TABLE SAME
    conn.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        gender TEXT,
        phone TEXT,
        disease TEXT
    )
    """)

    # NEW COLUMNS (SAFE)
    columns = [
        ("room", "TEXT"),
        ("payment", "TEXT"),
        ("payment_date", "TEXT"),
        ("admit_date", "TEXT"),
        ("discharge_date", "TEXT")
    ]

    for col, typ in columns:
        try:
            conn.execute(f"ALTER TABLE patients ADD COLUMN {col} {typ}")
        except:
            pass

    conn.close()

init_db()

# HOME
@app.route('/')
def home():
    return redirect('/login')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('/dashboard')
    return render_template("login.html")

# LOGOUT
@app.route('/logout')
def logout():
    return redirect('/login')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    conn = get_db()
    patients = conn.execute("SELECT * FROM patients").fetchall()
    conn.close()

    total = len(patients)
    male = len([p for p in patients if p["gender"] and p["gender"].lower() == "male"])
    female = len([p for p in patients if p["gender"] and p["gender"].lower() == "female"])

    return render_template("dashboard.html",
                           patients=patients,
                           total=total,
                           male=male,
                           female=female)

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = get_db()

        conn.execute("""
        INSERT INTO patients(
        name,age,gender,phone,disease,
        room,payment,payment_date,admit_date,discharge_date
        )
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            request.form['name'],
            request.form['age'],
            request.form['gender'],
            request.form['phone'],
            request.form['disease'],
            request.form.get('room'),
            request.form.get('payment'),
            request.form.get('payment_date'),
            request.form.get('admit_date'),
            request.form.get('discharge_date')
        ))

        conn.commit()
        conn.close()

        return render_template("register.html", msg="Patient Added Successfully!")

    return render_template("register.html")

# VIEW
@app.route('/view/<int:id>')
def view(id):
    conn = get_db()
    patient = conn.execute("SELECT * FROM patients WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("view.html", patient=patient)

# EDIT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()

    if request.method == 'POST':
        conn.execute("""
        UPDATE patients SET
        name=?,age=?,gender=?,phone=?,disease=?,
        room=?,payment=?,payment_date=?,admit_date=?,discharge_date=?
        WHERE id=?
        """, (
            request.form['name'],
            request.form['age'],
            request.form['gender'],
            request.form['phone'],
            request.form['disease'],
            request.form.get('room'),
            request.form.get('payment'),
            request.form.get('payment_date'),
            request.form.get('admit_date'),
            request.form.get('discharge_date'),
            id
        ))

        conn.commit()
        conn.close()
        return redirect('/dashboard')

    patient = conn.execute("SELECT * FROM patients WHERE id=?", (id,)).fetchone()
    conn.close()

    return render_template("edit.html", patient=patient)

# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/dashboard')

# RUN
if __name__ == "__main__":
    app.run(debug=True)