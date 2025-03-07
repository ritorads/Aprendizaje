from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from models import db, User
from routes.auth import auth_bp
from routes.main import main_bp
from routes.usuarios import usuarios_bp
from routes.gastos import gastos_bp
from routes.diario import diario_bp
app = Flask(__name__)
app.secret_key = "supersecreto"
import os

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Inicializar SQLAlchemy
db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Redirige a login si no está autenticado
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(gastos_bp)
app.register_blueprint(diario_bp)

with app.app_context():
    db.create_all()  # Crea las tablas si no existen

if __name__ == "__main__":
    app.run(debug=True)
