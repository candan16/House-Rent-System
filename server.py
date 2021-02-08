from flask import Flask, render_template, url_for, flash, redirect, request, session
# from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pymysql
import re
from flask_bootstrap import Bootstrap

app = Flask(__name__)

# Configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123*'
app.config['MYSQL_DB'] = 'housedb'

mysql = MySQL(app)

app.config['SECRET_KEY'] = '00e55ed4ed72e9d974345bba31cc8061'


posts = [
    {
        'author': 'Merve Candan',
        'title': 'Daily Rent at Izmir',
        'content': 'Houses',
        'date_posted': 'November 5, 2020'
    },
    {
        'author': 'Fatih Akcaalan',
        'title': 'Sale at Istanbul',
        'content': 'Houses 2',
        'date_posted': 'November 7, 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():

    # cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM user")
    # fetchdata = cur.fetchall()
    # print(fetchdata)
    # print("Done")
    # cur.close()

    # mysql.connect.commit()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # form = RegistrationForm()
    # return "Merve"
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'phone_num' in request.form and 'birt_date' in request.form:
        user_type = request.form['user_type']
        name = request.form['name']
        email = request.form['email']
        phone_num = request.form['phone_num']
        birt_date = request.form['birt_date']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE name = %s', (name,))
        profile = cursor.fetchone()
        if profile:
            message = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', name):
            message = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user (user_type,name,email, phone_num, birt_date, password, confirm_password) VALUES (NULL, %s, % s, % s, % s, % s, % s, % s)', (user_type,name, email, phone_num, birt_date, password, confirm_password, ))
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('register.html')

   # if form.validate_on_submit():
    #    flash('Account created for {form.name.data}!', 'success')
     #   cur.execute("INSERT INTO user (name, email, phone_num) VALUES (%s, %s, %s)", (name,email,phone))
      #  return redirect(url_for('home'))

@app.route("/login", methods = ['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        profile = cursor.fetchone()
        if profile:
            session['loggedin'] = True
            session['email'] = profile['email']
            session['password'] = profile['password']
            message = 'Logged in successfully !'
            return render_template('home.html', msg = message)
        else:
            message = 'Incorrect username / password !'
    return render_template('login.html', msg = message) 



    # form = LoginForm()
    # if form.validate_on_submit():
    #    if form.email.data == 'admin@blog.com' and form.password.data == 'password':
    #        flash('You have been logged in!', 'success')
    #        return redirect(url_for('home'))
    #    else:
    #        flash('login Unsuccessful. Please check username and password', 'danger')
    # return render_template('login.html', title = 'Login', form = form)

if __name__ == '__main__':
    app.run(debug = True)
