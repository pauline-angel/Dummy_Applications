from flask import Flask, request, redirect, url_for, render_template_string, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Dummy user data
users = {
    "admin": {"username": "admin", "password": "adminpass", "privilege": "admin"},
    "user1": {"username": "user1", "password": "user1pass", "privilege": "user1"},
    "user2": {"username": "user2", "password": "user2pass", "privilege": "user2"}
}

# Dummy details for users
user_details = {
    "user1": {"name": "User One", "account_number": "1234567890", "transactions": ["$100", "$200"]},
    "user2": {"name": "User Two", "account_number": "9876543210", "transactions": ["$50", "$150"]}
}

# Login page template
login_page = '''
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Login Page</h2>
    <form method="post" action="{{ url_for('login') }}">
        <label for="uid">Username:</label>
        <input type="text" id="uid" name="uid" required><br>
        <label for="passw">Password:</label>
        <input type="password" id="passw" name="passw" required><br>
        <input type="submit" id="login" name="login" value="Login">
    </form>
</body>
</html>
'''

# User and admin pages templates
user1_page = '''
<!DOCTYPE html>
<html>
<head><title>User Dashboard</title></head>
<body>
    <h2>Welcome, {{ name }}</h2>
    <p>Account Number: {{ account_number }}</p>
    <p>Transactions: {{ transactions }}</p>
    <a href="{{ url_for('logout') }}">Logout</a>
</body>
</html>
'''

user2_page = '''
<!DOCTYPE html>
<html>
<head><title>User Dashboard</title></head>
<body>
    <h2>Welcome, {{ name }}</h2>
    <p>Account Number: {{ account_number }}</p>
    <p>Transactions: {{ transactions }}</p>
    <a href="{{ url_for('logout') }}">Logout</a>
</body>
</html>
'''

admin_page = '''
<!DOCTYPE html>
<html>
<head><title>Admin Dashboard</title></head>
<body>
    <h2>Admin Dashboard</h2>
    <p>Below are the user details:</p>
    <ul>
        {% for user, details in user_details.items() %}
        <li>{{ details['name'] }} - Account: {{ details['account_number'] }}, Transactions: {{ details['transactions'] }}</li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('logout') }}">Logout</a>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['uid']
        password = request.form['passw']
        
        # Validate user credentials
        for user_id, user in users.items():
            if user['username'] == username and user['password'] == password:
                # Store user in session
                session['user_id'] = user_id
                # Redirect to the respective user/admin page after login
                return redirect(url_for('dashboard', user_id=user_id))
        
        # Invalid credentials, reload login page
        return render_template_string(login_page)
    
    return render_template_string(login_page)

@app.route('/dashboard/<user_id>', methods=['GET'])
def dashboard(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Fetch the logged-in user
    logged_in_user_id = session['user_id']
    
    # Authorization Bypass Logic
    if logged_in_user_id == user_id:
        # Access their own profile
        if logged_in_user_id == 'user1':
            details = user_details.get('user1', {})
            return render_template_string(user1_page, **details)
        elif logged_in_user_id == 'user2':
            details = user_details.get('user2', {})
            return render_template_string(user2_page, **details)
        elif logged_in_user_id == 'admin':
            return render_template_string(admin_page, user_details=user_details)
    
    # Access control for User 1 to access Admin profile
    if logged_in_user_id == 'user1' and user_id == 'admin':
        return render_template_string(admin_page, user_details=user_details)
    
    # Access control for User 2 to access User 1 profile
    if logged_in_user_id == 'user2' and user_id == 'user1':
        details = user_details.get('user1', {})
        return render_template_string(user1_page, **details)
    
    # Access control for Admin to access User 1 and User 2 profiles
    if logged_in_user_id == 'admin':
        if user_id == 'user1':
            details = user_details.get('user1', {})
            return render_template_string(user1_page, **details)
        elif user_id == 'user2':
            details = user_details.get('user2', {})
            return render_template_string(user2_page, **details)
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
