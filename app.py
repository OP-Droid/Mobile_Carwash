from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sqlite3
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DB_PATH = 'database.db'

# Login credentials
USERNAME = 'admin'
PASSWORD = 'carwash123'

def get_db_connection():
    return sqlite3.connect(DB_PATH)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user == USERNAME and pwd == PASSWORD:
            session['logged_in'] = True
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/login')

    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM contact")
    total_contacts = c.fetchone()[0]

    c.execute("SELECT * FROM contact ORDER BY id DESC LIMIT ? OFFSET ?", (per_page, offset))
    contacts = c.fetchall()

    c.execute("SELECT COUNT(*) FROM booking")
    total_bookings = c.fetchone()[0]

    c.execute("SELECT * FROM booking ORDER BY id DESC LIMIT ? OFFSET ?", (per_page, offset))
    bookings = c.fetchall()

    conn.close()

    return render_template('dashboard.html', contacts=contacts, bookings=bookings,
                           contact_pages=(total_contacts // per_page) + 1,
                           booking_pages=(total_bookings // per_page) + 1,
                           current_page=page)

@app.route('/delete/contact/<int:id>')
def delete_contact(id):
    if not session.get('logged_in'):
        return redirect('/login')
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM contact WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/dashboard')

@app.route('/delete/booking/<int:id>')
def delete_booking(id):
    if not session.get('logged_in'):
        return redirect('/login')
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM booking WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/dashboard')

@app.route('/download/<data_type>')
def download_data(data_type):
    conn = get_db_connection()
    df = pd.read_sql_query(f"SELECT * FROM {data_type}", conn)
    filename = f"{data_type}_data.xlsx"
    df.to_excel(filename, index=False)
    conn.close()
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
