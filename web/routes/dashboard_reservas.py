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



dashboard_reservas_bp = Blueprint("dashboard_reservas", __name__)

@dashboard_reservas_bp.route('/dashboard/reservas', methods=['GET', 'POST'])
@login_requerido
def dashboard_reservas():  
    if request.method == 'POST':
        id_reserva = request.form.get('reserva_id')
        estado_actual = request.form.get('estado_actual')
        if not id_reserva:
            flash("No se pudo completar la acción: ID inexistente")
            return redirect(url_for('dashboard_reservas.dashboard_reservas'))
        if not estado_actual or estado_actual == 'finalizada' or estado_actual == 'cancelada':
            flash("No se puede cancelar una reserva que ya está finalizada.")
            return redirect(url_for('dashboard_reservas.dashboard_reservas'))
        try:
            url_api = f'http://localhost:5000/api/reservas/{id_reserva}/cancelar'
            response = requests.patch(url_api, timeout=5)
            response.raise_for_status()
            flash("Reserva cancelada con éxito")

            return redirect(url_for('dashboard_reservas.dashboard_reservas'))
        
        except requests.exceptions.RequestException as e:
            flash(f"Error en la operación: Tal vez ya fue cancelada.")
            return redirect(url_for('dashboard_reservas.dashboard_reservas'))
       
    estado = request.args.get('estado')
    fecha = request.args.get('fecha')
    id_buscado = request.args.get('id')

    try:
        _limit = int(request.args.get('limit', 10))
        _offset = int(request.args.get('offset', 0))
    except ValueError:
        _limit, _offset = 10, 0

    try:
        lista_servicios = []
        lista_servicios_reserva = []
        params = {'_limit': _limit, '_offset': _offset}
        lista_reservas = []
        raw_data = None 

        if id_buscado:
            url_api = f'http://localhost:5000/api/reservas/{id_buscado}'
            response_reservas = requests.get(url_api, timeout=5)
            if response_reservas.status_code == 404:
                flash("No se encontraron resultados para los criterios seleccionados.")
                return redirect(url_for('dashboard_reservas.dashboard_reservas'))
            else:
                response_reservas.raise_for_status()
                data = response_reservas.json()
                lista_reservas = [data]
                raw_data = data
            
                url_rel = f'http://localhost:5000/api/servicios-reservas/{id_buscado}'
                resp_rel = requests.get(url_rel, timeout=5)
                if resp_rel.status_code == 200:
                    lista_servicios_reserva = resp_rel.json()
        else:
            if estado: 
                url_api = f'http://localhost:5000/api/reservas/estado/{estado}'
                response_reservas = requests.get(url_api, params=params, timeout=5)
                if response_reservas.status_code == 404:
                    flash("No se encontraron resultados para los criterios seleccionados.")
                    return redirect(url_for('dashboard_reservas.dashboard_reservas'))
    
            elif fecha: 
                url_api = f'http://localhost:5000/api/reservas/fecha/{fecha}'
                response_reservas = requests.get(url_api, params=params, timeout=5)
                if response_reservas.status_code == 404:
                    flash("No se encontraron resultados para los criterios seleccionados.")
                    return redirect(url_for('dashboard_reservas.dashboard_reservas'))

            else: 
                url_api = 'http://localhost:5000/api/reservas'
                response_reservas = requests.get(url_api, params=params, timeout=5)
            if response_reservas.status_code == 404:
                lista_reservas = []
                raw_data = {"data": [], "count": 0}
            else:
                response_reservas.raise_for_status()
                raw_data = response_reservas.json()
                lista_reservas = raw_data.get('data', []) if isinstance(raw_data, dict) else (raw_data if isinstance(raw_data, list) else [])


        try:
            response = requests.get('http://localhost:5000/api/servicios', timeout=5)
            
            if response.status_code == 404:
                lista_servicios = []
            else:
                response.raise_for_status()
                lista_servicios = response.json().get('data', [])
            
            dict_servicios = {s['servicio_id']: s['nombre'] for s in lista_servicios}

            for reserva in lista_reservas:
                reserva_id = reserva.get('reserva_id')
                if reserva_id:
                    try:
                        url_rel = f'http://localhost:5000/api/servicios-reservas/{reserva_id}'
                        resp_rel = requests.get(url_rel, timeout=2)
                        if resp_rel.status_code == 200:
                            servicios_data = resp_rel.json()
                            nombres = [dict_servicios.get(item.get('servicio_id'), "Desconocido") for item in servicios_data]
                            reserva['servicios_str'] = ", ".join(nombres) if nombres else "Ninguno"
                        else:
                            reserva['servicios_str'] = "Ninguno"
                    except:
                        reserva['servicios_str'] = "Error al cargar"

        except requests.exceptions.RequestException as e:
            print(f"Error al cargar servicios: {e}")
            lista_servicios = []
        
        datos_mesas = {'ocupadas': 0, 'desocupadas': 0, 'total': 0}
        try:
            resp_mesas = requests.get('http://localhost:5000/api/mesas', timeout=5)
            if resp_mesas.status_code == 200:
                datos_mesas = resp_mesas.json()
                datos_mesas['total'] = int(datos_mesas.get('ocupadas', 0)) + int(datos_mesas.get('desocupadas', 0))
        except:
            pass
            
        total_registros = 0
        try:
            if id_buscado:
                total_registros = 1 if lista_reservas else 0
            elif isinstance(raw_data, dict):
                total_registros = raw_data.get('count', raw_data.get('total', len(lista_reservas)))
            elif isinstance(raw_data, list):
                total_registros = len(raw_data)
            else:
                total_registros = len(lista_reservas)
        except:
            total_registros = len(lista_reservas)

        total_paginas = (total_registros + _limit - 1) // _limit if total_registros > 0 else 1
        pagina_actual = (_offset // _limit) + 1
        paginacion_links = build_links(url_for('dashboard_reservas.dashboard_reservas'), request.args.to_dict(), _limit, _offset, total_registros)

        return render_template('dashboard-reservas.html', reservas=lista_reservas, limit=_limit, offset=_offset, paginacion_links=paginacion_links, total_paginas=total_paginas, pagina_actual=pagina_actual, servicios=lista_servicios, servicios_reserva=lista_servicios_reserva, datos_mesas=datos_mesas)
    except requests.exceptions.HTTPError:
            flash("No se encontraron resultados para los criterios seleccionados.")
            return redirect(url_for('dashboard_reservas.dashboard_reservas'))
    except requests.exceptions.RequestException as e:
        print(f"Error crítico: {e}")
        return render_template('error-conexion.html'), 500

@dashboard_reservas_bp.route('/dashboard/reservas/registrar_ingreso', methods=['POST'])
def registrar_ingreso():
    id_reserva = request.form.get('reserva_id')
    
    try:
        url_api = f'http://localhost:5000/api/reservas/{id_reserva}/escanear'
        response = requests.patch(url_api, timeout=5)
        
        if response.status_code == 200:
            flash("Ingreso registrado con éxito.")
        else:
            flash("Error al registrar el ingreso: " + response.json().get('message', 'Error desconocido'))
            
    except requests.exceptions.RequestException:
        flash("Error de conexión con el servidor.")
        
    return redirect(url_for('dashboard_reservas.dashboard_reservas'))


@dashboard_reservas_bp.route('/dashboard/servicios/crear', methods=['POST'])
def crear_servicio():
    nombre_raw = request.form.get('nombre', '')

    if not nombre_raw or not nombre_raw.strip():
        flash("El nombre del servicio es obligatorio.")
        return redirect(url_for('dashboard_reservas.dashboard_reservas'))
    
    nombre = {
        "nombre": nombre_raw.strip()
    }
    try:
        url_api = f'http://localhost:5000/api/servicios'
        response = requests.post(url_api, json=nombre, timeout=5)
        response.raise_for_status()
        flash("Servicio creado con éxito")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 409:
            flash("Error: Ya existe un servicio con ese nombre.")
        else:
            flash("Error al procesar la solicitud.")
    except requests.exceptions.RequestException:
        flash("Error al crear el servicio")
    return redirect(url_for('dashboard_reservas.dashboard_reservas'))

@dashboard_reservas_bp.route('/dashboard/servicios/editar', methods=['POST'])
def editar_servicio():
    id_servicio = request.form.get('servicio_id')
    nuevo_nombre = request.form.get('nombre')

    if not id_servicio or not nuevo_nombre or not nuevo_nombre.strip():
        flash("Datos incompletos para la edición.")
        return redirect(url_for('dashboard_reservas.dashboard_reservas'))
    
    try:
        url_api = f'http://localhost:5000/api/servicios/{id_servicio}/nombre'
        response = requests.patch(url_api, json={"nombre": nuevo_nombre}, timeout=5)
        response.raise_for_status()
        flash("Servicio actualizado con éxito")

    except requests.exceptions.HTTPError as e:
        if response.status_code == 409:
            flash("Error: Ya existe otro servicio con ese nombre.")
        else:
            flash(f"Error al actualizar el servicio. {e}")

    except requests.exceptions.RequestException:
        flash(f"Error al actualizar el servicio")

    return redirect(url_for('dashboard_reservas.dashboard_reservas'))

@dashboard_reservas_bp.route('/dashboard/servicios/eliminar', methods=['POST'])
def eliminar_servicio():
    id_servicio = request.form.get('servicio_id')
    try:
        url_api = f'http://localhost:5000/api/servicios/{id_servicio}'
        response = requests.delete(url_api, timeout=5)
        response.raise_for_status()
        flash("Servicio eliminado con éxito")
    except requests.exceptions.RequestException:
        flash("Error al eliminar el servicio")
    return redirect(url_for('dashboard_reservas.dashboard_reservas'))

@dashboard_reservas_bp.route('/dashboard/servicios/cambiar-estado', methods=['POST'])
def cambiar_estado_servicio():
    servicio_id = request.form.get('servicio_id')
    estado_actual = request.form.get('estado_actual')
    
    nuevo_estado = 'deshabilitado' if estado_actual == 'habilitado' else 'habilitado'
    
    try:
        url_api = f'http://localhost:5000/api/servicios/{servicio_id}/estado'
        response = requests.patch(url_api, json={'estado': nuevo_estado}, timeout=5)
        response.raise_for_status()
        
        flash(f"Servicio marcado como {nuevo_estado} correctamente")
    except requests.exceptions.RequestException as e:
        flash(f"Error al cambiar el estado del servicio {e}")
        
    return redirect(url_for('dashboard_reservas.dashboard_reservas'))

@dashboard_reservas_bp.route('/dashboard/mesas/accion', methods=['POST'])
def gestionar_mesas():
    accion = request.form.get('accion')
    cantidad_actual = int(request.form.get('cantidad_actual', 0))
    
    if accion == 'agregar':
        nueva_capacidad = cantidad_actual + 1
    elif accion == 'borrar':
        nueva_capacidad = cantidad_actual - 1
    else:
        flash("Acción no reconocida")
        return redirect(url_for('dashboard_reservas.dashboard_reservas'))

    payload = {"cantidad_mesas": nueva_capacidad}

    try:
        url_api = 'http://localhost:5000/api/mesas/capacidad'
        response = requests.patch(url_api, json=payload, timeout=5)

        response.raise_for_status() 
        flash(f"Capacidad actualizada a {nueva_capacidad} mesas correctamente.")

    except requests.exceptions.HTTPError as e:
        flash("Error al gestionar mesas: No es posible realizar esta acción.")
    except Exception as e:
        flash(f"Error inesperado: {e}")  
    return redirect(url_for('dashboard_reservas.dashboard_reservas'))

@dashboard_reservas_bp.context_processor
def inject_usuario_dashboard():
    return {
        'usuario_actual': {
            'nombre': session.get('nombre'),
            'rol': session.get('rol')
        }
    }