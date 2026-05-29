"""
Modelos de datos de TecnoPlace.
Refleja exactamente el modelo entidad-relación documentado en la sección 7.1
del Avance 2: 7 entidades principales con integridad referencial.
"""
from datetime import datetime
from flask_login import UserMixin
from app import db, bcrypt


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False, index=True)
    contrasena = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    documento = db.Column(db.String(50))
    rol = db.Column(db.String(20), default="usuario", nullable=False)  # usuario | administrador
    verificado = db.Column(db.Boolean, default=False, nullable=False)
    bloqueado = db.Column(db.Boolean, default=False, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    documentos = db.relationship("DocumentoUsuario", backref="usuario", cascade="all, delete-orphan")
    validaciones = db.relationship("SeguridadValidacion", backref="usuario", cascade="all, delete-orphan")
    productos = db.relationship("Producto", backref="propietario", cascade="all, delete-orphan")
    logs = db.relationship("LogAuditoria", backref="usuario", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        """Cifra la contraseña con bcrypt (objetivo específico #2)."""
        self.contrasena = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.contrasena, password)

    @property
    def es_admin(self) -> bool:
        return self.rol == "administrador"

    def __repr__(self):
        return f"<Usuario {self.correo} verif={self.verificado}>"


class DocumentoUsuario(db.Model):
    """Documentos enviados por el usuario para verificación de identidad."""
    __tablename__ = "documentos_usuario"

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False, index=True)
    foto_documento = db.Column(db.String(255), nullable=False)
    selfie = db.Column(db.String(255), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class SeguridadValidacion(db.Model):
    """Registro del flujo de aprobación/rechazo por administrador."""
    __tablename__ = "seguridad_validacion"

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False, index=True)
    foto_documento = db.Column(db.String(255), nullable=False)
    selfie = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(20), default="pendiente", nullable=False)  # pendiente | aprobado | rechazado
    observaciones = db.Column(db.Text)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_decision = db.Column(db.DateTime)


class Categoria(db.Model):
    """Las cinco categorías predefinidas del alcance."""
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)

    productos = db.relationship("Producto", backref="categoria", lazy="dynamic")


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), nullable=False)  # nuevo | usado
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False, index=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)

    imagenes = db.relationship(
        "ImagenProducto",
        backref="producto",
        cascade="all, delete-orphan",
        order_by="ImagenProducto.id",
    )

    @property
    def imagen_principal(self) -> str:
        if self.imagenes:
            return self.imagenes[0].url
        return "images/placeholder.svg"


class ImagenProducto(db.Model):
    __tablename__ = "imagen_productos"

    id = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False, index=True)
    url = db.Column(db.String(255), nullable=False)


class LogAuditoria(db.Model):
    """Bitácora de acciones críticas del sistema."""
    __tablename__ = "log_auditoria"

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    accion = db.Column(db.String(100), nullable=False)
    tabla_afectada = db.Column(db.String(60))
    registro_id = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
