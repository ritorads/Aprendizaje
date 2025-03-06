from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

# Modelo para la autenticación
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


class Usuario(db.Model):
    __tablename__ = 'usuarios'  # Asegúrate que la tabla sea "usuarios"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    edad = db.Column(db.Integer, nullable=False)

    def __init__(self, nombre, email, edad):
        self.nombre = nombre
        self.email = email
        self.edad = edad

class Categoria(db.Model):
    __tablename__ = 'categorias'  # Asegúrate que la tabla sea "categorias"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)

    def __init__(self, nombre):     # Agregamos el parámetro nombre a la función __init__
        self.nombre = nombre


class Gasto(db.Model):
    __tablename__ = 'gastos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    cuotas = db.Column(db.Integer, nullable=True)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    primera_cuota = db.Column(db.Date, nullable=True)
    ultima_cuota = db.Column(db.Date, nullable=True)
    categoria = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)


class Diario(db.Model):
    __tablename__ = 'diarios'  # Asegúrate que la tabla sea "diarios"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_usuario = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    