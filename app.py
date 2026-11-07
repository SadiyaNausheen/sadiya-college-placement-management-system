
import os
from datetime import date
from flask import Flask, request, redirect, url_for, render_template_string, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)

# MySQL Database Connection
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("DB_PASSWORD"),
    "database": "sadiya_placement_db"
}

STYLE = """
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f6fb;
    color: #1f2937;
}
.layout { display: flex; min-height: 100vh; }
.side {
    width: 235px;
    background: #14213d;
    color: white;
    padding: 28px 18px;
}
.brand { font-size: 21px; font-weight: bold; }
.sub { color: #cbd5e1; font-size: 12px; margin: 10px 0 30px; }
.side a {
    display: block;
    color: white;
    text-decoration: none;
    padding: 13px;
    margin: 6px 0;
    border-radius: 8px;
}
.side a:hover, .side a.active { background: #2563eb; }
.main { flex: 1; padding: 30px; min-width: 0; }
.top { margin-bottom: 25px; }
.top h1 { margin: 0; font-size: 28px; }
.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 22px;
}
.card, .panel {
    background: white;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 3px 12px #0000000d;
}
.metric { font-size: 32px; font-weight: bold; color: #14213d; }
.label { color: #64748b; font-size: 13px; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb; }
th { background: #f1f5f9; }
.formgrid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
}
.field { margin-bottom: 12px; }
label { display: block; margin-bottom: 6px; font-weight: bold; }
input, select {
    width: 100%;
    padding: 11px;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
}
.btn {
    display: inline-block;
    background: #2563eb;
    color: white;
    border: 0;
    padding: 11px 17px;
    border-radius: 7px;
    cursor: pointer;
    text-decoration: none;
}
.notice { background: #dcfce7; padding: 12px; margin-bottom: 15px; }
@media(max-width:800px) {
    .layout { display: block; }
    .side { width: 100%; }
    .side nav { display: flex; flex-wrap: wrap; }
    .main { padding: 15px; }
    .cards, .formgrid { grid-template-columns: 1fr; }
}
"""

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }} | Sadiya Placement Portal</title>
<style>{{ style }}</style>
</head>
<body>
<div class="layout">
<aside class="side">
<div class="brand">Sadiya Placement Portal</div>
<div class="sub">College Placement Management</div>
<nav>
<a href="{{ url_for('dashboard') }}">Dashboard</a>
<a href="{{ url_for('students') }}">Students</a>
<a href="{{ url_for('companies') }}">Companies</a>
<a href="{{ url_for('applications') }}">Applications</a>
</nav>
</aside>
<main class="main">
<div class="top"><h1>{{ title }}</h1></div>
{% with messages = get_flashed_messages() %}
{% for message in messages %}
<div class="notice">{{ message }}</div>
{% endfor %}
{% endwith %}
{{ content|safe }}
</main>
</div>
</body>
</html>
"""


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            department VARCHAR(50),
            cgpa DECIMAL(3,2)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            company_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            company_name VARCHAR(100) NOT NULL,
            location VARCHAR(100),
            job_role VARCHAR(100),
            package_lpa DECIMAL(5,2),
            eligibility_cgpa DECIMAL(3,2)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            application_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            company_id INT NOT NULL,
            application_date DATE,
            status VARCHAR(30) DEFAULT 'Applied',
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (company_id) REFERENCES companies(company_id)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


def query(sql, values=(), fetch=True):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, values)

    result = cur.fetchall() if fetch else None

    if not fetch:
        conn.commit()

    cur.close()
    conn.close()
    return result


def page(title, page_name, content):
    return render_template_string(
        TEMPLATE,
        title=title,
        page=page_name,
        content=content,
        style=STYLE
    )


@app.route("/")
def dashboard():
    try:
        students_count = query(
            "SELECT COUNT(*) AS n FROM students"
        )[0]["n"]

        companies_count = query(
            "SELECT COUNT(*) AS n FROM companies"
        )[0]["n"]

        applications_count = query(
            "SELECT COUNT(*) AS n FROM applications"
        )[0]["n"]

        content = f"""
        <section class="cards">
            <div class="card">
                <div class="label">REGISTERED STUDENTS</div>
                <div class="metric">{students_count}</div>
            </div>
            <div class="card">
                <div class="label">COMPANIES</div>
                <div class="metric">{companies_count}</div>
            </div>
            <div class="card">
                <div class="label">APPLICATIONS</div>
                <div class="metric">{applications_count}</div>
            </div>
        </section>
        <section class="panel">
            <h2>Welcome to Sadiya Placement Portal</h2>
            <p>Manage students, companies and placement applications.</p>
            <a class="btn" href="/students">Add Student</a>
            <a class="btn" href="/companies">Add Company</a>
        </section>
        """

        return page("Dashboard", "dashboard", content)

    except Error as e:
        return page(
            "Database Error",
            "dashboard",
            f"<section class='panel'><h2>MySQL Error</h2><p>{e}</p></section>"
        )


@app.route("/students", methods=["GET", "POST"])
def students():
    if request.method == "POST":
        query(
            """INSERT INTO students
            (student_name, email, department, cgpa)
            VALUES (%s, %s, %s, %s)""",
            (
                request.form["student_name"],
                request.form["email"],
                request.form.get("department") or None,
                request.form.get("cgpa") or None
            ),
            False
        )
        flash("Student added successfully!")
        return redirect(url_for("students"))

    data = query("SELECT * FROM students ORDER BY student_id DESC")

    rows = ""
    for r in data:
        rows += f"""
        <tr>
            <td>{r['student_id']}</td>
            <td>{r['student_name']}</td>
            <td>{r['email']}</td>
            <td>{r['department'] or ''}</td>
            <td>{r['cgpa'] or ''}</td>
        </tr>
        """

    if not rows:
        rows = "<tr><td colspan='5'>No students added yet.</td></tr>"

    content = f"""
    <section class="panel">
        <h2>Register Student</h2>
        <form method="POST">
            <div class="formgrid">
                <div class="field">
                    <label>Student Name</label>
                    <input name="student_name" required>
                </div>
                <div class="field">
                    <label>Email</label>
                    <input type="email" name="email" required>
                </div>
                <div class="field">
                    <label>Department</label>
                    <input name="department">
                </div>
                <div class="field">
                    <label>CGPA</label>
                    <input type="number" name="cgpa" min="0" max="10" step="0.01">
                </div>
            </div>
            <button class="btn">Save Student</button>
        </form>
    </section>
    <section class="panel">
        <h2>Student Records</h2>
        <table>
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Department</th><th>CGPA</th></tr>
            {rows}
        </table>
    </section>
    """

    return page("Students", "students", content)


@app.route("/companies", methods=["GET", "POST"])
def companies():
    if request.method == "POST":
        query(
            """INSERT INTO companies
            (company_name, location, job_role, package_lpa, eligibility_cgpa)
            VALUES (%s, %s, %s, %s, %s)""",
            (
                request.form["company_name"],
                request.form.get("location"),
                request.form.get("job_role"),
                request.form.get("package_lpa") or None,
                request.form.get("eligibility_cgpa") or None
            ),
            False
        )
        flash("Company added successfully!")
        return redirect(url_for("companies"))

    data = query("SELECT * FROM companies ORDER BY company_id DESC")

    rows = ""
    for r in data:
        rows += f"""
        <tr>
            <td>{r['company_id']}</td>
            <td>{r['company_name']}</td>
            <td>{r['location'] or ''}</td>
            <td>{r['job_role'] or ''}</td>
            <td>{r['package_lpa'] or ''}</td>
            <td>{r['eligibility_cgpa'] or ''}</td>
        </tr>
        """

    if not rows:
        rows = "<tr><td colspan='6'>No companies added yet.</td></tr>"

    content = f"""
    <section class="panel">
        <h2>Add Company</h2>
        <form method="POST">
            <div class="formgrid">
                <div class="field">
                    <label>Company Name</label>
                    <input name="company_name" required>
                </div>
                <div class="field">
                    <label>Location</label>
                    <input name="location">
                </div>
                <div class="field">
                    <label>Job Role</label>
                    <input name="job_role">
                </div>
                <div class="field">
                    <label>Package (LPA)</label>
                    <input type="number" name="package_lpa" step="0.01">
                </div>
                <div class="field">
                    <label>Eligibility CGPA</label>
                    <input type="number" name="eligibility_cgpa" min="0" max="10" step="0.01">
                </div>
            </div>
            <button class="btn">Save Company</button>
        </form>
    </section>
    <section class="panel">
        <h2>Company Records</h2>
        <table>
            <tr><th>ID</th><th>Company</th><th>Location</th><th>Role</th><th>Package</th><th>CGPA</th></tr>
            {rows}
        </table>
    </section>
    """

    return page("Companies", "companies", content)


@app.route("/applications", methods=["GET", "POST"])
def applications():
    if request.method == "POST":
        query(
            """INSERT INTO applications
            (student_id, company_id, application_date, status)
            VALUES (%s, %s, %s, %s)""",
            (
                request.form["student_id"],
                request.form["company_id"],
                request.form.get("application_date") or date.today(),
                request.form.get("status") or "Applied"
            ),
            False
        )
        flash("Application recorded successfully!")
        return redirect(url_for("applications"))

    students_data = query(
        "SELECT student_id, student_name FROM students ORDER BY student_name"
    )
    companies_data = query(
        "SELECT company_id, company_name FROM companies ORDER BY company_name"
    )

    student_options = "".join(
        f"<option value='{r['student_id']}'>{r['student_name']}</option>"
        for r in students_data
    )

    company_options = "".join(
        f"<option value='{r['company_id']}'>{r['company_name']}</option>"
        for r in companies_data
    )

    data = query("""
        SELECT a.application_id, s.student_name, c.company_name,
               a.application_date, a.status
        FROM applications a
        JOIN students s ON a.student_id = s.student_id
        JOIN companies c ON a.company_id = c.company_id
        ORDER BY a.application_id DESC
    """)

    rows = ""
    for r in data:
        rows += f"""
        <tr>
            <td>{r['application_id']}</td>
            <td>{r['student_name']}</td>
            <td>{r['company_name']}</td>
            <td>{r['application_date'] or ''}</td>
            <td>{r['status']}</td>
        </tr>
        """

    if not rows:
        rows = "<tr><td colspan='5'>No applications recorded yet.</td></tr>"

    disabled = "" if students_data and companies_data else "disabled"

    content = f"""
    <section class="panel">
        <h2>Record Application</h2>
        <p>Add at least one student and one company first.</p>
        <form method="POST">
            <div class="formgrid">
                <div class="field">
                    <label>Student</label>
                    <select name="student_id" required>{student_options}</select>
                </div>
                <div class="field">
                    <label>Company</label>
                    <select name="company_id" required>{company_options}</select>
                </div>
                <div class="field">
                    <label>Application Date</label>
                    <input type="date" name="application_date" value="{date.today()}">
                </div>
                <div class="field">
                    <label>Status</label>
                    <select name="status">
                        <option>Applied</option>
                        <option>Shortlisted</option>
                        <option>Interview</option>
                        <option>Selected</option>
                        <option>Rejected</option>
                    </select>
                </div>
            </div>
            <button class="btn" {disabled}>Save Application</button>
        </form>
    </section>
    <section class="panel">
        <h2>Application Records</h2>
        <table>
            <tr><th>ID</th><th>Student</th><th>Company</th><th>Date</th><th>Status</th></tr>
            {rows}
        </table>
    </section>
    """

    return page("Applications", "applications", content)


if __name__ == "__main__":
    try:
        init_db()
        print("MySQL connected successfully!")
        print("Database tables are ready.")
    except Error as e:
        print("MySQL connection error:", e)
        print("Check your MySQL password and database settings.")

    print("Starting Sadiya Placement Portal at http://127.0.0.1:5000")
    app.run(debug=True)
