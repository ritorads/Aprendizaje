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

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:YPjtSNoWyaMhrcZVtOxIRQQcXjqymbQs@trolley.proxy.rlwy.net:57809/railway"
#direccion Postgre simulado en railway

app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Inicializar SQLAlchemy
db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Redirige a login si no está autenticado
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(gastos_bp)
app.register_blueprint(diario_bp)

with app.app_context():
    db.create_all()  # Crea las tablas si no existen

PORT = int(os.environ.get("PORT", 8080))  # Usa 8080 si no hay variable de entorno

# Ejecutar en el host
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

# Ejecutar en local 
# if __name__ == "__main__":
#     app.run(debug=True)
