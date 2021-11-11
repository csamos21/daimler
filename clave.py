from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route('/<password>')
def rutaHash(password):
    passHasheado = generate_password_hash(password)

    #hashG5 = 'pbkdf2:sha256:260000$qX0lmkO7ONntdgfM$a4cfda5c1dff01689e439152dc92a739ccf3bd35d602088c675ef7a1ca807320'

    passOKoNot = check_password_hash(passHasheado, password)

    return str(passOKoNot)