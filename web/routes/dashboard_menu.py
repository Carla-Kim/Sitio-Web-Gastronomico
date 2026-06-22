import os
import sys
import requests
from functools import wraps
from api.app import app as api_app
from flask import Blueprint, request, jsonify, url_for, flash, redirect, render_template, session
from api.utils.pagination import build_links
from api.utils.auth import login_requerido
from api.utils.auth import admin_requerido

API_URL = os.getenv("API_URL", "http://localhost:5000/api")

dashboard_menu_bp = Blueprint("dashboard_menu", __name__)


@dashboard_menu_bp.route('/dashboard/menu', methods=['GET', 'POST'])
@login_requerido
def dashboard_menu():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        id_a_eliminar = request.form.get('id')
        if not id_a_eliminar:
            flash("No se pudo completar la acción: ID inexistente")
            return redirect(url_for('dashboard_menu.dashboard_menu'))
        try:
            if tipo == 'producto':
                url_api = f'http://localhost:5000/api/productos/{id_a_eliminar}'
                response = requests.delete(url_api, timeout=5)
                response.raise_for_status()
                flash("Producto eliminado con éxito")

            else:
                url_api = f'http://localhost:5000/api/categorias/{id_a_eliminar}'
                response = requests.delete(url_api, timeout=5)
                
                response.raise_for_status()
                flash("Categoria eliminada con éxito")
                
        except requests.exceptions.HTTPError:
            flash("No se puede eliminar la categoria: tiene productos asociados.")
            return redirect(url_for('dashboard_menu.dashboard_menu'))
        except requests.exceptions.RequestException as e:
            print(f"Error al eliminar en API: {e}")
            return render_template('error-conexion.html'), 500
        return redirect(url_for('dashboard_menu.dashboard_menu'))
    else:
        id_buscado = request.args.get('id')
        categoria_id = request.args.get('categoria_id')

        try:
            _limit = int(request.args.get('limit', 10))
            _offset = int(request.args.get('offset', 0))
        except ValueError:
            _limit, _offset = 10, 0
           
        try:
            url_api_categorias = 'http://localhost:5000/api/categorias'
            response_categorias = requests.get(url_api_categorias, timeout=5)
            lista_categorias = []
            if response_categorias.status_code == 200:
                lista_categorias = response_categorias.json().get('data', [])
            
            dict_categorias = {c['categorias_id']: c['nombre'] for c in lista_categorias}


            lista_productos = []
            raw_data = {}
            params = {'limit': _limit, 'offset': _offset}
            if id_buscado:
                url_productos = f'http://localhost:5000/api/productos/{id_buscado}'
                response_productos = requests.get(url_productos, params=params, timeout=5)

                if response_productos.status_code == 204 or response_productos.status_code == 404:
                    flash("No se encontraron resultados para los filtros aplicados.")
                    return redirect(url_for('dashboard_menu.dashboard_menu'))
            elif categoria_id:
                url_productos = f'http://localhost:5000/api/productos/categoria/{categoria_id}'
                response_productos = requests.get(url_productos, params=params, timeout=5)

                if response_productos.status_code == 204 or response_productos.status_code == 404:
                    flash("No se encontraron resultados para los filtros aplicados.")
                    return redirect(url_for('dashboard_menu.dashboard_menu'))
                
            else:
                url_productos = 'http://localhost:5000/api/productos'
                response_productos = requests.get(url_productos, params=params, timeout=5)

            if response_productos.status_code == 204 or response_productos.status_code == 404:
                lista_productos = []
                raw_data = {"count": 0}
            else:
                response_productos.raise_for_status()
                raw_data = response_productos.json()
                lista_productos = raw_data if isinstance(raw_data, list) else raw_data.get('productos', [])
                if not isinstance(lista_productos, list):
                   lista_productos = [raw_data] if id_buscado else []

            for producto in lista_productos:
                if not producto.get("imagen_url"):
                    producto["imagen_url"] = "/uploads/productos/image.webp"
                producto["categoria_nombre"] = dict_categorias.get(producto.get("categoria"), "Sin categoría")

            total_registros = raw_data.get('count', raw_data.get('total', len(lista_productos))) if isinstance(raw_data, dict) else len(lista_productos)

            total_paginas = (total_registros + _limit - 1) // _limit if total_registros > 0 else 1
            pagina_actual = ( _offset // _limit) + 1

            paginacion_links = build_links(url_for('dashboard_menu.dashboard_menu'), request.args.to_dict(), _limit, _offset, total_registros)

            return render_template('dashboard-menu.html', productos=lista_productos, categorias=lista_categorias, paginacion_links=paginacion_links, pagina_actual=pagina_actual, total_paginas=total_paginas, limit=_limit, offset=_offset)
        
        except requests.exceptions.HTTPError:
            flash("No se encontraron resultados para los filtros aplicados.")
            return redirect(url_for('dashboard_menu.dashboard_menu'))

        except requests.exceptions.RequestException as e:

            return render_template('error-conexion.html'), 500
       
@dashboard_menu_bp.route('/dashboard/menu/crear', methods=['POST'])
def crear_producto():
    nombre = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    try:
        precio = float(request.form.get('precio', 0))
        categorias_id = int(request.form.get('categorias_id', 0))
        imagen = request.files.get("imagen")
    except (ValueError, TypeError):
        flash("Datos inválidos (precio o categoría)")
        return redirect(url_for('dashboard_menu.dashboard_menu'))
    if not nombre or not descripcion:
        flash("Datos incompletos. El nombre y la descripción son obligatorios.")
        return redirect(url_for('dashboard_menu.dashboard_menu'))
    
    files = {}

    if imagen and imagen.filename:
        files["imagen"] = (
            imagen.filename,
            imagen.stream,
            imagen.mimetype
        )

    datos = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "categorias_id": categorias_id
    }
    
    try:
        url_api = f'http://localhost:5000/api/productos'
        response = requests.post(url_api, data=datos, files=files, timeout=5)
        response.raise_for_status()
        print(response.status_code)
        print(response.text)
        flash("Producto creado con éxito")
    except requests.exceptions.RequestException as e:
        flash("Error al crear el producto {e}")
    return redirect(url_for('dashboard_menu.dashboard_menu'))

@dashboard_menu_bp.route('/dashboard/menu/editar', methods=['POST'])
def editar_producto():
    id_producto = request.form.get('id')
    nombre = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    try:
        precio = float(request.form.get('precio', 0))
        categorias_id = int(request.form.get('categorias_id', 0))
        imagen = request.files.get('imagen')
    except (ValueError, TypeError):
        flash("Datos inválidos (precio o categoría)")
        return redirect(url_for('dashboard_menu.dashboard_menu'))
    datos = {
        "categorias_id": str(categorias_id), 
        "nombre": nombre,
        "precio": str(precio),              
        "descripcion": descripcion
    }

    files = {}

    if imagen and imagen.filename:
        files["imagen"] = (
            imagen.filename,
            imagen.stream,
            imagen.mimetype
        )

    try:
        url_api = f'http://localhost:5000/api/productos/{id_producto}'
        response = requests.put(url_api, data=datos, files=files, timeout=5)
        response.raise_for_status()
        flash("Producto actualizado con éxito")
    except requests.exceptions.RequestException as e:
        flash(f"Error al actualizar el producto {e}")
    return redirect(url_for('dashboard_menu.dashboard_menu'))



@dashboard_menu_bp.route('/dashboard/categorias/crear', methods=['POST'])
def crear_categoria():
    nombre = request.form.get('nombre_categoria', '').strip()
    datos = {
        "nombre": nombre
    }
    if not nombre:
        flash("Datos incompletos. El nombre es obligatorio.")
        return redirect(url_for('dashboard_menu.dashboard_menu'))

    try:
        url_api = f'http://localhost:5000/api/categorias'
        response = requests.post(url_api, json=datos, timeout=5)
        response.raise_for_status()
        flash("Categoría creada con éxito")
    except requests.exceptions.RequestException as e:
        flash("Error al crear la categoría")
    return redirect(url_for('dashboard_menu.dashboard_menu'))

@dashboard_menu_bp.route('/dashboard/categorias/editar', methods=['POST'])
def editar_categoria():
    nombre = request.form.get('nombre', '').strip()
    id_categoria = request.form.get('id')
    datos = {"nombre": nombre}
    try:
        url_api = f'http://localhost:5000/api/categorias/{id_categoria}'
        response = requests.put(url_api, json=datos, timeout=5)
        response.raise_for_status()
        flash("Categoría actualizada con éxito")
    except requests.exceptions.RequestException:
        flash("Error al actualizar la categoría: Datos invalidos")
    return redirect(url_for('dashboard_menu.dashboard_menu'))

@dashboard_menu_bp.context_processor
def inject_usuario_dashboard():
    return {
        'usuario_actual': {
            'nombre': session.get('nombre'),
            'rol': session.get('rol')
        }
    }