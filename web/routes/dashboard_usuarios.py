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

dashboard_usuarios_bp = Blueprint("dashboard_usuarios", __name__)

@dashboard_usuarios_bp.route('/dashboard/usuarios', methods=['GET', 'POST'])
@admin_requerido
def dashboard_usuarios():
    if request.method == 'POST':
        usuario_a_eliminar = request.form.get('id_usuario')
        if not usuario_a_eliminar:
            flash("No se pudo completar la acción: ID inexistente")
            return redirect(url_for('dashboard_usuarios.dashboard_usuarios'))
        try:
                url_api = f'http://localhost:5000/api/usuarios/{usuario_a_eliminar}'
                response = requests.delete(url_api, timeout=5)
                response.raise_for_status()
                flash("Se elimino correctamente.")
                return redirect(url_for('dashboard_usuarios.dashboard_usuarios'))
        except requests.exceptions.RequestException as e:
                print(f"Error al eliminar en API: {e}")
                return render_template('error-conexion.html'), 500
    else:
        id_buscado = request.args.get('id')
        email_buscado = request.args.get('email')
        rol_buscado = request.args.get('rol')
        try:
            _limit = int(request.args.get('limit', 10))
            _offset = int(request.args.get('offset', 0))
        except ValueError:
            _limit, _offset = 10, 0

        try:
           if id_buscado:
                url_api = f'http://localhost:5000/api/usuarios/{id_buscado}'
                response = requests.get(url_api, timeout=5)
                response.raise_for_status()
                lista_usuarios = [response.json()]
           elif email_buscado:
               url_api = f'http://localhost:5000/api/usuarios/email'
               response = requests.get(url_api, params={'email': email_buscado}, timeout=5)
               response.raise_for_status()
               lista_usuarios = [response.json().get('usuario')]
           elif rol_buscado:
               url_api = f'http://localhost:5000/api/usuarios/rol'
               params = {'rol': rol_buscado, '_limit': _limit, '_offset': _offset}
               response = requests.get(url_api, params=params, timeout=5)
               response.raise_for_status()
               lista_usuarios = response.json().get('data', [])
           else:
               params = {'_limit': _limit, '_offset': _offset}
               url_api = f'http://localhost:5000/api/usuarios'
               response = requests.get(url_api, params=params, timeout=5)
               response.raise_for_status()
               lista_usuarios = response.json().get('data', [])

           try:
               raw_data = response.json()
               total_registros = raw_data.get('count', raw_data.get('total', len(lista_usuarios))) if isinstance(raw_data, dict) else len(lista_usuarios)
           except Exception:
               total_registros = len(lista_usuarios)
           
           total_paginas = (total_registros + _limit - 1) // _limit if total_registros > 0 else 1
           pagina_actual = ( _offset // _limit) + 1
           
           paginacion_links = build_links(url_for('dashboard_usuarios.dashboard_usuarios'), request.args.to_dict(), _limit, _offset, total_registros)
           return render_template('dashboard-usuarios.html', usuarios=lista_usuarios, limit=_limit, offset=_offset, paginacion_links=paginacion_links, pagina_actual=pagina_actual, total_paginas=total_paginas)

        except requests.exceptions.HTTPError:
            flash("No se encontraron resultados.")
            return redirect(url_for('dashboard_usuarios.dashboard_usuarios'))
        except requests.exceptions.RequestException as e:
           print(f"Error crítico al conectar con la API: {e}")
           return render_template('error-conexion.html'),500

@dashboard_usuarios_bp.route('/dashboard/usuarios/crear', methods=['POST'])
def crear_usuario():
    nombre_usuario = request.form.get('nombre_usuario', '').strip()
    contrasena = request.form.get('contrasena', '').strip()
    email = request.form.get('email', '').strip()
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    if not nombre_usuario or not contrasena or not email or not nombre or not apellido:
        flash ("Error al crear usuario: Datos invalidos")
        return redirect(url_for('dashboard_usuarios.dashboard_usuarios'))
    datos = {
        "nombre_usuario": nombre_usuario,
        "contrasena": contrasena,
        "email": email,
        "nombre": nombre,
        "apellido": apellido,
        "rol": request.form.get('rol')
    }
    try:
        url_api = f'http://localhost:5000/api/usuarios'
        response = requests.post(url_api, json=datos, timeout=5)
        response.raise_for_status()
        flash("Usuario creado con éxito")
    except requests.exceptions.HTTPError as e:
        flash(f"Error: {e.response.text}")
    except requests.exceptions.RequestException as e:
        flash("Error al crear el usuario")
    return redirect(url_for('dashboard_usuarios.dashboard_usuarios'))

@dashboard_usuarios_bp.route('/dashboard/usuarios/editar/parcial', methods=['POST'])
def editar_usuario_parcial():
    id_usuario = request.form.get('id_usuario')
    email = request.form.get('email').strip()
    contrasena = request.form.get('password').strip()

    datos = {}
    if email:
        datos["email"] = email
    if contrasena:
        datos["contrasena"] = contrasena

    if not datos:
        flash("Debes completar al menos uno de los campos para actualizar.")
        return redirect(url_for('dashboard_usuarios.dashboard_usuarios'))
    
    datos = {
        "email": email,
        "contrasena": contrasena
    }
    datos = {k: v for k, v in datos.items() if v}
    try:
        url_api = f'http://localhost:5000/api/usuarios/{id_usuario}'
        response = requests.patch(url_api, json=datos, timeout=5)
        response.raise_for_status()
        flash("Email y contraseña actualizados con éxito")
    except requests.exceptions.RequestException as e:
        flash("Error al actualizar el email y la contraseña del usuario")

    return redirect(url_for('dashboard_usuarios.dashboard_usuarios'))

@dashboard_usuarios_bp.route('/dashboard/usuarios/editar/completo', methods=['POST'])
def editar_usuario_completo():
    id_usuario = request.form.get('id_usuario')
    nombre_usuario = request.form.get('usuario', '').strip()
    contrasena = request.form.get('password', '').strip()
    email = request.form.get('email', '').strip()
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    if not nombre_usuario or not contrasena or not email or not nombre or not apellido:
        flash ("Error al editar usuario: Datos invalidos")
        return redirect(url_for('dashboard_usuarios.dashboard_usuarios'))
    datos_completos = {
        "nombre_usuario": nombre_usuario,
        "contrasena": contrasena,
        "email": email,
        "nombre": nombre,
        "apellido": apellido,
        "rol": request.form.get('rol')
    } 
    
    datos_completos = {k: v for k, v in datos_completos.items() if v}
    try:
        url_api = f'http://localhost:5000/api/usuarios/{id_usuario}'
        response = requests.put(url_api,  json=datos_completos, timeout=5)
        response.raise_for_status()
        flash("Usuario actualizado con éxito")
    except requests.exceptions.RequestException as e:
        flash("Error al actualizar el usuario")

    return redirect(url_for('dashboard_usuarios.dashboard_usuarios'))

@dashboard_usuarios_bp.context_processor
def inject_usuario_dashboard():
    return {
        'usuario_actual': {
            'nombre': session.get('nombre'),
            'rol': session.get('rol')
        }
    }