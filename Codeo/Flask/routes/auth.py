from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.get_by_username(username)

        if user and user.check_password(password):
            login_user(user)
            flash("¡Inicio de sesión exitoso!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Usuario o contraseña incorrectos", "error")  # <- Mensaje para SweetAlert2
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.get_by_username(username):
            flash("El usuario ya existe", "danger")
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Usuario registrado correctamente", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
