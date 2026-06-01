from flask import Blueprint, request, jsonify
from ..services.auth import autenticar

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    datos = request.get_json()

    usuario = autenticar(
        datos['usuario'],
        datos['contraseña']
    )

    if usuario is None:
        return {'error': 'Credenciales inválidas'}, 401

    return {
        'id': usuario['id'],
        'rol': usuario['rol']
    }
