"""
UserController — perfil, mis productos y proceso de verificación de identidad.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services.media_service import MediaService
from app.services.validation_service import ValidationService
from app.models import Producto

users_bp = Blueprint("users", __name__)


@users_bp.route("/")
@login_required
def perfil():
    estado = ValidationService.estado_actual(current_user.id)
    mis_productos = (
        Producto.query.filter_by(id_usuario=current_user.id)
        .order_by(Producto.fecha_publicacion.desc())
        .all()
    )
    return render_template(
        "users/profile.html",
        estado_verificacion=estado,
        mis_productos=mis_productos,
    )


@users_bp.route("/verificar", methods=["GET", "POST"])
@login_required
def verificar():
    """Caso de uso 'Subir foto cédula y selfie' include 'Validar identidad'."""
    if current_user.es_admin:
        flash("Los administradores no requieren verificación.", "info")
        return redirect(url_for("main.index"))

    if current_user.verificado:
        flash("Tu identidad ya está verificada.", "success")
        return redirect(url_for("users.perfil"))

    estado = ValidationService.estado_actual(current_user.id)

    if request.method == "POST":
        documento = request.files.get("foto_documento")
        selfie = request.files.get("selfie")

        if not documento or not selfie:
            flash("Debes adjuntar el documento y la selfie.", "danger")
            return render_template("users/verify.html", estado=estado)

        ruta_doc = MediaService.guardar_documento_seguro(documento, "doc")
        ruta_sel = MediaService.guardar_documento_seguro(selfie, "selfie")

        if not ruta_doc or not ruta_sel:
            flash("Formato de archivo no permitido (usa JPG, PNG o WEBP).", "danger")
            return render_template("users/verify.html", estado=estado)

        ValidationService.enviar_documentos(current_user, ruta_doc, ruta_sel)
        flash(
            "Documentos enviados. Un administrador revisará tu solicitud en menos de 48 horas.",
            "success",
        )
        return redirect(url_for("users.perfil"))

    return render_template("users/verify.html", estado=estado)
