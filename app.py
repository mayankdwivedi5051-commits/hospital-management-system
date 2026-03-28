from flask import Flask, render_template, redirect, request

app = Flask(__name__)

# Dummy data
patients = [
    {"id": 1, "name": "rishabh", "age": 23, "gender": "male", "phone": "9090909090", "disease": "khasi"},
    {"id": 2, "name": "mayank", "age": 20, "gender": "male", "phone": "9090909090", "disease": "fever"},
    {"id": 3, "name": "jadu", "age": 45, "gender": "male", "phone": "8900808080", "disease": "fever"},
    {"id": 4, "name": "tannu", "age": 21, "gender": "female", "phone": "1234567898", "disease": "cough"},
]

# HOME
@app.route('/')
def home():
    return redirect('/login')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('/dashboard')
    return render_template('login.html')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    total = len(patients)
    male = len([p for p in patients if p["gender"] == "male"])
    female = len([p for p in patients if p["gender"] == "female"])

    return render_template(
        'dashboard.html',
        patients=patients,
        total=total,
        male=male,
        female=female
    )

# LOGOUT
@app.route('/logout')
def logout():
    return redirect('/login')

# ADD PATIENT
@app.route('/register')
def register():
    return "<h2>Add Patient Page (working)</h2>"

# VIEW
@app.route('/view/<int:id>')
def view(id):
    return f"<h2>Viewing Patient ID: {id}</h2>"

# EDIT
@app.route('/edit/<int:id>')
def edit(id):
    return f"<h2>Editing Patient ID: {id}</h2>"

# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    global patients
    patients = [p for p in patients if p["id"] != id]
    return redirect('/dashboard')

# RUN
if __name__ == '__main__':
    app.run(debug=True)