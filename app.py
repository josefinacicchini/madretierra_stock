from crypt import methods
from curses import flash
from flask import Flask, render_template, request, redirect, url_for, flash
from config import config
from flaskext.mysql import MySQL
from datetime import datetime
import os
from flask import send_from_directory

# Models:
from models.ModelUser import ModelUser
# Entities:
from models.entities.User import User

app = Flask(__name__, template_folder='template')

db = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('home'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/home')
def home():
	sql = "SELECT * FROM `madretierra`.`stock`;"	
	conn = db.connect()
	cursor = conn.cursor()
	cursor.execute(sql)
	stock=cursor.fetchall()
	print(stock)
	conn.commit()
	return render_template('home.html', stock=stock)

@app.route('/destroy/<int:id>')
def destroy(id): 
	conn = db.connect() 
	cursor = conn.cursor() 
	cursor.execute("DELETE FROM `madretierra`.`stock` WHERE id=%s", (id)) 
	conn.commit() 
	return redirect('/home')

@app.route('/edit/<int:id>')
def edit(id):
 conn = db.connect()
 cursor = conn.cursor()
 cursor.execute("SELECT * FROM `madretierra`.`stock` WHERE id=%s", (id))
 stock=cursor.fetchall()
 conn.commit()
 return render_template('edit.html', stock=stock)

@app.route('/update', methods=['POST'])
def update():
	_nombre=request.form['txtNombre']
	_aroma=request.form['txtAroma']
	_cantidad=request.form['txtCantidad']
	id=request.form['txtID']
	sql = "UPDATE `madretierra`.`stock` SET `Nombre_producto`=%s, `Aroma`=%s, `Cantidad`=%s WHERE id=%s;"
	datos=(_nombre,_aroma,_cantidad,id)
	conn = db.connect()
	cursor = conn.cursor()
	cursor.execute(sql,datos)
	conn.commit()
	return redirect('home')

@app.route('/create')
def create():
 return render_template('create.html')

@app.route('/store', methods=['POST'])
def storage():
	sql = "INSERT INTO `madretierra`.`stock` (`ID`, `Nombre_producto`, `Aroma`, `Cantidad`) VALUES (NULL, %s, %s, %s);"
	_nombre=request.form['txtNombre']
	_aroma=request.form['txtAroma']
	_cantidad=request.form['txtCantidad']
	if _nombre == '' or _aroma == '' or _cantidad =='':
		flash('Recuerda llenar los datos de los campos')
		return redirect(url_for('create'))
	now = datetime.now()
	tiempo = now.strftime("%Y%H%M%S")
	datos=(_nombre,_aroma,_cantidad)
	conn = db.connect()
	cursor = conn.cursor()
	cursor.execute(sql,datos)
	conn.commit()
	return redirect('home')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()

