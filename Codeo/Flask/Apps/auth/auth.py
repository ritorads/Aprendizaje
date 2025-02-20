from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user
from models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Lógica de login
    pass

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Lógica de registro
    pass

@auth_bp.route("/logout")
@login_required
def logout():
    # Lógica de logout
    pass
