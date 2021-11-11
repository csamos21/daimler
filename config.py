class dev():
    DEBUG = True
    SECRET_KEY = "Ecu4d0RRrr0201"
    DATABASE = {
        'name' : 'db.sqlite3', 
        'engine' : 'pewee.SqliteDatabase' 
    }

class prod():
    DEBUG = False
    SECRET_KEY = "K0l0mb14$*."
    DATABASE = {
        'name' : 'daimler.sqlite3', 
        'engine' : 'pewee.MysqlDatabase',
        'host' : 'url.donde.esta.mi.bd.com',
        'username' : 'dsistema_prueba',
        'password' : 'C3l3st1n0**'
    }    