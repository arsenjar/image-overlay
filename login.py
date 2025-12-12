import sqlite3

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

def login(username, password):
    con = get_db_connection()
    cur = con.cursor()
    
    # 3. Check if the user exists
    user = cur.execute('SELECT * FROM loginData WHERE username = ?', (username,)).fetchone()
    
    if user:
        # User exists, check password
        db_password = user['password']
        if password == db_password:
            # Successful login
            con.close()
            # Redirect to a success page
            return True, False, "Login successful"
        else:
            # Incorrect password
            con.close()
            return False, False, "Login unsuccessful"
    else:
        # 4. User does NOT exist, create the account
        try:
            cur.execute('INSERT INTO loginData (username, password) VALUES (?, ?)', (username, password))
            con.commit()
            con.close()
            # Account created and logged in
            return True, True, "made account"
        except sqlite3.IntegrityError:
            # Should not happen with the current logic, but good for robustness
            con.close()
            return False, False, "did not made account"
