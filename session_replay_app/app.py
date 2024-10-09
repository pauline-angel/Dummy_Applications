from flask import Flask, request, redirect, url_for, render_template_string, make_response

app = Flask(__name__)

# Dummy user data
users = {'user1': 'password1'}

# Login page template
login_page = '''
    <h2>Login</h2>
    <form method="POST" action="/login">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <p>{{ error }}</p>
'''

# Internal page template
internal_page = '''
    <h2>Internal Page</h2>
    <p>Welcome, you have accessed the internal page!</p>
    <a href="/logout">Logout</a>
'''

# Home route
@app.route('/')
def home():
    session_id = request.cookies.get('session_id')
    if session_id:
        return redirect(url_for('internal'))
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session_id = 'sessionid-' + username
            response = make_response(redirect(url_for('internal')))
            response.set_cookie('session_id', session_id)
            return response
        else:
            return render_template_string(login_page, error="Invalid credentials")
    
    return render_template_string(login_page, error="")

# Internal route
@app.route('/internal')
def internal():
    session_id = request.cookies.get('session_id')
    if session_id:
        return render_template_string(internal_page)
    return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session_id', '', expires=0)  # Delete the cookie
    return response

if __name__ == '__main__':
    app.run(debug=True)
