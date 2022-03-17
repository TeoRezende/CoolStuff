from flask import Flask, render_template, request, session, redirect
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt
from datetime import datetime
app = Flask(__name__)
DATABASE = "C:/Users/18126/Documents/Smile/smile.db"
#test
def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None



#homepage
@app.route('/')
def render_homepage():
    return render_template('home.html')

@app.route('/addtocart/<productid>')
def addtocart(productid):
    userid = session['userid']
    timestamp = datetime.now()
    print("User {} would like to add {} to cart at {}".format(userid, productid, timestamp))

    query = 'INSERT INTO cart(id, userid, productid, timestamp) VALUES(NULL,?,?,?,?)'
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (userid, productid, timestamp))
    con.commit()
    con.close()
    return redirect(request.referrer)

#menu
@app.route('/menu')
def render_menu_page():

    #connect to database
    con = create_connection(DATABASE)
    #fetch datas from the goddamn database
    query = "SELECT name, description, volume, price, image, id FROM product"
    cur = con.cursor() #this does something I don't know
    print("connected")
    cur.execute(query) #this executed the query
    product_list = cur.fetchall() #makes the list usable by python
    con.close()
    print(product_list)
    return render_template('menu.html', products=product_list)

#contact
@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')

#Signup
@app.route('/signup', methods=['GET', 'POST'])
def render_signup_page():
    print(request.form)
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    pword = request.form.get("pword")
    pword2 = request.form.get("pword2")

    con = create_connection(DATABASE)

    query = "INSERT INTO customer(id, fname, lname, email, pword) VALUES(NULL,?,?,?,?)"

    cur = con.cursor()
    cur.execute(query, (fname, lname, email, pword))
    con.commit()
    con.close()

    return render_template('signup.html')

#login
@app.route('/login', methods=["GET", "POST"])
def render_login_page():
    return render_template('login.html')

app.run(host='0.0.0.0', debug=True)
