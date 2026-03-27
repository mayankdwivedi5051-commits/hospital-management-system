from flask import Flask, render_template, redirect, request

app = Flask(__name__)

# Dummy data (test ke liye)
patients = [
    {"id": 1, "name": "rishabh", "age": 23, "gender": "male", "phone": "9090909090", "disease": "khasi"},
    {"id": 2, "name": "mayank", "age": 20, "gender": "male", "phone": "9090909090", "disease": "fever"},
    {"id": 3, "name": "jadu", "age": 45, "gender": "male", "phone": "8900808080", "disease": "fever"},
    {"id": 4, "name": "tannu", "age": 21, "gender": "female", "phone": "1234567898", "disease": "cough"},
    {"id": 5, "name": "tasu", "age": 29, "gender": "female", "phone": "6307593233", "disease": "chhik ana"},
    {"id": 6, "name": "rohan", "age": 99, "gender": "male", "phone": "9090909090", "disease": "accident"},
]

# 👉 HOME → direct dashboard
@app.route('/')
def home():
    return redirect('/dashboard')

# 👉 LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('/dashboard')
    return render_template('login.html')

# 👉 DASHBOARD (MAIN PAGE)
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

# 👉 RUN APP
if __name__ == '__main__':
    app.run(debug=True)