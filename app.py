from flask import Flask, render_template
import sqlite3
app = Flask(__name__)
DATABASE = "C:/Users/d.banseman/OneDrive - Wellingaton College/13DTS/Python2022/Smile/Smile.db"

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


@app.route('/contact')
def render_contact_page():
    return render_template('contact.html')


app.run(host='0.0.0.0', debug=True)
