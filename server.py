from flask import Flask, render_template, request, redirect
from database import *
from vehicleDatabase import *

app = Flask(__name__)
app.secret_key = 'supersecretkey'

setup_databases()
setup_vehicle_database()

@app.route('/')
def root_dir():
    return redirect('http://localhost:5000/register')

@app.route('/register', methods=['GET', 'POST'])
def registration():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        designation = request.form['designation']
        print("[-] Registration :", username, "|", password)

        store_sql(username, password, designation)

        print("---Stored Successfully---")

        return redirect('http://localhost:5000/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']

        userType = verify_sql(username, password)
        if(userType == "Incorrect Credentials"):
            return render_template('login.html', msg="invalid")
        else:
            url = "http://localhost:5000/home/"+ userType + "/" + username
            return redirect(url)
    return render_template('login.html')

@app.route('/home/<userType>/<username>', methods = ['GET'])
def home_page(userType, username):
    return render_template('home.html', username=username, userType=userType)

@app.route('/enter/<userType>/<username>', methods = ['GET', 'POST'])
def enter_page(userType, username):
    if(request.method == 'GET'):
        return render_template('index.html', username=username, userType=userType)
    # Now its a post method
    # Here we need to store the data of the user in SQL
    if(store_vehicle(request.form, userType, username)):
        return render_template('index.html', username=username, userType=userType)
    return render_template('index.html', username=username, userType=userType)

@app.route('/report/<userType>/<username>')
def report_page(userType, username):
    return render_template('getreport.html', userType=userType, username=username)

@app.route('/submit_dates/<userType>/<username>', methods=['GET'])
def submit_dates(userType, username):
    from_date = request.args.get('from-date')
    to_date = request.args.get('to-date')
    machine_name = request.args.get('machine-name')

    list_dict_data = fetch_vehicle_data(from_date, to_date, machine_name, userType, username)
    return render_template('user_details.html', users = list_dict_data, userType=userType, username=username)

if __name__ == '__main__':
    app.run(debug=True)