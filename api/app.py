import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = 'gastronomia_db'

DB_CONFIG = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
}

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

test_bp = Blueprint('test', __name__)

@test_bp.route('/usuarios/<usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    conn = mysql.connector.connect(database=DB_NAME, **DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM Usuarios WHERE usuario_id = %s;
        """, (usuario_id,))
        usuario = cursor.fetchone()

    finally:
        cursor.close()
        conn.close()

    result = usuario

    return jsonify(result), 200

@test_bp.route('/login', methods=['POST'])
def verificar_usuario():
    data = request.json
    email = data.get('email')
    contraseña = data.get('contraseña')

    conn = mysql.connector.connect(database=DB_NAME, **DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM Usuarios WHERE email = %s AND contrasena = %s;
        """, (email, contraseña))
        usuario = cursor.fetchone()

    finally:
        cursor.close()
        conn.close()

    if usuario is None:
        return jsonify({"error": "credenciales inválidas"}), 401

    return jsonify(usuario), 200

app.register_blueprint(test_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
