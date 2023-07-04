import hashlib
import sqlite3
from flask import Flask, request

app = Flask(__name__)
conexion = sqlite3.connect('usuarios.db')
cursor = conexion.cursor()
cursor.execute("DROP TABLE IF EXISTS usuarios")
cursor.execute('''CREATE TABLE usuarios 
               (user TEXT PRIMARY KEY NOT NULL, 
                pash TEXT NOT NULL)''')
conexion.commit()

def crear(user, password):
    pash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO usuarios (user, pash) VALUES (?, ?)",
                   (user, pash))
    conexion.commit()

@app.route('/login', methods=['POST'])
def validacion():
    user = request.form['user']
    password = request.form['password']
    pash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM usuarios WHERE user=? AND pash=?",
                   (user, pash))
    usuario = cursor.fetchone()

    if usuario is None:
        return "El usuario no es válido"
    else:
        return "Sesión iniciada"

# Agregar usuarios a la base de datos
crear('Matias', 'cisco123')
crear('Rodrigo', 'cisco123')
crear('Agustin', 'cisco123')

if __name__ == '__main__':
    app.run(port=4850)
