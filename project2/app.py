from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="trial",
        password="trial@123",
        database="family"
    )

@app.route('/')
def index():
    try:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id, name FROM users")
        users = cursor.fetchall()
    except Error as e:
        flash(f'Error: {str(e)}', 'danger')
        users = []
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
    return render_template('index.html', users=users)

@app.route('/submit', methods=['POST'])
def submit():
    user_id = request.form['user_id']
    date = request.form['date']
    marks = request.form['marks']

    try:
        db = create_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO marks (user_id, date, marks) VALUES (%s, %s, %s)", (user_id, date, marks)
        )
        db.commit()
        flash('Marks successfully added!', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)