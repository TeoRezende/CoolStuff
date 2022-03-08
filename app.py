from flask import Flask, render_template
import sqlite3
app = Flask(__name__)
DATABASE = "C:/Users/d.benseman/OneDrive - Wellington College/13DTS/Python2022/Smile/Smile.db"
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
    return render_template('menu.html')
    #connect to database
    con = create_connection(DB_NAME)
    #fetch datas from the goddamn database
    query = "SELECT name, description, volume, price, image FROM product"
    cur = con.cursor() #this does something

    cur = con.execute() #this executed the query
    product_list = cur.fetchall() #makes the list usable by python
    con.close()

    return render_template('menu.html', products = product_list)

@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')


app.run(host='0.0.0.0', debug=True)
