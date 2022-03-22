from flask import Flask, render_template, request, session, redirect
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt
from datetime import datetime
app = Flask(__name__)
app.secret_key = "a47n59fdjkr932jnegslq03nswor04923kr41rf"
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
    if request.method == 'POST':
        print(request.form)
        fname = request.form.get("fname").title() #I'm not using the .strip() function for the names because my name contains spaces.
        lname = request.form.get("lname").title()
        email = request.form.get("email").strip().lower()
        pword = request.form.get("pword")
        pword2 = request.form.get("pword2")

        if pword != pword2:
            return redirect("/signup?error=Passwords+don't+match")

        if len(pword) < 8:
            return redirect("/signup?error=Password+must+have+more+than+8+characters")

        if len(pword) > 2000:
            return redirect("/signup?error=Password+cannot+be+more+than+2000+characters")

        con = create_connection(DATABASE)

        query = "INSERT INTO customer(id, fname, lname, email, pword) VALUES(NULL,?,?,?,?)"

        cur = con.cursor()
        try:
            cur.execute(query, (fname, lname, email, pword))
        except sqlite3.IntegrityError:
            return redirect('/signup?error=Email+is+already+in+use')
        con.commit()
        con.close()
        return redirect('/login')

    return render_template('signup.html')

#login
@app.route('/login', methods=["GET", "POST"])
def render_login_page():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        pword = request.form['pword'].strip()

        query = """SELECT id, fname, lname, pword FROM customer WHERE email = ?"""
        con = create_connection(DATABASE)
        cur = con.cursor()
        cur.execute(query, (email,))
        user_data = cur.fetchall()
        con.close()

        try:
            userid = user_data[0][0]
            firstname = user_data[0][1]
            lastname = user_data[0][2]
            password = user_data[0][3]
        except IndexError:
            print("eee")
            return redirect("/login?error=Email+invalid+or+password+incorrect")

        #checking if the password is valid
        if password != pword:
            return redirect("/login?error=Email+invalid+or+password+incorrect")

        session['email'] = email
        session["userid"] = userid
        session["fname"] = firstname
        session['lname'] = lastname
        print(session)
        return redirect('/')
    #redirects to the page but has now set the logged_in variable to 1
    return render_template('login.html', logged_in=1)

@app.route('/logout')
def logout():
    print('nutz')
app.run(host='0.0.0.0', debug=True)
