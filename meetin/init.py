from flask import Flask
from flask_login import LoginManager
import mysql.connector

from flask_wtf.csrf import CSRFProtect

login_manager = LoginManager()

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'meetin'
app.config['SECRET_KEY'] = 'Fdwjforw343nvfgjgoreqgjrq3g564SHGSH'


sql_connection = mysql.connector.MySQLConnection()
sql_connection.connect(user =  app.config['MYSQL_USER'], password = app.config['MYSQL_PASSWORD'], database = app.config['MYSQL_DB'] )
cursor = sql_connection.cursor(dictionary = True)
login_manager.init_app(app)

csrf = CSRFProtect(app)
import meetin.routes

  
    