from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, Diario, User

# Crear un Blueprint para las rutas de diario
diario_bp = Blueprint('diario', __name__)

# Ruta para mostrar los diarios de la base de datos
@diario_bp.route("/diario", methods=["GET"])
@login_required
def diario():
    # Obtener todos los diarios de la base de datos usando SQLAlchemy
    diarios = Diario.query.all()

    # Renderiza la plantilla de diarios
    return render_template("diario/diario.html", diarios=diarios, user=current_user.username)