"""
ProductService — reglas de negocio de publicación, edición y borrado.
Garantiza la regla de autoría: solo el dueño edita su producto (objetivo específico #4).
"""
from datetime import datetime
from app import db
from app.models import Producto, ImagenProducto, LogAuditoria


class ProductService:

    @staticmethod
    def crear(usuario, titulo, descripcion, precio, estado, id_categoria, imagenes_urls):
        producto = Producto(
            titulo=titulo.strip(),
            descripcion=descripcion.strip(),
            precio=float(precio),
            estado=estado,
            id_usuario=usuario.id,
            id_categoria=int(id_categoria),
            fecha_publicacion=datetime.utcnow(),
            activo=True,
        )
        db.session.add(producto)
        db.session.flush()

        for url in imagenes_urls:
            if url:
                db.session.add(ImagenProducto(id_producto=producto.id, url=url))

        log = LogAuditoria(
            id_usuario=usuario.id,
            accion="CREAR_PRODUCTO",
            tabla_afectada="productos",
            registro_id=producto.id,
        )
        db.session.add(log)
        db.session.commit()
        return producto

    @staticmethod
    def actualizar(producto, usuario, titulo, descripcion, precio, estado,
                   id_categoria, imagenes_urls_nuevas):
        """Solo el dueño puede editar. Devuelve (bool_ok, mensaje)."""
        if producto.id_usuario != usuario.id and not usuario.es_admin:
            return False, "No tienes permisos para editar este producto."

        producto.titulo = titulo.strip()
        producto.descripcion = descripcion.strip()
        producto.precio = float(precio)
        producto.estado = estado
        producto.id_categoria = int(id_categoria)

        for url in imagenes_urls_nuevas:
            if url:
                db.session.add(ImagenProducto(id_producto=producto.id, url=url))

        log = LogAuditoria(
            id_usuario=usuario.id,
            accion="EDITAR_PRODUCTO",
            tabla_afectada="productos",
            registro_id=producto.id,
        )
        db.session.add(log)
        db.session.commit()
        return True, "Producto actualizado."

    @staticmethod
    def eliminar(producto, usuario):
        if producto.id_usuario != usuario.id and not usuario.es_admin:
            return False
        db.session.delete(producto)
        log = LogAuditoria(
            id_usuario=usuario.id,
            accion="ELIMINAR_PRODUCTO",
            tabla_afectada="productos",
            registro_id=producto.id,
        )
        db.session.add(log)
        db.session.commit()
        return True
