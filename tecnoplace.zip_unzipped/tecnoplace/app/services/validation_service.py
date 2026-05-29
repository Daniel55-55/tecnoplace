"""
ValidationService — gestiona el envío de documento+selfie y la aprobación por admin.
Implementa el caso de uso central del proyecto (objetivo específico #3).
"""
from datetime import datetime
from app import db
from app.models import DocumentoUsuario, SeguridadValidacion, Usuario, LogAuditoria


class ValidationService:

    @staticmethod
    def enviar_documentos(usuario: Usuario, ruta_documento: str, ruta_selfie: str):
        """Crea el registro de documentos y la solicitud de verificación pendiente."""

        # Marcar solicitudes anteriores como reemplazadas (si las hubiera)
        SeguridadValidacion.query.filter_by(
            id_usuario=usuario.id, estado="pendiente"
        ).update({"estado": "reemplazada"})

        doc = DocumentoUsuario(
            id_usuario=usuario.id,
            foto_documento=ruta_documento,
            selfie=ruta_selfie,
            fecha_subida=datetime.utcnow(),
        )
        validacion = SeguridadValidacion(
            id_usuario=usuario.id,
            foto_documento=ruta_documento,
            selfie=ruta_selfie,
            estado="pendiente",
            fecha_solicitud=datetime.utcnow(),
        )
        db.session.add_all([doc, validacion])
        db.session.commit()

        log = LogAuditoria(
            id_usuario=usuario.id,
            accion="ENVIO_VERIFICACION",
            tabla_afectada="seguridad_validacion",
            registro_id=validacion.id,
        )
        db.session.add(log)
        db.session.commit()
        return validacion

    @staticmethod
    def aprobar(validacion_id: int, admin_id: int, observaciones: str = ""):
        v = SeguridadValidacion.query.get(validacion_id)
        if not v:
            return None
        v.estado = "aprobado"
        v.observaciones = observaciones
        v.fecha_decision = datetime.utcnow()

        usuario = Usuario.query.get(v.id_usuario)
        usuario.verificado = True

        log = LogAuditoria(
            id_usuario=admin_id,
            accion="APROBAR_VERIFICACION",
            tabla_afectada="seguridad_validacion",
            registro_id=v.id,
        )
        db.session.add(log)
        db.session.commit()
        return v

    @staticmethod
    def rechazar(validacion_id: int, admin_id: int, observaciones: str = ""):
        v = SeguridadValidacion.query.get(validacion_id)
        if not v:
            return None
        v.estado = "rechazado"
        v.observaciones = observaciones
        v.fecha_decision = datetime.utcnow()

        log = LogAuditoria(
            id_usuario=admin_id,
            accion="RECHAZAR_VERIFICACION",
            tabla_afectada="seguridad_validacion",
            registro_id=v.id,
        )
        db.session.add(log)
        db.session.commit()
        return v

    @staticmethod
    def estado_actual(usuario_id: int) -> str:
        """Devuelve el estado más reciente: ninguno | pendiente | aprobado | rechazado."""
        v = (
            SeguridadValidacion.query.filter_by(id_usuario=usuario_id)
            .order_by(SeguridadValidacion.id.desc())
            .first()
        )
        return v.estado if v else "ninguno"

    @staticmethod
    def pendientes():
        return (
            SeguridadValidacion.query.filter_by(estado="pendiente")
            .order_by(SeguridadValidacion.fecha_solicitud.asc())
            .all()
        )
