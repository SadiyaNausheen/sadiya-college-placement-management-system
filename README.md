# Sadiya Placement Portal

A beginner-friendly College Placement Management System using Python Flask and MySQL.

## Features
- Dashboard with student, company, and application totals
- Add and view students
- Add and view companies
- Record applications and track status
- Delete student records (if they do not have linked applications)
- Responsive layout for laptop and mobile

## 1. Database
This project uses the database you created in MySQL Workbench:

`sadiya_placement_db`

The app automatically creates the three tables if they do not already exist:
- students
- companies
- applications

The table definitions match the SQL steps used while setting up the project.

## 2. Install packages
Open a terminal in this folder and run:

```bash
python -m pip install -r requirements.txt
```

## 3. Check MySQL password
Open `app.py` and find `DB_CONFIG` near the top.

Default settings:
- host: localhost
- user: root
- password: empty
- database: sadiya_placement_db

If your MySQL root account has a password, replace the empty string in:
`"password": os.environ.get("DB_PASSWORD", ""),`
with your password, for example:
`"password": os.environ.get("DB_PASSWORD", "YOUR_MYSQL_PASSWORD"),`

Do not share your password with anyone.

## 4. Run the website
In the VS Code terminal, run:

```bash
python app.py
```

Open this address in Chrome:

`http://127.0.0.1:5000`

Keep the terminal open while using the website. Press Ctrl+C in the terminal to stop it.

## Demo
1. Open Students and add a student.
2. Open Companies and add a company.
3. Open Applications and connect that student to that company.
4. Return to Dashboard to see updated counts.

This is a local demonstration app. It is not deployed online and does not include login/security for public hosting.
