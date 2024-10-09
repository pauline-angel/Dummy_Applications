from flask import Flask, request, redirect, url_for, session, render_template_string
from flask_session import Session
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with your own secret key

# Configure session to use filesystem (can use other backends too)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Store user sessions
user_sessions = {}

@app.route('/')
def index():
    if 'username' in session:
        return f"Hello, {session['username']}! <a href='/logout'>Logout</a>"
    return render_template_string('''
        <h1>Login</h1>
        <form action="/login" method="post">
            Username: <input type="text" name="username">
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']

    # Check if user is already logged in
    if username in user_sessions and user_sessions[username] != session.sid:
        return "User already logged in elsewhere. Please logout from the other session."

    # Store user session ID
    user_sessions[username] = session.sid
    session['username'] = username
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    username = session.get('username')
    if username in user_sessions:
        del user_sessions[username]
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
