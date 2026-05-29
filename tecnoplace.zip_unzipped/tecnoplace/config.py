"""
Configuración central de TecnoPlace.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    # Seguridad
    SECRET_KEY = os.environ.get("SECRET_KEY", "tecnoplace-dev-secret-key-cambiar-en-produccion")
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'tecnoplace.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Archivos
    UPLOAD_FOLDER = str(BASE_DIR / "app" / "static" / "uploads")
    SECURE_FOLDER = str(BASE_DIR / "app" / "static" / "secure")
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    # Sesiones
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Paginación
    PRODUCTS_PER_PAGE = 12
