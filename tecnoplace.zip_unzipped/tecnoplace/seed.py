"""
seed.py — Carga datos de demostración para visualizar TecnoPlace de inmediato.
Uso:  python seed.py
"""
from datetime import datetime, timedelta
import random

from app import create_app, db
from app.models import Usuario, Categoria, Producto, ImagenProducto

app = create_app()


DEMO_PRODUCTS = [
    # (titulo, descripcion, precio, estado, categoria_nombre)
    ("iPhone 14 Pro 256GB", "iPhone 14 Pro color negro, 256 GB, batería al 92%, incluye cargador original y caja.",
     3800000, "usado", "Celulares"),
    ("Samsung Galaxy S23 Ultra", "Equipo nuevo sellado, color verde, 512 GB, 12 GB RAM. Garantía Samsung Colombia.",
     4500000, "nuevo", "Celulares"),
    ("MacBook Air M2 13''", "MacBook Air M2 2023, 8 GB RAM, 256 GB SSD, color medianoche, poco uso, perfecta estética.",
     5200000, "usado", "Computadores"),
    ("Lenovo ThinkPad X1 Carbon", "Intel i7 12va, 16 GB RAM, 512 GB SSD, batería en buen estado, ideal para trabajo.",
     4100000, "usado", "Computadores"),
    ("Smart TV LG OLED 55''", "TV OLED 4K, modelo 2023, dolby atmos, control magic remote. Solo 6 meses de uso.",
     3200000, "usado", "Televisores"),
    ("Samsung Crystal UHD 65''", "TV 65 pulgadas, 4K, smart TV con Tizen, HDR10+. Sellada en caja.",
     2800000, "nuevo", "Televisores"),
    ("Apple Watch Series 9", "Apple Watch Series 9, 45 mm, color medianoche, correa sport. Caja completa.",
     1850000, "nuevo", "Relojes Inteligentes"),
    ("Galaxy Watch 6 Classic", "Reloj Samsung Galaxy Watch 6 Classic 47mm, color negro, bisel giratorio.",
     1450000, "usado", "Relojes Inteligentes"),
    ("AirPods Pro 2da Gen", "AirPods Pro 2 con MagSafe USB-C, cancelación activa de ruido, sellados.",
     920000, "nuevo", "Audífonos"),
    ("Sony WH-1000XM5", "Sony WH-1000XM5, los mejores audífonos con cancelación de ruido del mercado. Color negro.",
     1100000, "usado", "Audífonos"),
    ("iPad Pro 11'' M2", "iPad Pro 11 pulgadas con chip M2, 256 GB, Wi-Fi, color gris espacial, incluye Apple Pencil 2da gen.",
     4800000, "usado", "Computadores"),
    ("Xiaomi Redmi Note 13 Pro", "Smartphone Xiaomi Redmi Note 13 Pro, 256 GB, cámara 200 MP, batería 5000 mAh.",
     1350000, "nuevo", "Celulares"),
]

DEMO_USERS = [
    ("María Fernanda Rodríguez", "maria@demo.com", "Demo1234!", "3201234567", "CC1023456789"),
    ("Carlos Andrés Pérez", "carlos@demo.com", "Demo1234!", "3157654321", "CC1098765432"),
    ("Laura Gómez Torres", "laura@demo.com", "Demo1234!", "3009876543", "CC1054321678"),
]


def seed():
    with app.app_context():
        # Usuarios verificados de demostración
        usuarios_creados = []
        for nombre, correo, pwd, tel, doc in DEMO_USERS:
            if Usuario.query.filter_by(correo=correo).first():
                continue
            u = Usuario(
                nombre=nombre,
                correo=correo,
                telefono=tel,
                documento=doc,
                rol="usuario",
                verificado=True,
                fecha_registro=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            )
            u.set_password(pwd)
            db.session.add(u)
            usuarios_creados.append(u)

        db.session.commit()

        todos_usuarios = Usuario.query.filter(Usuario.rol == "usuario", Usuario.verificado == True).all()
        if not todos_usuarios:
            print("⚠ No hay usuarios verificados. Saliendo.")
            return

        # Productos
        for titulo, desc, precio, estado, cat_nombre in DEMO_PRODUCTS:
            cat = Categoria.query.filter_by(nombre=cat_nombre).first()
            if not cat:
                continue
            if Producto.query.filter_by(titulo=titulo).first():
                continue
            owner = random.choice(todos_usuarios)
            p = Producto(
                titulo=titulo,
                descripcion=desc,
                precio=precio,
                estado=estado,
                id_usuario=owner.id,
                id_categoria=cat.id,
                fecha_publicacion=datetime.utcnow() - timedelta(days=random.randint(0, 15)),
                activo=True,
            )
            db.session.add(p)

        db.session.commit()
        print(f"✓ Datos de demo cargados:")
        print(f"  - {len(DEMO_USERS)} usuarios verificados (contraseña: Demo1234!)")
        print(f"  - {len(DEMO_PRODUCTS)} productos de muestra")
        print(f"  - Admin: admin@tecnoplace.com / Admin123!")


if __name__ == "__main__":
    seed()
