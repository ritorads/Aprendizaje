from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Gasto, Categoria
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

gastos_bp = Blueprint('gastos', __name__)

meses = {
        "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
        "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
    }


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

# Nota: Podemos agregar una paginación a la vista de gastos
@gastos_bp.route("/gastos", methods=["GET"])
@login_required
def gastos():
    # Definir los meses
    
    # Obtener la categoría y el mes seleccionados
    selected_vista=request.args.get("vista", "visualizacion")

    selected_categoria = request.args.get("categoria", "")
    selected_mes = request.args.get("mes", "")
    selected_year =  request.args.get("year", "")
    order_field = request.args.get("order_field", "fecha")  # Campo por defecto: "fecha"
    order_direction = request.args.get("order_direction", "asc")  # Dirección por defecto: "asc"

    # Consulta base
    query = Gasto.query.filter_by(Id_usuario=current_user.id)

    # Filtrar por categoría si se seleccionó
    if selected_categoria:
        query = query.filter(Gasto.categoria == selected_categoria)
    
    # Filtrar por mes si se seleccionó y es válido
    if selected_mes and selected_mes in meses:
        mes_numero = meses[selected_mes]  # Obtener el número del mes
        if mes_numero:  # Solo aplicar el filtro si no es "Todos" (None)
            query = query.filter(db.extract('month', Gasto.fecha) == mes_numero)
    
    if selected_year:
        query = query.filter(db.extract('year', Gasto.fecha) == selected_year)

    # Aplicar orden dinámico
    if order_field and order_direction == "asc":
        query = query.order_by(getattr(Gasto, order_field).asc())
    elif order_field and order_direction == "dsc":
        query = query.order_by(getattr(Gasto, order_field).desc())
    
    gastos = query.all()  # Obtener todos los gastos
    
    categorias = Categoria.query.all()  # Obtener todas las categorías

    return render_template(
        "gastos/gastos.html",
        vista=selected_vista,
        gastos=gastos,
        meses=list(meses.keys()),
        selected_categoria=selected_categoria,
        selected_mes=selected_mes,
        selected_year=selected_year,
        order_field=order_field,
        order_direction=order_direction,
        categorias=categorias,
        user=current_user.username
    )

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


@gastos_bp.route("/delete_gasto/<int:id>", methods=["POST"])
@login_required
def delete_gasto(id):
    gasto = Gasto.query.get(id)
    if not gasto:
        return jsonify({"success": False, "error": "Gasto no encontrado"}), 404

    try:
        db.session.delete(gasto)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
