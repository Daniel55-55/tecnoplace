"""
ProductController — publicación, edición, eliminación y detalle.
Aplica la regla 'solo usuarios verificados pueden publicar' (decisión arquitectónica clave).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from app.services.product_service import ProductService
from app.services.media_service import MediaService
from app.models import Producto, Categoria

products_bp = Blueprint("products", __name__)


@products_bp.route("/<int:producto_id>")
def detalle(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    return render_template("products/detail.html", producto=producto)


@products_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def crear():
    if not current_user.verificado:
        flash(
            "Debes verificar tu identidad antes de publicar productos.",
            "warning",
        )
        return redirect(url_for("users.verificar"))

    categorias = Categoria.query.order_by(Categoria.nombre).all()

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        precio = request.form.get("precio", "0").strip()
        estado = request.form.get("estado", "usado")
        id_categoria = request.form.get("id_categoria", "")

        if not titulo or not precio or not id_categoria:
            flash("Título, precio y categoría son obligatorios.", "danger")
            return render_template("products/form.html", categorias=categorias, producto=None)

        try:
            precio_f = float(precio)
            if precio_f <= 0:
                raise ValueError
        except ValueError:
            flash("El precio debe ser un número mayor que cero.", "danger")
            return render_template("products/form.html", categorias=categorias, producto=None)

        # Subida de hasta 4 imágenes
        urls = []
        for file in request.files.getlist("imagenes"):
            url = MediaService.guardar_imagen_producto(file)
            if url:
                urls.append(url)

        producto = ProductService.crear(
            current_user, titulo, descripcion, precio_f, estado, id_categoria, urls
        )
        flash("Producto publicado correctamente.", "success")
        return redirect(url_for("products.detalle", producto_id=producto.id))

    return render_template("products/form.html", categorias=categorias, producto=None)


@products_bp.route("/<int:producto_id>/editar", methods=["GET", "POST"])
@login_required
def editar(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    if producto.id_usuario != current_user.id and not current_user.es_admin:
        abort(403)

    categorias = Categoria.query.order_by(Categoria.nombre).all()

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        precio = request.form.get("precio", "0").strip()
        estado = request.form.get("estado", "usado")
        id_categoria = request.form.get("id_categoria", "")

        try:
            precio_f = float(precio)
            if precio_f <= 0:
                raise ValueError
        except ValueError:
            flash("El precio debe ser un número válido.", "danger")
            return render_template("products/form.html", categorias=categorias, producto=producto)

        urls = []
        for file in request.files.getlist("imagenes"):
            url = MediaService.guardar_imagen_producto(file)
            if url:
                urls.append(url)

        ok, msg = ProductService.actualizar(
            producto, current_user, titulo, descripcion, precio_f, estado, id_categoria, urls
        )
        flash(msg, "success" if ok else "danger")
        return redirect(url_for("products.detalle", producto_id=producto.id))

    return render_template("products/form.html", categorias=categorias, producto=producto)


@products_bp.route("/<int:producto_id>/eliminar", methods=["POST"])
@login_required
def eliminar(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    if not ProductService.eliminar(producto, current_user):
        abort(403)
    flash("Producto eliminado.", "info")
    return redirect(url_for("users.perfil"))


@products_bp.route("/<int:producto_id>/comprar", methods=["POST"])
@login_required
def comprar(producto_id):
    """Simulación interna de compra (alcance académico, sin pasarela)."""
    if not current_user.verificado:
        flash("Debes verificar tu identidad para comprar.", "warning")
        return redirect(url_for("users.verificar"))

    producto = Producto.query.get_or_404(producto_id)
    if producto.id_usuario == current_user.id:
        flash("No puedes comprar tu propio producto.", "warning")
        return redirect(url_for("products.detalle", producto_id=producto.id))

    flash(
        f"¡Compra simulada exitosa! Contacta al vendedor: {producto.propietario.correo}",
        "success",
    )
    return redirect(url_for("products.detalle", producto_id=producto.id))
