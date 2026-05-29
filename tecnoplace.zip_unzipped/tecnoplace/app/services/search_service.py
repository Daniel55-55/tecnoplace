"""
SearchService — búsqueda y filtrado del catálogo.
Implementa el motor de búsqueda por título, categoría, precio y estado (objetivo #5).
"""
from sqlalchemy import or_
from app.models import Producto


class SearchService:

    @staticmethod
    def buscar(
        q: str = "",
        id_categoria: int | None = None,
        estado: str = "",
        precio_min: float | None = None,
        precio_max: float | None = None,
        page: int = 1,
        per_page: int = 12,
    ):
        query = Producto.query.filter_by(activo=True)

        if q:
            patron = f"%{q.lower()}%"
            query = query.filter(
                or_(
                    Producto.titulo.ilike(patron),
                    Producto.descripcion.ilike(patron),
                )
            )

        if id_categoria:
            query = query.filter(Producto.id_categoria == id_categoria)

        if estado in ("nuevo", "usado"):
            query = query.filter(Producto.estado == estado)

        if precio_min is not None:
            query = query.filter(Producto.precio >= precio_min)

        if precio_max is not None:
            query = query.filter(Producto.precio <= precio_max)

        query = query.order_by(Producto.fecha_publicacion.desc())

        return query.paginate(page=page, per_page=per_page, error_out=False)
