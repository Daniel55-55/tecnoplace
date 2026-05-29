"""
AuthService — registra, autentica y gestiona sesiones de usuarios.
Aplica bcrypt para el hash de contraseñas (objetivo específico #2).
"""
from datetime import datetime
from app import db
from app.models import Usuario, LogAuditoria


class AuthService:

    @staticmethod
    def registrar_usuario(nombre: str, correo: str, password: str,
                          telefono: str = "", documento: str = "") -> tuple:
        """Crea un usuario. Devuelve (Usuario|None, mensaje_error)."""
        if Usuario.query.filter_by(correo=correo).first():
            return None, "Este correo ya está registrado."

        if len(password) < 8:
            return None, "La contraseña debe tener al menos 8 caracteres."

        usuario = Usuario(
            nombre=nombre.strip(),
            correo=correo.strip().lower(),
            telefono=telefono.strip(),
            documento=documento.strip(),
            rol="usuario",
            verificado=False,
            fecha_registro=datetime.utcnow(),
        )
        usuario.set_password(password)

        db.session.add(usuario)
        db.session.commit()

        AuthService._log(usuario.id, "REGISTRO", "usuarios", usuario.id)
        return usuario, None

    @staticmethod
    def autenticar(correo: str, password: str) -> tuple:
        """Devuelve (Usuario|None, mensaje_error)."""
        usuario = Usuario.query.filter_by(correo=correo.strip().lower()).first()
        if not usuario or not usuario.check_password(password):
            return None, "Correo o contraseña incorrectos."
        if usuario.bloqueado:
            return None, "Tu cuenta ha sido bloqueada por el administrador."
        AuthService._log(usuario.id, "LOGIN", "usuarios", usuario.id)
        return usuario, None

    @staticmethod
    def _log(id_usuario, accion, tabla, registro_id):
        log = LogAuditoria(
            id_usuario=id_usuario,
            accion=accion,
            tabla_afectada=tabla,
            registro_id=registro_id,
        )
        db.session.add(log)
        db.session.commit()
