import functools
import os
from re import X

from flask import Flask, render_template, flash, current_app
from flask import redirect, request, url_for, session, g
from flask.templating import render_template_string
from datetime import datetime

import utils
from db import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash

from config import dev
import forms

app = Flask(__name__)
app.config.from_object(dev)
app.secret_key = os.urandom(24)

usuarios = ("SADMIN", "ADMIN", "USER")

sesion_iniciada = (False, None, None)     #sesion_iniciada = False
usuario = None
rol_uact = None


@app.route("/", methods=["GET", "POST"])
@app.route("/inicio", methods=["GET", "POST"])
def inicio():
    if g.user:  
        # si ya inicio sesion
        # chequear el perfil
        # segun el perfil lo envia a la pagina segun Mapa de Navegabilidad
        sql = "Select * from productos;"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql)
        productos = cursor.fetchall()
        print(productos)
        close_db()
        return render_template("home.html", sesion_iniciada=sesion_iniciada, productos=productos, usuario=g.user)
    else:
        return render_template('index.html', sesion_iniciada=sesion_iniciada, usuario=g.user)


@app.route("/login", methods=["GET", "POST"])
def login():
    global sesion_iniciada, usuario, rol_uact
    login_form = forms.LoginForm(request.form)

    try:
        if g.user:
            return redirect(url_for('inicio'))

        if request.method == 'POST':
            db = get_db()
            error = None
            username = request.form['usuario']
            password = request.form['password']
            passhasheado = generate_password_hash(password)
            if not username:
                error = 'Debes ingresar el usuario'
                flash(error, 'error')
                return render_template('login.html')

            if not password:
                error = 'Contraseña requerida'
                flash(error,'error')
                return render_template('login.html')

            user = db.execute(
                'SELECT * FROM usuarios WHERE codigo_usuario = ? AND password = ?', (
                    username, passhasheado)
            ).fetchone()
            if user is None:
                user = db.execute(
                    "SELECT * FROM usuarios WHERE codigo_usuario = ?", (username,)
                ).fetchone()
                if user is None:
                    error = 'Usuario no existe'
                else:
                    # Validar contraseña hash
                    # campo password de la tabla usuarios
                    store_password = user[7]
                    result = check_password_hash(store_password, password)
                    if result is False:
                        error = 'Contraseña inválida'
                    else:
                        session.clear()
                        # campo codigo_usuario de la tabla usuarios
                        session['user_id'] = user[1]
                        sesion_iniciada = (True, session['user_id'], user[6])    
                        #sesion iniciada = True
                        usuario = session['user_id']
                        rol_uact = user[6]
                        return redirect(url_for('inicio'))
                flash(error)
            else:
                session.clear()
                # campo codigo_usuario de la tabla usuarios
                session['user_id'] = user[1]
                if usuario == "SUPERADMIN":
                    return "Pagina de Super Administrador"
                elif usuario == "ADMIN":
                    return render_template("home.html")
                elif usuario == "USER":
                    return redirect(url_for('inicio'))
            flash(error)
            close_db()
        return render_template("login.html", form=login_form, sesion_iniciada=sesion_iniciada)
    except Exception as e:
        print(e)
        return render_template("login.html", form=login_form, sesion_iniciada=sesion_iniciada)


@app.route("/salir", methods=["POST"])
def salir():
    global sesion_iniciada
    sesion_iniciada = (False, None, None)     #sesion_iniciada = False
    g.user = None
    session.clear()
    return redirect(url_for('inicio'))


@app.route("/cancelar", methods=["POST"])
def cancelar():
    global sesion_iniciada
    # sesion iniciada = False
    return redirect(url_for('inicio'))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    # si ya inicio sesion
    # chequear el perfil
    # segun el perfil mostrar informacion de acuerdo a él.
    return "Dashboard con Informacion del Inventario de Autos segun Perfil"
    # render_template('index.html')


@app.route("/admin", methods=["GET", "POST"])
def admin():
    # si ya inicio sesion
    # chequear el perfil
    return render_template('admin.html')
    # "Administracion de Usuarios"


@app.route("/registro", methods=["GET", "POST"])
def registro():
    # si ya inicio sesion
    # chequear el perfil
    return render_template('registro_user.html')
    # "Administracion de Usuarios"

@app.route("/crud_fabricante", methods=["GET", "POST"])
def crud_fabricante():
    if g.user:  
        # si ya inicio sesion
        # chequear el perfil
        # segun el perfil lo envia a la pagina segun Mapa de Navegabilidad
        sql = "Select * from fabricante"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql)
        fabricantes = cursor.fetchall()
        close_db()
        return render_template("show_fab.html", sesion_iniciada=sesion_iniciada, fabricantes=fabricantes, usuario=g.user)
    else:
        return render_template('index.html', sesion_iniciada=sesion_iniciada, usuario=g.user)

@app.route('/reg_fabricante', methods=('GET', 'POST'))
def reg_fabricante():
    if g.user == None:
        return redirect(url_for('/login'))

    reg_fab_form = forms.FabricanteForm(request.form)
    try:
        if request.method == 'POST':
            cod_fab = request.form['cod_fab']
            tid_fab = request.form['tipoid_fab']
            nid_fab = request.form['nroid_fab']
            dv_fab = request.form['dv_nroid_fab']
            rsocial = request.form['rsocial_fab']
            nrep_fab = request.form['name_rep_fab']
            ncon_fab = request.form['name_con_fab']
            email = request.form['email_fab']
            cpais = request.form['codigo_pais']
            ciu_fab = request.form['ciudad']
            dir_fab = request.form['direccion']
            tel_fab = request.form['telefono']
            cel_fab = request.form['celular']
            cusuario = usuario
            error = None
            db = get_db()

            if not utils.isNroidValid(nid_fab):
                error = "El Nro. de ID del Fabricante debe ser numerico."
                print(error)
                return render_template('reg_fab.html', form=reg_fab_form, sesion_iniciada=sesion_iniciada)

            if not utils.isEmailValid(email):
                error = 'Correo invalido'
                print(error)
                return render_template('reg_fab.html', form=reg_fab_form, sesion_iniciada=sesion_iniciada)

            if db.execute('SELECT id_fabricante FROM fabricante WHERE nroid_fabricante = ?', (nid_fab,)).fetchone() is not None:
                error = 'Existe un Fabricante con ese Nro. de ID'.format(
                    nid_fab)
                print(error)
                return render_template('reg_fab.html', form=reg_fab_form, sesion_iniciada=sesion_iniciada)

            db.execute(
                '''INSERT INTO fabricante (cod_fabricante, tipoid_fabricante, nroid_fabricante, dv_nroid, razon_social_fabricante, nombre_representante,
                nombre_contacto, email_fabricante, codigo_pais, ciudad, direccion, telefono, celular, codigo_usuario) VALUES 
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (cod_fab, tid_fab, nid_fab, dv_fab, rsocial, nrep_fab, ncon_fab,
                 email, cpais, ciu_fab, dir_fab, tel_fab, cel_fab, cusuario)
            )
            db.commit()
            close_db()

            print('Fabricante Registrado correctamente')
            return redirect(url_for('crud_fabricante'))

        return render_template('reg_fab.html', form=reg_fab_form, sesion_iniciada=sesion_iniciada)
    except:
        print('ERROR- REG FABRICANTE')
        return render_template('reg_fab.html', form=reg_fab_form, sesion_iniciada=sesion_iniciada)

@app.route("/edit_fab/<int:id>", methods=["GET", "POST"])
def edit_fab(id):
    if g.user:  
        # si ya inicio sesion
        # chequear el perfil
        # segun el perfil lo envia a la pagina segun Mapa de Navegabilidad
        edit_fab_form = forms.EditFabForm(request.form)        
        if request.method == 'GET':
   
            db = get_db()
            cursor = db.cursor()
            cursor.execute("select * from fabricante where id_fabricante=?", (id,))
            fabricantes = cursor.fetchall()
            close_db()
            return render_template("edit_fab.html", form=edit_fab_form, sesion_iniciada=sesion_iniciada, fabricantes=fabricantes, usuario=g.user)
        else:
            cod_fab = request.form['cod_fab']
            tid_fab = request.form['tipoid_fab']
            nid_fab = request.form['nroid_fab']
            dv_fab = request.form['dv_nroid_fab']
            rsocial = request.form['rsocial_fab']
            nrep_fab = request.form['name_rep_fab']
            ncon_fab = request.form['name_con_fab']
            email = request.form['email_fab']
            cpais = request.form['codigo_pais']
            ciu_fab = request.form['ciudad']
            dir_fab = request.form['direccion']
            tel_fab = request.form['telefono']
            cel_fab = request.form['celular']                        

            sql = '''Update fabricante set cod_fabricante=?, tipoid_fabricante = ?, nroid_fabricante = ?,
                dv_nroid =?, razon_social_fabricante=?, nombre_representante=?, nombre_contacto=?, 
                email_fabricante=?, codigo_pais=?, ciudad=?, direccion=?, telefono=?, celular=?
                Where id_fabricante =?;'''
            datos =(cod_fab, tid_fab, nid_fab, dv_fab, rsocial, nrep_fab, ncon_fab, email, cpais, ciu_fab, dir_fab, tel_fab, cel_fab, id) 
            db = get_db()
            cursor = db.cursor()
            cursor.execute(sql, datos)
            db.commit()
            close_db()
            return redirect(url_for('crud_fabricante'))
    else:
        return render_template('index.html', sesion_iniciada=sesion_iniciada, usuario=g.user)

@app.route("/del_fab/<int:id>")
def del_fab(id):
    if g.user:  
        # si ya inicio sesion
        # chequear el perfil
        # segun el perfil lo envia a la pagina segun Mapa de Navegabilidad
        db = get_db()
        db.execute("delete from fabricante where id_fabricante=?", (id,))
        db.commit()
        close_db()
        return redirect(url_for('crud_fabricante'))
    else:
        return render_template('index.html', sesion_iniciada=sesion_iniciada, usuario=g.user)

@app.route("/crud_productos", methods=["GET", "POST"])
def crud_productos():
    if g.user:  
        # si ya inicio sesion
        # chequear el perfil
        # segun el perfil lo envia a la pagina segun Mapa de Navegabilidad
        sql = "Select * from productos"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql)
        productos = cursor.fetchall()
        close_db()
        return render_template("show_prod.html", sesion_iniciada=sesion_iniciada, productos=productos, usuario=g.user)
    else:
        return render_template('index.html', sesion_iniciada=sesion_iniciada, usuario=g.user)

@app.route('/reg_producto', methods=('GET', 'POST'))
def reg_producto():
    if g.user == None:
        return redirect(url_for('/login'))

    prod_fab_form = forms.ProductosForm(request.form)
    try:
        if request.method == 'POST':
            cod_prod = request.form['cod_prod']
            name_prod = request.form['name_prod']
            desc_prod = request.form['desc_prod']
            cant_min_req = request.form['cant_min_req']
            cant_disp = request.form['cant_disp']
            cusuario = usuario
            error = None
            db = get_db()

            if not utils.isNroidValid(cod_prod):
                error = "El Nro. de ID del Producto debe ser numerico."
                print(error)
                return render_template('reg_prod.html', form=prod_fab_form, sesion_iniciada=sesion_iniciada)

            if db.execute('SELECT id_producto FROM productos WHERE codigo_producto = ?', (cod_prod,)).fetchone() is not None:
                error = 'Existe un Producto con ese Codigo'.format(cod_prod)
                print(error)
                return render_template('reg_prod.html', form=prod_fab_form, sesion_iniciada=sesion_iniciada)

            db.execute(
                '''INSERT INTO Productos (codigo_producto, nombre_producto, descripcion, cminima_rq_bodega, cdisponible_bodega, codigo_usuario)
                VALUES (?,?,?,?,?,?)''',
                (cod_prod, name_prod, desc_prod, cant_min_req, cant_disp, cusuario)
            )
            db.commit()
            close_db()

            print('Producto Registrado correctamente')
            return redirect(url_for('crud_productos'))

        return render_template('reg_prod.html', form=prod_fab_form, sesion_iniciada=sesion_iniciada)
    except:
        print('ERROR- REG PRODUCTO')
        return render_template('reg_prod.html', form=prod_fab_form, sesion_iniciada=sesion_iniciada)

@app.route("/edit_prod/<int:id>", methods=["GET", "POST"])
def edit_prod(id):
    if g.user:  
        edit_prod_form = forms.ProductosForm(request.form)        
        if request.method == 'GET':
   
            db = get_db()
            cursor = db.cursor()
            cursor.execute("select * from productos where id_producto=?", (id,))
            productos = cursor.fetchall()
            close_db()
            return render_template("edit_prod.html", form=edit_prod_form, sesion_iniciada=sesion_iniciada, productos=productos, usuario=g.user)
        else:
            cod_prod = request.form['cod_prod']
            name_prod = request.form['name_prod']
            desc_prod = request.form['desc_prod']
            cant_min_req = float(request.form['cant_min_req'])
            cant_disp = float(request.form['cant_disp'])

            sql = '''Update productos set codigo_producto=?, nombre_producto=?, descripcion=?,
                cminima_rq_bodega=?, cdisponible_bodega=? Where id_producto =?;'''
            datos =(cod_prod, name_prod, desc_prod, cant_min_req, cant_disp, id) 
            db = get_db()
            cursor = db.cursor()
            cursor.execute(sql, datos)
            db.commit()
            close_db()
            return redirect(url_for('crud_productos'))
    else:
        return render_template('index.html', sesion_iniciada=sesion_iniciada, usuario=g.user)

@app.route("/del_prod/<int:id>")
def del_prod(id):
    if g.user:  
        # si ya inicio sesion
        # chequear el perfil
        # segun el perfil lo envia a la pagina segun Mapa de Navegabilidad
        db = get_db()
        db.execute("delete from productos where id_producto=?", (id,))
        db.commit()
        close_db()
        return redirect(url_for('crud_productos'))
    else:
        return render_template('index.html', sesion_iniciada=sesion_iniciada, usuario=g.user)


@app.route("/info_prod/<int:id>")
def info_prod(id):
    if g.user:  
        if request.method == 'GET':

            db = get_db()
            cursor = db.cursor()
            cursor.execute( '''select pr.codigo_producto, pr.nombre_producto, pr.descripcion, pro.codigo_proveedor, pro.razon_social_proveedor, pro.celular,
                    pro.email_proveedor, pro.direccion from productos as pr 
                    inner join produ_prov as pp on pr.id_producto= pp.id_producto
                    inner join proveedor as pro on pro.id_proveedor= pp.id_proveedor  
                    where pr.id_producto= ?; ''', (id,))
            productos = cursor.fetchall()
            close_db()
            return render_template("info_prod.html", sesion_iniciada=sesion_iniciada, productos=productos, usuario=g.user)
    else:
        return render_template('index.html', sesion_iniciada=sesion_iniciada, usuario=g.user)

@app.route("/crud_proveedor", methods=["GET", "POST"])
def crud_proveedor():
    if g.user:  
        sql = "Select * from proveedor"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql)
        proveedor = cursor.fetchall()
        close_db()
        return render_template("show_provee.html", sesion_iniciada=sesion_iniciada, proveedor=proveedor, usuario=g.user)
    else:
        return render_template('index.html', sesion_iniciada=sesion_iniciada, usuario=g.user)

@app.route( '/reg_proveedor', methods=('GET', 'POST') )
def reg_proveedor():
    if g.user==None:
        return redirect( url_for( '/login' ) )
    
    reg_prov_form = forms.ProveedoresForm(request.form)
    try:
        if request.method == 'POST':
            cod_prov = request.form['cod_prov'] 
            tipoid_prov = request.form['tipoid_prov']
            nroid_prov  = request.form['nroid_prov']
            dv_nroid_prov = request.form['dv_nroid_prov'] 
            rsocial_prov = request.form['rsocial_prov']
            name_rep_prov = request.form['name_rep_prov']
            name_con_prov = request.form['name_con_prov']
            email_prov = request.form['email_prov']
            codigo_pais = request.form['codigo_pais']
            ciudad = request.form['ciudad']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            celular = request.form['celular'] 
            cusuario = usuario
            error = None
            db = get_db()

            if not utils.isNroidValid( nroid_prov ):
                error = "El Nro. de ID del Proveedor debe ser numerico."
                print( error )
                return render_template( 'reg_proveed.html', form = reg_prov_form, sesion_iniciada=sesion_iniciada )

            if not utils.isEmailValid( email_prov ):
                error = 'Correo invalido'
                print( error )
                return render_template( 'reg_proveed.html', form = reg_prov_form, sesion_iniciada=sesion_iniciada )

            if db.execute( 'SELECT nroid_proveedor FROM proveedor WHERE nroid_proveedor = ?', (nroid_prov,) ).fetchone() is not None:
                error = 'Existe un Fabricante con ese Nro. de ID'.format( nroid_prov )
                print( error )
                return render_template( 'reg_proveed.html', form = reg_prov_form, sesion_iniciada=sesion_iniciada )

            db.execute(
                '''INSERT INTO proveedor (codigo_proveedor, tipoid_proveedor, nroid_proveedor, dv_nroid, razon_social_proveedor, nombre_representante,
                nombre_contacto, email_proveedor, codigo_pais, ciudad, direccion, telefono, celular, codigo_usuario) VALUES 
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (cod_prov, tipoid_prov, nroid_prov, dv_nroid_prov, rsocial_prov, name_rep_prov, name_con_prov, email_prov, codigo_pais, ciudad, direccion, telefono, celular, cusuario)
            )
            db.commit()
            close_db()

            print( 'Proveedor Registrado correctamente' )
            return redirect(url_for('crud_proveedor'))
        
        return render_template( 'reg_proveed.html', form = reg_prov_form, sesion_iniciada=sesion_iniciada )
    except:
        print('ERROR - REGISTRO DE PROVEEDORES')
        return render_template( 'reg_proveed.html', form = reg_prov_form, sesion_iniciada=sesion_iniciada )


@app.route("/edit_prov/<int:id>", methods=["GET", "POST"])
def edit_prov(id):
    if g.user:  
        # si ya inicio sesion
        # chequear el perfil
        # segun el perfil lo envia a la pagina segun Mapa de Navegabilidad
        edit_prov_form = forms.ProveedoresForm(request.form)        
        if request.method == 'GET':
   
            db = get_db()
            cursor = db.cursor()
            cursor.execute("select * from proveedor where id_proveedor=?", (id,))
            proveedor = cursor.fetchall()
            close_db()
            return render_template("edit_prov.html", form=edit_prov_form, sesion_iniciada=sesion_iniciada, proveedor=proveedor, usuario=g.user)
        else:
            cod_prov = request.form['cod_prov'] 
            tipoid_prov = request.form['tipoid_prov']
            nroid_prov  = request.form['nroid_prov']
            dv_nroid_prov = request.form['dv_nroid_prov'] 
            rsocial_prov = request.form['rsocial_prov']
            name_rep_prov = request.form['name_rep_prov']
            name_con_prov = request.form['name_con_prov']
            email_prov = request.form['email_prov']
            codigo_pais = request.form['codigo_pais']
            ciudad = request.form['ciudad']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            celular = request.form['celular'] 

            sql ='''Update proveedor set codigo_proveedor = ?, tipoid_proveedor = ?, nroid_proveedor = ?, dv_nroid = ?, 
                razon_social_proveedor = ?, nombre_representante = ?, nombre_contacto = ?, email_proveedor = ?, codigo_pais = ?, 
                ciudad = ?, direccion = ?, telefono = ?, celular = ? Where id_proveedor = ?;'''              

            datos=(cod_prov, tipoid_prov, nroid_prov, dv_nroid_prov, rsocial_prov, name_rep_prov, name_con_prov, email_prov, codigo_pais, ciudad, direccion, telefono, celular, id) 
            db = get_db()
            cursor = db.cursor()
            cursor.execute(sql, datos)
            db.commit()
            close_db()
            return redirect(url_for('crud_proveedor'))
    else:
        return render_template('index.html', sesion_iniciada=sesion_iniciada, usuario=g.user)


@app.route("/del_prov/<int:id>")
def del_prov(id):
    if g.user:  
        # si ya inicio sesion
        # chequear el perfil
        # segun el perfil lo envia a la pagina segun Mapa de Navegabilidad
        db = get_db()
        db.execute("delete from proveedor where id_proveedor=?", (id,))
        db.commit()
        close_db()
        return redirect(url_for('crud_proveedor'))
    else:
        return render_template('index.html', sesion_iniciada=sesion_iniciada, usuario=g.user)

@app.route("/crud_usuario", methods=["GET", "POST"])
def crud_usuario():
    if g.user:  
        # si ya inicio sesion
        # chequear el perfil
        # segun el perfil lo envia a la pagina segun Mapa de Navegabilidad
        sql = "Select * from usuarios"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql)
        cusers = cursor.fetchall()
        close_db()
        return render_template("show_users.html", sesion_iniciada=sesion_iniciada, cusers=cusers, usuario=g.user)
    else:
        return render_template('index.html', sesion_iniciada=sesion_iniciada, usuario=g.user)

@app.route('/reg_users', methods=('GET', 'POST'))
def reg_users():
    if g.user == None:
        return redirect(url_for('/login'))

    users_form = forms.RegistroUsuario(request.form)
    print(request.form)
    try:
        if request.method == 'POST':
            cod_usuario = request.form['cod_usuario']
            print(cod_usuario)
            nombre_usuario = request.form['nombre_usuario']
            email_usuario = request.form['email_usuario']
            cargo = request.form['cargo']
            foto = request.form['foto']
            codigo_rol = request.form['codigo_rol']
            password = request.form['password']
            codigo_pais = request.form['codigo_pais']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            celular = request.form['celular']
            ciudad = request.form['ciudad']
            error = None
            db = get_db()

            print(foto)

            if not utils.isNroidValid(cod_usuario):
                error = "El Nro. de ID del Usuario debe ser numerico."
                print(error)
                return render_template('reg_user.html', form=users_form, sesion_iniciada=sesion_iniciada)

            if not utils.isEmailValid(email_usuario):
                error = 'Correo invalido'
                print(error)
                return render_template('reg_user.html', form=users_form, sesion_iniciada=sesion_iniciada)

            if db.execute('SELECT codigo_usuario FROM usuarios WHERE codigo_usuario = ?', (cod_usuario,)).fetchone() is not None:
                error = 'Ya existe el Usuario: '.format( cod_usuario )
                print(error)
                return render_template('reg_user.html', form=users_form, sesion_iniciada=sesion_iniciada)
            
            passhasheado = generate_password_hash(password)

            db.execute(
                '''INSERT INTO usuarios (codigo_usuario, nombre_usuario, email_usuario, cargo, foto, codigo_rol, 
                password, codigo_pais, direccion, telefono, celular, ciudad) VALUES 
                (?,?,?,?,?,?,?,?,?,?,?,?)''',
                (cod_usuario, nombre_usuario, email_usuario, cargo, foto, codigo_rol, passhasheado, codigo_pais,
                    direccion, telefono, celular, ciudad)
            )
            db.commit()
            close_db()

            print('Usuario Registrado correctamente')
            return redirect(url_for('crud_usuario'))

        return render_template('reg_user.html', form=users_form, sesion_iniciada=sesion_iniciada)
    except:
        print('ERROR- REG USUARIO')
        return render_template('reg_user.html', form=users_form, sesion_iniciada=sesion_iniciada)


@app.route("/ayuda", methods=["GET"])
def ayuda():
    # si ya inicio sesion
    # chequear el perfil
    return render_template('config.html')
    # Ayuda en General con aceso a Videos.
    # render_template('ayuda.html')


@app.before_request  # Decorador
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM usuarios WHERE codigo_usuario = ?', (user_id,)
        ).fetchone()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))


@app.errorhandler(404)
def page_not_found(error):
    return "Pagina No Encontrada ... ", 404


if __name__ == '__main__':  # Cuando este corriendo de modo principal debe subir el servidor
    app.run()  # app.run(debug=True)     #Para que cuando haga un cambio y guarde el servidor se actualiza enseguida
