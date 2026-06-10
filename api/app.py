import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS
from api.routes.menu import menu_bp
from api.routes.categorias import categorias_bp
from api.routes.reserva import reservas_bp
from api.routes.mesa import mesa_bp
from api.routes.resenas import resenas_bp
from api.routes.servicio import servicio_bp
from api.routes.servicios_reservas import servicio_reserva_bp
from api.routes.usuario import usuarios_bp


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

@test_bp.route('/stats', methods=['GET'])
def create_stats():
    conn = mysql.connector.connect(database=DB_NAME, **DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                MONTH(fecha) AS mes,
                COUNT(*) AS cantidad
            FROM Reservas
            GROUP BY MONTH(fecha)
            ORDER BY MONTH(fecha);
        """)
        reservas_db = cursor.fetchall()

        cursor.execute("""
            SELECT
                rol,
                COUNT(*) AS cantidad
            FROM Usuarios
            GROUP BY rol;
        """)
        usuarios_db = cursor.fetchall()

        cursor.execute("""
            SELECT
                AVG(puntuacion_ambiente) AS ambiente,
                AVG(puntuacion_servicio) AS servicio,
                AVG(puntuacion_comida) AS comida
            FROM Resenas;
        """)
        reseñas_db = cursor.fetchone()

        cursor.execute("""
            SELECT
                c.nombre,
                COUNT(*) AS cantidad
            FROM Productos p
            JOIN Categorias c
                ON p.categorias_id = c.categorias_id
            GROUP BY c.categorias_id;
        """)
        menu_db = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    meses = [
        "Ene", "Feb", "Mar", "Abr", "May", "Jun",
        "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
    ]

    result = {
        "reservas": {
            "meses": [meses[r["mes"]] for r in reservas_db],
            "cantidades": [r["cantidad"] for r in reservas_db]
        },

        "usuarios": {
            "roles": [r["rol"] for r in usuarios_db],
            "cantidades": [r["cantidad"] for r in usuarios_db]
        },

        "reseñas": {
            "aspectos": [
                "Ambiente",
                "Servicio",
                "Comida"
            ],
            "promedios": [
                float(reseñas_db["ambiente"] or 0),
                float(reseñas_db["servicio"] or 0),
                float(reseñas_db["comida"] or 0)
            ]
        },

        "menu": {
            "categorias": [r["nombre"] for r in menu_db],
            "cantidades": [r["cantidad"] for r in menu_db]
        }
    }

    return jsonify(result), 200

app.register_blueprint(test_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(resenas_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(mesa_bp)
app.register_blueprint(servicio_bp)
app.register_blueprint(servicio_reserva_bp)
app.register_blueprint(usuarios_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
