import sqlite3

file_name = "accounts.db"

def setup_databases():
    '''
    This Will creates an Accounts Database file
    and adds a table named Accounts : 
    _______________________________________________
    |  id  |  username  |  password  |  userType  |
    | INT  |    TEXT    |    TEXT    |    TEXT    |
    ===============================================
    '''
    conn = sqlite3.connect(file_name)
    curr = conn.cursor()

    sql_create_command = """CREATE TABLE IF NOT EXISTS accounts (
                            id integer PRIMARY KEY,
                            username text NOT NULL,
                            password text NOT NULL,
                            userType text NOT NULL
                        );"""
    curr.execute(sql_create_command)
    conn.commit()
    conn.close()

def Search_username(username):
    # Perform Search Operations
    conn = sqlite3.connect(file_name)
    sql_search_command = """SELECT * FROM accounts WHERE username=?"""
    curr = conn.cursor()
    curr.execute(sql_search_command, (username, ))
    rows = curr.fetchall()
    conn.close()
    if(not rows):
        return True
    return False

def add_details(username, password, designation):
    # Perform Insert Operation
    conn = sqlite3.connect(file_name)
    sql_insert_command = """INSERT INTO accounts(username, password, userType)
                            VALUES (?, ?, ?);"""
    curr = conn.cursor()
    curr.execute(sql_insert_command, (username, password, designation))
    conn.commit()
    conn.close()
    return True

def store_sql(username, password, designation):
    # Search the username whether already exists ?
    # if yes return False
    # Else Add the user and return True

    if Search_username(username) :
        # User Does Not Exist
        # Now We need to add the Username
        add_details(username, password, designation)
        # Added Successfully
    else:
        print("[-] Username already exists")
    return True

def verify_sql(username, password):
    # Verify User and retrive type
    conn = sqlite3.connect('accounts.db')
    curr = conn.cursor()
    sql_search_command = """SELECT * FROM accounts WHERE username=? AND password=?"""
    curr.execute(sql_search_command, (username, password))
    rows = curr.fetchall()
    print(rows)
    if(rows):
        # rows list in not empty
        user = rows[0][3]
        return user
    return "Incorrect Credentials"