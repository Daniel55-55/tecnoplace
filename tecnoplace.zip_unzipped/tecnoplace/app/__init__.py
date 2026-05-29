"""
Application Factory de TecnoPlace.
Inicializa Flask, extensiones y registra los Blueprints (capa de controladores MVC).
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

from config import Config

# Instancias de extensiones (capa transversal)
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    # Asegurar que existan carpetas críticas
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["SECURE_FOLDER"], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, "..", "instance"), exist_ok=True)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Debes iniciar sesión para acceder."
    login_manager.login_message_category = "warning"

    from app.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar Blueprints (controladores)
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.users import users_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(products_bp, url_prefix="/productos")
    app.register_blueprint(users_bp, url_prefix="/perfil")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Crear las tablas y datos semilla
    with app.app_context():
        db.create_all()
        _seed_initial_data()

    # Inyectar año y categorías a todas las plantillas
    from datetime import datetime
    from app.models import Categoria

    @app.context_processor
    def inject_globals():
        return {
            "current_year": datetime.now().year,
            "all_categorias": Categoria.query.order_by(Categoria.nombre).all(),
        }

    # Manejadores de errores
    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden(e):
        from flask import render_template
        return render_template("errors/403.html"), 403

    @app.errorhandler(500)
    def server_error(e):
        from flask import render_template
        return render_template("errors/500.html"), 500

    return app


def _seed_initial_data():
    """Crea las cinco categorías base y un administrador por defecto."""
    from app.models import Categoria, Usuario
    from datetime import datetime

    categorias_base = [
        "Televisores",
        "Celulares",
        "Computadores",
        "Relojes Inteligentes",
        "Audífonos",
    ]

    for nombre in categorias_base:
        if not Categoria.query.filter_by(nombre=nombre).first():
            db.session.add(Categoria(nombre=nombre))

    # Admin por defecto
    if not Usuario.query.filter_by(correo="admin@tecnoplace.com").first():
        admin = Usuario(
            nombre="Administrador TecnoPlace",
            correo="admin@tecnoplace.com",
            telefono="3000000000",
            documento="ADMIN-000",
            rol="administrador",
            verificado=True,
            fecha_registro=datetime.utcnow(),
        )
        admin.set_password("Admin123!")
        db.session.add(admin)

    db.session.commit()
