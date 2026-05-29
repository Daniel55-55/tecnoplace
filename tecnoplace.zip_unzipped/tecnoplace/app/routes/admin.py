"""
AdminController — panel del administrador.
Acceso restringido por rol == 'administrador'.
"""
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from app import db
from app.models import Usuario, Producto, Categoria, SeguridadValidacion, LogAuditoria
from app.services.validation_service import ValidationService

admin_bp = Blueprint("admin", __name__)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    stats = {
        "usuarios": Usuario.query.count(),
        "verificados": Usuario.query.filter_by(verificado=True).count(),
        "pendientes": SeguridadValidacion.query.filter_by(estado="pendiente").count(),
        "productos": Producto.query.count(),
        "categorias": Categoria.query.count(),
    }
    ultimos_logs = LogAuditoria.query.order_by(LogAuditoria.id.desc()).limit(15).all()
    return render_template("admin/dashboard.html", stats=stats, logs=ultimos_logs)


@admin_bp.route("/validaciones")
@login_required
@admin_required
def validaciones():
    pendientes = ValidationService.pendientes()
    return render_template("admin/validations.html", pendientes=pendientes)


@admin_bp.route("/validaciones/<int:vid>/aprobar", methods=["POST"])
@login_required
@admin_required
def aprobar_validacion(vid):
    obs = request.form.get("observaciones", "")
    ValidationService.aprobar(vid, current_user.id, obs)
    flash("Identidad aprobada. El usuario ya puede publicar.", "success")
    return redirect(url_for("admin.validaciones"))


@admin_bp.route("/validaciones/<int:vid>/rechazar", methods=["POST"])
@login_required
@admin_required
def rechazar_validacion(vid):
    obs = request.form.get("observaciones", "")
    ValidationService.rechazar(vid, current_user.id, obs)
    flash("Identidad rechazada.", "info")
    return redirect(url_for("admin.validaciones"))


@admin_bp.route("/usuarios")
@login_required
@admin_required
def usuarios():
    usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).all()
    return render_template("admin/users.html", usuarios=usuarios)


@admin_bp.route("/usuarios/<int:uid>/bloquear", methods=["POST"])
@login_required
@admin_required
def bloquear_usuario(uid):
    u = Usuario.query.get_or_404(uid)
    if u.es_admin:
        flash("No puedes bloquear a otro administrador.", "danger")
        return redirect(url_for("admin.usuarios"))
    u.bloqueado = not u.bloqueado
    db.session.add(LogAuditoria(
        id_usuario=current_user.id,
        accion="BLOQUEAR_USUARIO" if u.bloqueado else "DESBLOQUEAR_USUARIO",
        tabla_afectada="usuarios",
        registro_id=u.id,
    ))
    db.session.commit()
    flash(
        f"Usuario {'bloqueado' if u.bloqueado else 'desbloqueado'}.",
        "info",
    )
    return redirect(url_for("admin.usuarios"))


@admin_bp.route("/categorias", methods=["GET", "POST"])
@login_required
@admin_required
def categorias():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if nombre and not Categoria.query.filter_by(nombre=nombre).first():
            db.session.add(Categoria(nombre=nombre))
            db.session.commit()
            flash("Categoría creada.", "success")
        else:
            flash("Nombre inválido o ya existe.", "danger")
        return redirect(url_for("admin.categorias"))

    cats = Categoria.query.order_by(Categoria.nombre).all()
    return render_template("admin/categories.html", categorias=cats)


@admin_bp.route("/categorias/<int:cid>/eliminar", methods=["POST"])
@login_required
@admin_required
def eliminar_categoria(cid):
    c = Categoria.query.get_or_404(cid)
    if c.productos.count() > 0:
        flash("No se puede eliminar: tiene productos asociados.", "danger")
    else:
        db.session.delete(c)
        db.session.commit()
        flash("Categoría eliminada.", "info")
    return redirect(url_for("admin.categorias"))


@admin_bp.route("/productos/<int:pid>/eliminar", methods=["POST"])
@login_required
@admin_required
def moderar_producto(pid):
    p = Producto.query.get_or_404(pid)
    db.session.delete(p)
    db.session.add(LogAuditoria(
        id_usuario=current_user.id,
        accion="MODERAR_PRODUCTO",
        tabla_afectada="productos",
        registro_id=pid,
    ))
    db.session.commit()
    flash("Producto eliminado por moderación.", "info")
    return redirect(url_for("admin.dashboard"))
