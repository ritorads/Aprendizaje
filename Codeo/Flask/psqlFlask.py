from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User  # Importa db y User desde models

import psycopg2
from db import conexion_open_psqlFlask, conexion_close_psqlFlask  # Importar funciones desde db.py

app = Flask(__name__)
app.secret_key = "supersecreto"

# Configurar la base de datos de autenticación
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:0@localhost/flask_auth"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar SQLAlchemy con la app
db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Crear las tablas (si no existen) dentro del contexto de la aplicación
with app.app_context():
    db.create_all()

# Página de inicio: un simple menú
@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("main/home.html", user=current_user.username)
    return render_template("index.html")

# Ruta de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return render_template("main/home.html", user=current_user.username)
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.get_by_username(username)
        if user is not None and user.check_password(password):
            login_user(user)
            return render_template("home")
        else:
            flash("Usuario o contraseña incorrectos", "danger")
    return render_template("auth/login.html")

# Ruta de registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return render_template("main/home.html", user=current_user.username)
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
            return render_template("login")
    return render_template("auth/register.html")

# Ruta protegida para ver usuarios de flask_auth
@app.route("/home")
@login_required
def home():
    return render_template("main/home.html", user=current_user.username)

# Ruta para mostrar los usuarios de la base de datos psqlFlask
@app.route("/psqlflask/usuarios", methods=["GET"])
@login_required
def usuarios_psqlflask():
    conn, cursor = conexion_open_psqlFlask()
    cursor.execute("SELECT id, nombre, email, edad FROM users;")
    users = cursor.fetchall()
    conexion_close_psqlFlask(conn, cursor)

    usuarios_list = [
        {"id": row[0], "nombre": row[1], "email": row[2], "edad": row[3]} for row in users
    ]
    return render_template("main/psqlflask_usuarios.html", usuarios=usuarios_list)

# Ruta para agregar un usuario a la base de datos psqlFlask
@app.route("/psqlflask/add_user", methods=["POST"])
@login_required
def add_user_psqlflask():
    nombre = request.form["nombre"]
    email = request.form["email"]
    edad = request.form["edad"]

    if not nombre or not email or not edad:
        flash("Faltan datos", "danger")
        return render_template("usuarios_psqlflask")

    try:
        conn, cursor = conexion_open_psqlFlask()
        cursor.execute(
            "INSERT INTO users (nombre, email, edad) VALUES (%s, %s, %s) RETURNING id;",
            (nombre, email, edad),
        )
        new_id = cursor.fetchone()[0]
        conexion_close_psqlFlask(conn, cursor)
        flash("Usuario agregado correctamente", "success")
        return render_template("usuarios_psqlflask")
    except Exception as e:
        flash(f"Error al insertar el usuario: {e}", "danger")
        return render_template("usuarios_psqlflask")

# Ruta para cerrar sesión
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
