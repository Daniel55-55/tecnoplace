"""
AuthController — registro, inicio y cierre de sesión.
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "")
        correo = request.form.get("correo", "")
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")
        telefono = request.form.get("telefono", "")
        documento = request.form.get("documento", "")

        if not nombre or not correo or not password:
            flash("Todos los campos obligatorios deben llenarse.", "danger")
            return render_template("auth/register.html")

        if password != password2:
            flash("Las contraseñas no coinciden.", "danger")
            return render_template("auth/register.html")

        usuario, err = AuthService.registrar_usuario(
            nombre, correo, password, telefono, documento
        )
        if err:
            flash(err, "danger")
            return render_template("auth/register.html")

        login_user(usuario)
        flash(
            "¡Cuenta creada! El siguiente paso es verificar tu identidad para publicar.",
            "success",
        )
        return redirect(url_for("users.verificar"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        correo = request.form.get("correo", "")
        password = request.form.get("password", "")

        usuario, err = AuthService.autenticar(correo, password)
        if err:
            flash(err, "danger")
            return render_template("auth/login.html")

        login_user(usuario, remember=True)
        flash(f"Bienvenido, {usuario.nombre}.", "success")

        if usuario.es_admin:
            return redirect(url_for("admin.dashboard"))

        next_page = request.args.get("next")
        return redirect(next_page or url_for("main.index"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("main.index"))
