"""
Punto de entrada de TecnoPlace.
"""

from app import create_app, db
from app.models import Usuario, Categoria

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Usuario": Usuario,
        "Categoria": Categoria
    }


# SOLO para desarrollo local
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)