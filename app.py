from flask import Flask, render_template, request, redirect, url_for, session, Response
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# store password (simple)
ADMIN_PASSWORD = "1234"

# DATABASE
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect('/login')

# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    global ADMIN_PASSWORD

    if request.method == 'POST':
        if request.form['username'] == "admin" and request.form['password'] == ADMIN_PASSWORD:
            session['user'] = "admin"
            return redirect('/dashboard')
        else:
            return "Invalid Username or Password"

    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# DASHBOARD
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    search = request.form.get('search')
    gender = request.form.get('gender')
    disease = request.form.get('disease')

    query = "SELECT * FROM patients WHERE 1=1"
    params = []

    if search:
        query += " AND (name LIKE ? OR phone LIKE ?)"
        params.extend(['%'+search+'%', '%'+search+'%'])

    if gender:
        query += " AND gender=?"
        params.append(gender)

    if disease:
        query += " AND disease LIKE ?"
        params.append('%'+disease+'%')

    cursor.execute(query, params)
    patients = cursor.fetchall()

    # COUNTS
    cursor.execute("SELECT COUNT(*) FROM patients")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patients WHERE gender='male'")
    male = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patients WHERE gender='female'")
    female = cursor.fetchone()[0]

    conn.close()

    return render_template('dashboard.html', patients=patients, total=total, male=male, female=female)

# ADD PATIENT
@app.route('/register', methods=['GET','POST'])
def register():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO patients (name,age,gender,phone,disease) VALUES (?,?,?,?,?)",
            (
                request.form['name'],
                request.form['age'],
                request.form['gender'],
                request.form['phone'],
                request.form['disease']
            )
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('register_patient.html')

# DELETE
@app.route('/delete/<int:id>')
def delete(id):

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/dashboard')

# EDIT
@app.route('/edit/<int:id>')
def edit(id):

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = cursor.fetchone()

    conn.close()

    return render_template('edit_patient.html', patient=patient)

# UPDATE
@app.route('/update/<int:id>', methods=['POST'])
def update(id):

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE patients 
    SET name=?, age=?, gender=?, phone=?, disease=? 
    WHERE id=?
    """, (
        request.form['name'],
        request.form['age'],
        request.form['gender'],
        request.form['phone'],
        request.form['disease'],
        id
    ))

    conn.commit()
    conn.close()

    return redirect('/dashboard')

# VIEW PATIENT
@app.route('/view/<int:id>')
def view(id):

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = cursor.fetchone()

    conn.close()

    return render_template('view_patient.html', p=patient)

# CHANGE PASSWORD
@app.route('/change_password', methods=['GET','POST'])
def change_password():
    global ADMIN_PASSWORD

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        old = request.form['old']
        new = request.form['new']

        if old == ADMIN_PASSWORD:
            ADMIN_PASSWORD = new
            return "Password Changed Successfully"
        else:
            return "Wrong Old Password"

    return render_template('change_password.html')

# EXPORT
@app.route('/export')
def export():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    conn.close()

    def generate():
        yield 'ID,Name,Age,Gender,Phone,Disease\n'
        for row in data:
            yield f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}\n"

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=patients.csv"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')