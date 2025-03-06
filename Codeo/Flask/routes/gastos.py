from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Gasto, Categoria
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

gastos_bp = Blueprint('gastos', __name__)

def calcular_facturacion(fecha: date, cuotas: int) -> date:
    dia = fecha.day
    mes = fecha.month
    año = fecha.year
    
    if 1 <= dia <= 24:
        mes_facturacion = mes + 1
    elif 25 <= dia <= 31:
        mes_facturacion = mes + 2
    else:
        mes_facturacion = mes
    if mes_facturacion > 12:
        mes_facturacion -= 12
        año += 1

    primera = date(año, mes_facturacion, 1)
    ultima = primera + relativedelta(months=+(cuotas - 1))
    return primera,ultima

@gastos_bp.route("/gastos" , methods=["GET"])
@login_required
def gastos():
    return render_template("gastos/gastos.html", 
                           gastos = Gasto.query.filter_by(Id_usuario=current_user.id).all(),
                           vista = request.args.get("vista", "visualizacion"),
                           categorias = Categoria.query.all(),
                           user=current_user.username)


@gastos_bp.route("/gastos/filtrar", methods=["GET"])
@login_required
def filtrar_gastos():
    selected = request.args.get("categoria")  # Ajusta si el param se llama 'categoria' o 'cadtegoria'
    
    # Si se seleccionó una categoría, filtra por ella y por el usuario actual
    if selected:
        gastos_lista = Gasto.query.filter(
            Gasto.Id_usuario == current_user.id,
            Gasto.categoria == selected
        ).all()
    else:
        # De lo contrario, muestra todos los gastos del usuario
        gastos_lista = Gasto.query.filter_by(Id_usuario=current_user.id).all()

    # Renderiza el fragmento HTML (p. ej., la tabla o solo el tbody)
    return render_template("gastos/tabla_gastos.html", gastos=gastos_lista)



@gastos_bp.route("/add_gasto", methods=["POST"])
@login_required
def add_gasto():
    nombre = request.form.get("nombre")
    monto = request.form.get("monto")
    cuotas = request.form.get("cuotas")
    fecha = request.form.get("fecha")
    categoria_id = request.form.get("categoria")
    descripcion = request.form.get("descripcion")

    if not nombre or not monto or not categoria_id or not fecha:
        flash("Todos los campos son obligatorios.", "danger")
        flash(f'nombre: {nombre}, monto: {monto}, cuotas: {cuotas}, fecha: {fecha}, categoria_id: {categoria_id}', "danger")
        return redirect(url_for("gastos.gastos", vista="form"))

    try:
        primera, ultima = calcular_facturacion(datetime.strptime(fecha, "%Y-%m-%d"), int(cuotas))
        nuevo_gasto = Gasto(
            Id_usuario = current_user.id,
            nombre=nombre,
            cuotas = int(cuotas),
            monto=float(monto),
            fecha=datetime.strptime(fecha, "%Y-%m-%d"),
            primera_cuota = primera,
            ultima_cuota = ultima,
            categoria= Categoria.query.get(categoria_id).nombre,
            descripcion= descripcion,
        )
        db.session.add(nuevo_gasto)
        db.session.commit()
        flash("Gasto agregado correctamente.", "success")
    except Exception as e:
        db.session.rollback()

    return redirect(url_for("gastos.gastos", vista="visualizacion"))

@gastos_bp.route("/gastos/proyeccion", methods=["GET"])
@login_required
def proyeccion():
    gastos_list = Gasto.query.all()
    categorias = Categoria.query.all()
    return render_template("gastos/proyeccion.html", 
                           gastos=gastos_list, 
                           categorias=categorias, 
                           user=current_user.username)

@gastos_bp.route("/delete_gasto/<int:id>", methods=["POST"])
@login_required
def delete_gasto(id):
    gasto = Gasto.query.get(id)
    if not gasto:
        return redirect(url_for("gastos.gastos", vista = "categorias"))
    try:
        db.session.delete(gasto)
        db.session.commit()
        return redirect(url_for("gastos.gastos", vista = "categorias"))
    except Exception as e:
        db.session.rollback()
        return redirect(url_for("gastos.gastos", vista = "categorias"))
