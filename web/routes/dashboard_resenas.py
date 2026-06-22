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

dashboard_resenas_bp = Blueprint("dashboard_resenas", __name__)

@dashboard_resenas_bp.route('/dashboard/resenas', methods=['GET', 'POST'])
@login_requerido
def dashboard_resenas():
    if request.method == 'POST':
        resena_a_cambiar = request.form.get('id_resena')
        estado_actual = request.form.get('estado')
            
        if not resena_a_cambiar:
            flash("No se pudo completar la acción: ID inexistente")
            return redirect(url_for('dashboard_resenas.dashboard_resenas'))
        
        if estado_actual == 'deshabilitada':
            estado_nuevo= 'habilitada'
        else:
            estado_nuevo = 'deshabilitada'

        try:
            url_api = f'http://localhost:5000/api/resenas/{resena_a_cambiar}'
            response = requests.patch(url_api, json={'estado':estado_nuevo}, timeout=5)
            response.raise_for_status()
            flash(f"Reseña {estado_nuevo} con éxito")
            return redirect(url_for('dashboard_resenas.dashboard_resenas'))
        except requests.exceptions.RequestException as e:
            print(f"Error al eliminar en API: {e}")
            return render_template('error-conexion.html'), 500
    else:
        id_buscado = request.args.get('resena-id')
        id_reserva_buscada = request.args.get('resena-reserva-id')
        try:        
            _limit = int(request.args.get('limit', 10))  
            _offset = int(request.args.get('offset', 0))  
        except ValueError:
            _limit, _offset = 10, 0

        try:
            params = {'_limit': _limit, '_offset': _offset}
            if id_buscado:
                url_api = f'http://localhost:5000/api/resenas/{id_buscado}'
                response = requests.get(url_api, timeout=5)
                response.raise_for_status()
                lista_resenas = [response.json()]

            elif id_reserva_buscada:
                url_api = f'http://localhost:5000/api/resenas/reserva/{id_reserva_buscada}'
                response = requests.get(url_api, timeout=5)
                response.raise_for_status()
                lista_resenas = [response.json()]

            else:
                filtros = ['estado', 'fecha_desde', 'fecha_hasta', 'puntaje_ambiente', 'puntaje_servicio', 'puntaje_comida']
                for f in filtros:
                    valor = request.args.get(f)
                    if valor:
                        params[f] = valor
                url_api = f'http://localhost:5000/api/resenas'
                response = requests.get(url_api, params=params, timeout=5)
                response.raise_for_status()
                data = response.json()
                lista_resenas = data if isinstance(data, list) else data.get('resenas', [])

            try:
                raw_data = response.json()
                total_registros = raw_data.get('count', raw_data.get('total', len(lista_resenas))) if isinstance(raw_data, dict) else len(lista_resenas)
            except Exception:
                total_registros = len(lista_resenas)
                
            total_paginas = (total_registros + _limit - 1) // _limit if total_registros > 0 else 1
            pagina_actual = ( _offset // _limit) + 1

            paginacion_links = build_links(url_for('dashboard_resenas.dashboard_resenas'), request.args.to_dict(), _limit, _offset, total_registros)

            return render_template('dashboard-resenas.html', resenas=lista_resenas, limit=_limit, offset=_offset, paginacion_links=paginacion_links, pagina_actual=pagina_actual, total_paginas=total_paginas)
       
        except requests.exceptions.HTTPError:
            flash("No se encontraron resultados para los filtros aplicados.")
            return redirect(url_for('dashboard_resenas.dashboard_resenas'))
        except requests.exceptions.RequestException as e:
           print(f"Error crítico al conectar con la API: {e}")
           return render_template('error-conexion.html'),500

@dashboard_resenas_bp.context_processor
def inject_usuario_dashboard():
    return {
        'usuario_actual': {
            'nombre': session.get('nombre'),
            'rol': session.get('rol')
        }
    }