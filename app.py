from flask import Flask, render_template
import sqlite3
from sqlite3 import Error
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




@app.route('/')
def render_homepage():
    return render_template('home.html')


@app.route('/menu')
def render_menu_page():

    #connect to database
    con = create_connection(DATABASE)
    #fetch datas from the goddamn database
    query = "SELECT name, description, volume, price, image FROM product"
    cur = con.cursor() #this does something I don't know
    print("connected")
    cur.execute(query) #this executed the query
    product_list = cur.fetchall() #makes the list usable by python
    con.close()
    print(product_list)
    return render_template('menu.html', products=product_list)

@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')


app.run(host='0.0.0.0', debug=True)
