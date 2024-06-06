from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import json
import sqlite3
import urllib.parse


def create_table(form_data):
    conn = sqlite3.connect('vehicle_data.db')
    c = conn.cursor()

    # Constructing the CREATE TABLE query dynamically based on form data
    columns = ", ".join(f"{key} TEXT" for key in form_data.keys())
    c.execute(f"CREATE TABLE IF NOT EXISTS users ({columns})")

    conn.commit()
    conn.close()

# Example form data
example_form_data = {
    'name': 'TEXT NOT NULL',
    'description': 'TEXT',
    'date': 'TEXT NOT NULL',
    'shift': 'TEXT NOT NULL',
    'unit': 'TEXT NOT NULL',
    'smu': 'TEXT NOT NULL',
    'emu': 'TEXT NOT NULL',
    'charge': 'TEXT',  
    'location': 'TEXT NOT NULL',
    'nature': 'TEXT NOT NULL',
    'trips': 'TEXT',  
    'quantity': 'TEXT',  
    'quanunits': 'TEXT',
    'operator': 'TEXT',
    'start_time': 'TEXT',
    'end_time': 'TEXT',
    'fuel': 'TEXT',
    'fuel_quantity': 'TEXT',  
    'BreakDown': 'TEXT',
    'BreakdownStartTime':'TEXT',
    'BreakdownEndTime':'TEXT',
    'Spearparts': 'TEXT',
    'mech': 'TEXT',
    'remarks': 'TEXT',  
}


create_table(example_form_data)

app = Flask(__name__)
@app.route('/')
def home():
    return(render_template('home.html'))
@app.route('/get_report')
def report():
    return(render_template('get_report.html'))
@app.route('/entry', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        remarks = request.form.get('remarks', '')  
        date = request.form.get('date')
        shift = request.form.get('shift')
        unit = request.form.get('unit','')
        smu = request.form.get('smu',0)
        emu=request.form.get('emu',0)
        quanunits=request.form.get('quanunits')
        charge = request.form.get('charge', '')  
        location = request.form.get('location', '')  
        nature = request.form.get('nature', '')  
        trips = request.form.get('trips', 0)  
        quantity = request.form.get('quantity', 0)  
        operator = request.form.get('operator', '')  
        start_time = request.form.get('start-time', '') 
        end_time = request.form.get('end-time', '') 
        fuel = request.form.get('fuel', '')
        fuel_quantity = request.form.get('fuel-quantity', 0)
        breakdown_details = request.form.get('BreakDown', '')  
        spear_parts_used = request.form.get('Spearparts', '')  
        mechanic = request.form.get('mech', '')
        brs=request.form.get('br-start-time','')
        bre=request.form.get('br-end-time','')

        conn = sqlite3.connect('vehicle_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, description, date, shift,unit,smu,emu,charge,location, nature, trips, quantity,quanunits, operator, start_time, end_time, fuel, fuel_quantity, BreakDown,BreakdownStartTime,BreakdownEndTime, SpearParts, mech, remarks) VALUES (?,?,?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, description, date, shift,unit,smu,emu, charge, location, nature, trips, quantity,quanunits, operator, start_time, end_time, fuel, fuel_quantity, breakdown_details, brs, bre, spear_parts_used, mechanic, remarks))
        conn.commit()
        conn.close()
        
        return redirect(url_for('user_details', name=urllib.parse.quote(name), date=date, shift=shift))    
    return render_template('index.html')


@app.route('/user/<name>&<date>&<shift>')
def user_details(name, date, shift):
    name = urllib.parse.unquote(name)
    print(name)
    # read the users.txt file and find the user with the matching email
      # Connect to the database
    conn = sqlite3.connect('vehicle_data.db')
    c = conn.cursor()

    # Query the database to fetch user details by name
    c.execute("SELECT * FROM users WHERE name=? AND date=? AND shift=?", (name, date, shift))
    user = c.fetchone()  # Fetch the first result
    # Close the database connection
    conn.close()
    user_list=[]

    # Check if user exists
    if user:
        user_data = {
            'name': user[0],
            'description': user[1],
            'date': user[2],
            'shift': user[3],
            'unit':user[4],
            'smu':user[5],
            'emu':user[6],
            'charge': user[7],
            'location': user[8],
            'nature': user[9],
            'trips': user[10],
            'quantity': user[11],
            'quanunits': user[12],
            'operator': user[13],
            'start_time': user[14],
            'end_time': user[15],
            'fuel': user[16],
            'fuel_quantity': user[17],
            'BreakDown': user[18],
            'SpearParts': user[21],
            'mech': user[22],
            'remarks': user[23],
            'working_hours':int(user[6])-int(user[5]),
            'breakdown_start':user[19],
            'breakdown_end':user[20]
        }
        user_list.append(user_data)

        return render_template('user_details.html', users=user_list)
    else:
        # User not found, return 404
        abort(404)

@app.route('/users', methods=['GET'])
def all_users():
    # Connect to the database
    conn = sqlite3.connect('vehicle_data.db')
    c = conn.cursor()

    # Query the database to fetch all users
    c.execute("SELECT * FROM users")
    users = c.fetchall()  # Fetch all results

    # Close the database connection
    conn.close()

    # Convert the fetched data into a list of dictionaries
    user_list = []
    for user in users:
        user_data = {
            'name': user[0],
            'description': user[1],
            'date': user[2],
            'shift': user[3],
            'unit':user[4],
            'smu':user[5],
            'emu':user[6],
            'charge': user[7],
            'location': user[8],
            'nature': user[9],
            'trips': user[10],
            'quantity': user[11],
            'quanunits': user[12],
            'operator': user[13],
            'start_time': user[14],
            'end_time': user[15],
            'fuel': user[16],
            'fuel_quantity': user[17],
            'BreakDown': user[18],
            'SpearParts': user[21],
            'mech': user[22],
            'remarks': user[23],
            'working_hours':int(user[6])-int(user[5]),
            'breakdown_start':user[19],
            'breakdown_end':user[20]
        }
        user_list.append(user_data)

    # Return all users in JSON format
    return render_template('user_details.html', users=user_list)


if __name__ == '__main__':
    app.run(debug=True)
