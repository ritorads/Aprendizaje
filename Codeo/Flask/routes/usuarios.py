from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Usuario

# Crear un Blueprint para las rutas de usuarios
usuarios_bp = Blueprint('usuarios', __name__)

# Ruta para mostrar los usuarios de la base de datos
@usuarios_bp.route("/usuarios_psqlflask", methods=["GET"])
@login_required
def usuarios_psqlflask():
    # Obtener todos los usuarios de la base de datos usando SQLAlchemy
    usuarios = Usuario.query.all()

    # Renderiza la plantilla de usuarios
    return render_template("main/usuarios.html", usuarios=usuarios)

# Ruta para agregar un nuevo usuario a la base de datos
@usuarios_bp.route("/psqlflask/add_user", methods=["POST"])
@login_required
def add_user_psqlflask():
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    edad = request.form.get("edad")

    if not nombre or not email or not edad:
        flash("Faltan datos", "danger")
        return redirect(url_for("usuarios.usuarios_psqlflask"))

    try:
        # Crear un nuevo usuario con SQLAlchemy
        nuevo_usuario = Usuario(nombre=nombre, email=email, edad=edad)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario agregado correctamente", "success")
        return redirect(url_for("usuarios.usuarios_psqlflask"))
    except Exception as e:
        flash(f"Error al insertar el usuario: {e}", "danger")
        return redirect(url_for("usuarios.usuarios_psqlflask"))
