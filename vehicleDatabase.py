import sqlite3

# Example form data
example_form_data = {
    'owner': 'TEXT NOT NULL',
    'type' : 'TEXT NOT NULL',
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

def setup_vehicle_database():
    conn = sqlite3.connect('vehicle_data.db')
    c = conn.cursor()

    # Constructing the CREATE TABLE query dynamically based on form data
    columns = ", ".join(f"{key} TEXT" for key in example_form_data.keys())
    c.execute(f"CREATE TABLE IF NOT EXISTS users ({columns})")

    conn.commit()
    conn.close()

def store_vehicle(data, user_type, username):
    name = data.get('name')
    description = data.get('description')
    remarks = data.get('remarks', '')  
    date = data.get('date')
    shift = data.get('shift')
    unit = data.get('unit','')
    smu = data.get('smu',0)
    emu=data.get('emu',0)
    quanunits=data.get('quanunits')
    charge = data.get('charge', '')  
    location = data.get('location', '')  
    nature = data.get('nature', '')  
    trips = data.get('trips', 0)  
    quantity = data.get('quantity', 0)  
    operator = data.get('operator', '')  
    start_time = data.get('start-time', '') 
    end_time = data.get('end-time', '') 
    fuel = data.get('fuel', '')
    fuel_quantity = data.get('fuel-quantity', 0)
    breakdown_details = data.get('BreakDown', '')  
    spear_parts_used = data.get('Spearparts', '')  
    mechanic = data.get('mech', '')
    brs=data.get('br-start-time','')
    bre=data.get('br-end-time','')

    conn = sqlite3.connect('vehicle_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (owner, type, name, description, date, shift,unit,smu,emu,charge,location, nature, trips, quantity,quanunits, operator, start_time, end_time, fuel, fuel_quantity, BreakDown,BreakdownStartTime,BreakdownEndTime, SpearParts, mech, remarks) VALUES (?, ?, ?,?,?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username, user_type, name, description, date, shift,unit,smu,emu, charge, location, nature, trips, quantity,quanunits, operator, start_time, end_time, fuel, fuel_quantity, breakdown_details, brs, bre, spear_parts_used, mechanic, remarks))
    conn.commit()
    conn.close()

    return True

def fetch_vehicle_data(from_date, to_date, machine_name, userType, username):
    conn = sqlite3.connect('vehicle_data.db')
    c = conn.cursor()
    if(userType == 'manager'):
        query = """
        SELECT * FROM users
        WHERE date BETWEEN ? AND ? AND name = ?"""
        c.execute(query, (from_date, to_date, machine_name))
        users = c.fetchall()  # Fetch all results
        # Close the database connection
        conn.close()
    else:
        query = """
        SELECT * FROM users 
        WHERE date BETWEEN ? AND ? AND name = ? AND owner = ?
        """
        c.execute(query, (from_date, to_date, machine_name, username))
        users = c.fetchall()  # Fetch all results
        conn.close()

    user_list = []
    shift = 2
    for user in users:
        user_data = {
            'name': user[shift+0],
            'description': user[shift+1],
            'date': user[shift+2],
            'shift': user[shift+3],
            'unit': user[shift+4],
            'smu': user[shift+5],
            'emu': user[shift+6],
            'charge': user[shift+7],
            'location': user[shift+8],
            'nature': user[shift+9],
            'trips': user[shift+10],
            'quantity': user[shift+11],
            'quanunits': user[shift+12],
            'operator': user[shift+13],
            'start_time': user[shift+14],
            'end_time': user[shift+15],
            'fuel': user[shift+16],
            'fuel_quantity': user[shift+17],
            'BreakDown': user[shift+18],
            'SpearParts': user[shift+21],
            'mech': user[shift+22],
            'remarks': user[shift+23],
            'working_hours': int(user[shift+6]) - int(user[shift+5]),
            'breakdown_start': user[shift+19],
            'breakdown_end': user[shift+20]
        }
        user_list.append(user_data)
    return user_list
