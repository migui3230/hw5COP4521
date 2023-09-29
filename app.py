"""
Name:Miguel Sarenas
Date:09/18/2023
Assignment:Module4:Basic Flask Website
Due Date:09/24/2023
About this project: this program shows how to create a simple flask website with add user, list users, and results pages
Assumptions: sample data
All work below was performed by Miguel Sarenas
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# function to validate user input


def validate_input(name, age, phone_number, security_role_level, login_password):
    errors = []
    if not name.strip():
        errors.append("Name cannot be empty or only contain spaces.")
    if not (age.isdigit() and 0 < int(age) < 121):
        errors.append("Age must be a whole number between 1 and 120.")
    if not phone_number.strip():
        errors.append("Phone number cannot be empty or only contain spaces.")
    if not (security_role_level.isdigit() and 1 <= int(security_role_level) <= 3):
        errors.append("Security role level must be a number between 1 and 3.")
    if not login_password.strip():
        errors.append("Login password cannot be empty or only contain spaces.")

    return errors

# route to home page


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/home', methods=['POST'])
def home():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('hospital_user.db')
    c = conn.cursor()

    c.execute("SELECT * FROM HospitalUser WHERE name=? AND login_password=?",
              (username, password))
    user = c.fetchone()

    if user:
        session['username'] = username
        return render_template('home.html')
    else:
        flash('Invalid username and/or password!')
        return redirect('/')

# route to add user page and add user to database


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    msg = ""
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone_number = request.form['phone_number']
        has_covid = 'has_covid' in request.form
        security_role_level = request.form['security_role_level']
        login_password = request.form['login_password']

        errors = validate_input(name, age, phone_number,
                                security_role_level, login_password)

        # error handling
        if errors:
            msg = "Error: " + ", ".join(errors)
        else:
            conn = sqlite3.connect('hospital_user.db')
            c = conn.cursor()
            c.execute("INSERT INTO HospitalUser (name, age, phone_number, has_covid, security_role_level, login_password) VALUES (?, ?, ?, ?, ?, ?)",
                      (name, age, phone_number, has_covid, security_role_level, login_password))
            conn.commit()
            conn.close()
            msg = "Record added successfully"

        return redirect(url_for('results', msg=msg))

    return render_template('add_user.html')

# route to list users page


@app.route('/list_users')
def list_users():
    conn = sqlite3.connect('hospital_user.db')
    c = conn.cursor()
    c.execute(
        "SELECT name, age, phone_number, has_covid, security_role_level, login_password FROM HospitalUser")
    users = c.fetchall()
    conn.close()

    return render_template('list_users.html', users=users)

# route to results page


@app.route('/results')
def results():
    msg = request.args.get('msg')
    return render_template('results.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
