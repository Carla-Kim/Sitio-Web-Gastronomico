from flask import Blueprint, request, jsonify
from ..services.categorias import *

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/categorias/<int:id>', methods=['PUT'])
def formatear_categoria(id):
    data = request.get_json()

    result = actualizar_categoria(id, data)

    if result == 'body_invalido':
        return jsonify({'error': 'El body es inválido'}), 400
    elif result == 'nombre_invalido':
        return jsonify({'error': 'El nombre es inválido'}), 400
    elif result == 'error_db':
        return jsonify({'error': 'Error en la conexión con la base de datos'}), 500
    elif result == 'categoria_no_encontrada':
        return jsonify({'error': 'No se encontró una categoría con esa ID.'}), 404
    else:
        return '', 204
