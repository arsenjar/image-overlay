import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

# 1. Database Setup
# The database connection function ensures a new connection 
# is made for each request (best practice in Flask)
def get_db_connection():
    # Connect to the database file
    con = sqlite3.connect("login.db")
    # Allows accessing columns by name
    con.row_factory = sqlite3.Row
    return con

# Initialize database and table (This runs when the script starts)
def init_db():
    con = get_db_connection()
    cur = con.cursor()
    # Create the table if it doesn't exist. 
    # Using PRIMARY KEY and NOT NULL ensures data integrity.
    cur.execute('''
        CREATE TABLE IF NOT EXISTS loginData (
            username TEXT PRIMARY KEY NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    con.commit()
    con.close()

# Initialize the database when the script runs
init_db()

# 2. Flask Application Setup
app = Flask(__name__)
# A secret key is required to use sessions
app.secret_key = 'a_super_secret_key_for_session' 

# Route for the main login page
@app.route('/', methods=['GET'])
def index():
    # Render the HTML template
    return render_template('login.html', message=request.args.get('message'))

# Route to handle the form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    con = get_db_connection()
    cur = con.cursor()
    
    # 3. Check if the user exists
    user = cur.execute('SELECT * FROM loginData WHERE username = ?', (username,)).fetchone()
    
    if user:
        # User exists, check password
        db_password = user['password']
        if password == db_password:
            # Successful login
            session['logged_in'] = True
            session['username'] = username
            con.close()
            # Redirect to a success page
            return redirect(url_for('success'))
        else:
            # Incorrect password
            con.close()
            message = "Incorrect password for existing user."
            return redirect(url_for('index', message=message))
    else:
        # 4. User does NOT exist, create the account
        try:
            cur.execute('INSERT INTO loginData (username, password) VALUES (?, ?)', (username, password))
            con.commit()
            session['logged_in'] = True
            session['username'] = username
            con.close()
            # Account created and logged in
            return redirect(url_for('success'))
        except sqlite3.IntegrityError:
            # Should not happen with the current logic, but good for robustness
            con.close()
            message = "Error creating account."
            return redirect(url_for('index', message=message))


# 5. Simple Success Page
@app.route('/success')
def success():
    if 'logged_in' in session and session['logged_in']:
        # This is the page the user sees after successful login/registration
        return redirect(url_for('gui'))
    else:
        # If they try to access directly without logging in
        return redirect(url_for('index', message="Please log in first."))

# 6. Logout Route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index', message="You have been logged out."))

@app.route('/gui')
def gui():
    if session.get('logged_in'):
        return render_template('gui.html', username = session.get("username"))
    else:
        return redirect(url_for("index", message = "Log in first."))

# Run the app
if __name__ == '__main__':
    # Setting debug=True is useful during development
    app.run(debug=True)
