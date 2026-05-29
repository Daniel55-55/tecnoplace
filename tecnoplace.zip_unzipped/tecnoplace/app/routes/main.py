"""
MainController — página de inicio y búsqueda del catálogo.
"""
from flask import Blueprint, render_template, request
from app.services.search_service import SearchService
from app.models import Categoria
from flask import current_app

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Landing del marketplace con últimos productos."""
    resultados = SearchService.buscar(page=1, per_page=8)
    return render_template("index.html", productos=resultados.items)


@main_bp.route("/buscar")
def buscar():
    q = request.args.get("q", "").strip()
    cat = request.args.get("categoria", "").strip()
    estado = request.args.get("estado", "").strip()
    precio_min = request.args.get("precio_min", "").strip()
    precio_max = request.args.get("precio_max", "").strip()
    page = int(request.args.get("page", 1))

    id_cat = int(cat) if cat.isdigit() else None
    p_min = float(precio_min) if precio_min else None
    p_max = float(precio_max) if precio_max else None

    paginacion = SearchService.buscar(
        q=q,
        id_categoria=id_cat,
        estado=estado,
        precio_min=p_min,
        precio_max=p_max,
        page=page,
        per_page=current_app.config["PRODUCTS_PER_PAGE"],
    )
    return render_template(
        "products/list.html",
        paginacion=paginacion,
        q=q,
        cat_actual=id_cat,
        estado_actual=estado,
        precio_min=precio_min,
        precio_max=precio_max,
    )


@main_bp.route("/acerca")
def acerca():
    return render_template("acerca.html")
