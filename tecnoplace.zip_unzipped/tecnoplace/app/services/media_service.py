"""
MediaService — guarda imágenes de productos y documentos privados.
Las cédulas y selfies van a /secure (no expuesto públicamente).
Las fotos de productos van a /static/uploads.
"""
import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app


class MediaService:

    @staticmethod
    def _allowed(filename: str) -> bool:
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower()
            in current_app.config["ALLOWED_EXTENSIONS"]
        )

    @staticmethod
    def _gen_name(filename: str) -> str:
        ext = filename.rsplit(".", 1)[1].lower()
        return f"{uuid.uuid4().hex}.{ext}"

    @staticmethod
    def guardar_imagen_producto(file_storage) -> str | None:
        """Guarda y redimensiona una imagen de producto. Devuelve URL relativa."""
        if not file_storage or not file_storage.filename:
            return None
        if not MediaService._allowed(file_storage.filename):
            return None

        new_name = MediaService._gen_name(file_storage.filename)
        full_path = os.path.join(current_app.config["UPLOAD_FOLDER"], new_name)
        file_storage.save(full_path)

        # Redimensionar con Pillow (numeral 9.3)
        try:
            with Image.open(full_path) as img:
                img.thumbnail((1024, 1024))
                img.save(full_path, optimize=True, quality=85)
        except Exception:
            pass

        return f"uploads/{new_name}"

    @staticmethod
    def guardar_documento_seguro(file_storage, prefijo: str = "doc") -> str | None:
        """Guarda un documento privado en /secure."""
        if not file_storage or not file_storage.filename:
            return None
        if not MediaService._allowed(file_storage.filename):
            return None

        ext = file_storage.filename.rsplit(".", 1)[1].lower()
        new_name = f"{prefijo}_{uuid.uuid4().hex}.{ext}"
        full_path = os.path.join(current_app.config["SECURE_FOLDER"], new_name)
        file_storage.save(full_path)

        try:
            with Image.open(full_path) as img:
                img.thumbnail((1280, 1280))
                img.save(full_path, optimize=True, quality=85)
        except Exception:
            pass

        return f"secure/{new_name}"
