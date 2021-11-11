#from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField
from wtforms import TextField, TextAreaField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.fields import FileField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')])
    password = PasswordField('Password', validators=[DataRequired(message='No dejar vacío, completar')])

class Contactenos(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message='No dejar vacío, completar')])
    correo = EmailField('Correo', validators=[DataRequired(message='No dejar vacío, completar')])
    mensaje = StringField('Mensaje', validators=[DataRequired(message='No dejar vacío, completar')])
    enviar = SubmitField('Enviar Mensaje')

class RegistroUsuario(FlaskForm):
    cod_usuario = StringField('Codigo Usuario', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=15)])
    nombre_usuario = StringField('Nombre Usuario', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    email_usuario = EmailField('Email Usuario', validators=[DataRequired(message='No dejar vacío, completar'), Email()])
    cargo = StringField('Cargo Usuario', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=15)])
    foto = FileField('Selecciona imagen:')
    codigo_rol = SelectField('Rol de Usuario', choices=[("USER"), ("SADMIN"), ("ADMIN")])
    password = PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=50)])
    codigo_pais = StringField('Pais', validators=[DataRequired(message='No dejar vacío, completar')])
    direccion = TextField('Direccion', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])    
    telefono = StringField('Telefono', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=50)])
    celular = StringField('celular', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=50)])
    ciudad = StringField('ciudad', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=50)])
    submit = SubmitField('Registrar Usuario')

class FabricanteForm(FlaskForm):
    cod_fab = StringField('Codigo Fabricante', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=15)])
    tipoid_fab = SelectField('Tipo ID', choices=[("CC"), ("NUIP"), ("CE"), ("NIT")])
    nroid_fab = StringField('Nro. ID', validators=[DataRequired(message='')])    
    dv_nroid_fab = StringField('DV', validators=[DataRequired(message='')])
    rsocial_fab = StringField('Razon Social', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    name_rep_fab = StringField('Nombre Representante', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    name_con_fab = StringField('Nombre Contacto', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    email_fab = EmailField('Email Fabricante', validators=[DataRequired(message='No dejar vacío, completar'), Email()])
    codigo_pais = StringField('Pais', validators=[DataRequired(message='No dejar vacío, completar')])
    ciudad = StringField('Ciudad', validators=[DataRequired(message='No dejar vacío, completar')])    
    direccion = TextField('Direccion', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])    
    telefono = StringField('Telefono', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=50)])
    celular = StringField('Celular', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=50)])
    submit = SubmitField('Registrar Fabricante')

class EditFabForm(FlaskForm):
    id_fab = StringField('ID.', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=15)])
    cod_fab = StringField('Codigo Fabricante', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=15)])
    tipoid_fab = SelectField('Tipo ID', choices=[("CC"), ("NUIP"), ("CE"), ("NIT")])
    nroid_fab = StringField('Nro. ID', validators=[DataRequired(message='')])    
    dv_nroid_fab = StringField('DV', validators=[DataRequired(message='')])
    rsocial_fab = StringField('Razon Social', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    name_rep_fab = StringField('Nombre Representante', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    name_con_fab = StringField('Nombre Contacto', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    email_fab = EmailField('Email Fabricante', validators=[DataRequired(message='No dejar vacío, completar'), Email()])
    codigo_pais = StringField('Pais', validators=[DataRequired(message='No dejar vacío, completar')])
    ciudad = StringField('Ciudad', validators=[DataRequired(message='No dejar vacío, completar')])    
    direccion = TextField('Direccion', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])    
    telefono = StringField('Telefono', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=50)])
    celular = StringField('Celular', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=50)])
    submit = SubmitField('Actualiza Fabricante')

class AutosForm(FlaskForm):
    cod_aut = StringField('Codigo Auto', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=15)])
    name_aut = SelectField('Nombre Auto', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    Desc_aut = StringField('Descripcion', validators=[DataRequired(message='')])    
    mod_aut = StringField('Modelo', validators=[DataRequired(message='')])
    id_fab = StringField('ID Fabrica', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    lin_aut = StringField('Linea', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    submit = SubmitField('Registrar Usuario')

class ProveedoresForm(FlaskForm):
    cod_prov = StringField('Codigo Proveedor', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=15)])
    tipoid_prov = SelectField('Tipo ID', choices=[("CC"), ("NUIP"), ("CE"), ("NIT")])
    nroid_prov = StringField('Nro. ID', validators=[DataRequired(message='')])    
    dv_nroid_prov = StringField('DV', validators=[DataRequired(message='')])
    rsocial_prov = StringField('Razon Social', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    name_rep_prov = StringField('Nombre Representante', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    name_con_prov = StringField('Nombre Contacto', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    email_prov = EmailField('Email Fabricante', validators=[DataRequired(message='No dejar vacío, completar'), Email()])
    codigo_pais = StringField('Pais', validators=[DataRequired(message='No dejar vacío, completar')])
    ciudad = StringField('Ciudad', validators=[DataRequired(message='No dejar vacío, completar')])    
    direccion = TextField('Direccion', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])    
    telefono = StringField('Telefono', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=50)])
    celular = StringField('Celular', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=50)])
    submit = SubmitField('Registrar Usuario')


class ProductosForm(FlaskForm):
    cod_prod = StringField('Codigo Producto', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=15)])
    name_prod = StringField('Nombre Producto', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])
    desc_prod = StringField('Descripcion', validators=[DataRequired(message='No dejar vacío, completar'), Length(max=255)])    
    cant_min_req = IntegerField('Cantidad Minima Requerida', validators=[DataRequired(message='Valor mayor a 0'), Length(min=10, max=10, message="")])
    cant_disp = IntegerField('Cantidad Disponible', validators=[DataRequired(message='Valor mayor a 0'), Length(min=10, max=10, message="")])
    submit = SubmitField('Registrar Usuario')
