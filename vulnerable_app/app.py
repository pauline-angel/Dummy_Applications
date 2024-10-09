from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Hardcoded secret key

# Database setup (not secure)
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Basic SQL Injection vulnerability
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('user_form'))
        else:
            flash('Invalid credentials. Try admin:admin123 for login.')
    return render_template('login.html')

@app.route('/form', methods=['GET', 'POST'])
def user_form():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        phone = request.form['phone']

        # Display submitted data (potential XSS vulnerability)
        flash(f'Submitted Data: Name={name}, Age={age}, Email={email}, Phone={phone}')
        return redirect(url_for('user_form'))

    return render_template('form.html')

@app.route('/admin')
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Display admin page
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
