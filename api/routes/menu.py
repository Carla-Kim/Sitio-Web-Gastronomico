#Eliminar producto - Nico

@productos_bp.route('/productos/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    
    resultado = elimina_producto(id_producto)

    if resultado == 'id_invalido':
        return jsonify(ReturnErrors(400)), 400
    elif resultado == 'Error_db':
        return jsonify(ReturnErrors(500)), 500
    elif resultado == 'Producto_no_encontrado':
        return jsonify(ReturnErrors(404)), 404
    else:
        return '', 204
