import sqlite3

#Conexión a la Base de Datos
con = sqlite3.connect('daimler.db')

#Creando cursor
pibote = con.cursor()

try:
    pibote.execute ("""	
		drop table autos;
		drop table menu;
		drop table menu_rol;
		drop table productos;
		drop table proveedor;
		drop table roles;
		drop table usuarios;
		drop table fabricante;
		drop table produ_prov;
		drop table produ_auto;
    """)
except Exception as e:
    print(e)
    
con.commit()

con.close()