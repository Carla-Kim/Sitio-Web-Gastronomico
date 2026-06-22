from functools import wraps
from flask import session, flash, redirect

def login_requerido(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if session.get("usuario_id") is None:
            flash("Inicia sesión primero")
            return redirect('/dashboard/login')
        return view(*args, **kwargs)
    return wrapper

def admin_requerido(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if session.get("usuario_id") is None:
            return redirect('/dashboard/login')
        if session.get("rol") != "admin":
            flash("No tienes permisos para entrar al módulo Usuarios")
            return redirect('/dashboard')
        return view(*args, **kwargs)
    return wrapper