from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE INIT
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Patient Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        disease TEXT
    )
    ''')

    # Admin Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin(
        username TEXT,
        password TEXT
    )
    ''')

    # Default Admin
    cursor.execute("SELECT * FROM admin")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admin VALUES (?,?)", ("admin","1234"))

    conn.commit()
    conn.close()

init_db()

# LOGIN
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username,password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "Invalid Username or Password"

    return render_template('login.html')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', patients=patients)

# ADD PATIENT
@app.route('/register', methods=['GET','POST'])
def register():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO patients (name,age,gender,phone,disease) VALUES (?,?,?,?,?)",
                       (request.form['name'], request.form['age'], request.form['gender'],
                        request.form['phone'], request.form['disease']))

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('register_patient.html')

# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    if 'user' not in session:
        return redirect('/')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/dashboard')

# CHANGE PASSWORD (PERMANENT)
@app.route('/change_password', methods=['GET','POST'])
def change_password():
    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':
        old = request.form['old']
        new = request.form['new']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM admin WHERE password=?", (old,))
        if cursor.fetchone():
            cursor.execute("UPDATE admin SET password=?", (new,))
            conn.commit()
            msg = "Password Changed Successfully"
        else:
            msg = "Wrong Old Password"

        conn.close()
        return msg

    return render_template('change_password.html')

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)