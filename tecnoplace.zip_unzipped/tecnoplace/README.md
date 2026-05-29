# TecnoPlace 🛡️📱

> Plataforma segura para la compra y venta de dispositivos tecnológicos con **validación de identidad** de usuarios y **arquitectura modular MVC**.

**Proyecto académico** – Arquitectura de Software · UNIMINUTO · NRC 85024
**Autor:** Daniel Alejandro Garcia · ID 863128

---

## 🎯 Características

- ✅ **Validación de identidad obligatoria** (foto del documento + selfie + aprobación admin)
- 🔐 Cifrado de contraseñas con **bcrypt**
- 🛡️ Protección **CSRF** en todos los formularios
- 📦 CRUD completo de productos con regla de autoría
- 🔍 Motor de búsqueda con filtros (categoría, estado, precio)
- 🗂️ 5 categorías predefinidas: Televisores, Celulares, Computadores, Relojes Inteligentes, Audífonos
- 👨‍💼 Panel de administración con moderación, bloqueo de usuarios y bitácora
- 📱 Diseño **responsive** (360 / 768 / 1280 px)
- 🎨 Paleta verde institucional (WCAG AA en contraste)
- 🧱 Patrón **MVC**: Modelo (SQLAlchemy) · Vista (Jinja2) · Controlador (Flask Blueprints)
- 📝 Bitácora de auditoría (`log_auditoria`) sobre todas las acciones críticas

---

## 🧱 Arquitectura

Cliente-Servidor bajo patrón **MVC**, con 4 capas claramente separadas:

| Capa | Tecnología | Responsabilidad |
|---|---|---|
| **Presentación** | HTML5 + CSS3 (paleta verde) + JS vanilla | Interfaz y validación cliente |
| **Controladores** | Flask + Blueprints | Orquesta el flujo HTTP |
| **Servicios** | Python puro | Lógica de negocio (Auth, Validation, Product, Search, Media) |
| **Persistencia** | SQLAlchemy + SQLite | Acceso a datos con repositorios |

### Modelo de datos (7 entidades)

`usuarios` · `documentos_usuario` · `seguridad_validacion` · `productos` · `categorias` · `imagen_productos` · `log_auditoria`

---

## 🛠️ Stack tecnológico

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.11 |
| Framework web | Flask 3.0 + Jinja2 |
| Base de datos | SQLite (migrable a PostgreSQL) |
| ORM | SQLAlchemy 2.0 |
| Seguridad | bcrypt + Flask-WTF (CSRF) + Flask-Login |
| Multimedia | Pillow (PIL) |
| Servidor producción | Gunicorn + Nginx |

---

## 📦 Estructura del proyecto

```
tecnoplace/
├── app/
│   ├── __init__.py            # Application Factory
│   ├── models.py              # 7 entidades SQLAlchemy
│   ├── routes/                # CONTROLADORES (Flask Blueprints)
│   │   ├── main.py            # Home + búsqueda
│   │   ├── auth.py            # Registro / Login / Logout
│   │   ├── products.py        # CRUD productos
│   │   ├── users.py           # Perfil + verificación
│   │   └── admin.py           # Panel administrativo
│   ├── services/              # CAPA DE SERVICIOS (lógica de negocio)
│   │   ├── auth_service.py
│   │   ├── product_service.py
│   │   ├── validation_service.py
│   │   ├── search_service.py
│   │   └── media_service.py
│   ├── templates/             # VISTAS Jinja2
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   ├── products/
│   │   ├── users/
│   │   ├── admin/
│   │   └── errors/
│   └── static/
│       ├── css/style.css      # Paleta verde institucional
│       ├── js/main.js         # Validación cliente
│       ├── images/
│       ├── uploads/           # Fotos públicas de productos
│       └── secure/            # Documentos privados (cédulas + selfies)
├── instance/                  # Base de datos SQLite
├── config.py                  # Configuración central
├── run.py                     # Punto de entrada
├── seed.py                    # Datos de demostración
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Instalación local (paso a paso)

### Requisitos previos
- Python **3.10 o superior** ([descargar](https://www.python.org/downloads/))
- Git ([descargar](https://git-scm.com/))

### 1) Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/tecnoplace.git
cd tecnoplace
```

### 2) Crear un entorno virtual

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3) Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4) (Opcional) Cargar datos de demostración

Para tener productos de muestra y usuarios verificados desde el primer arranque:

```bash
python seed.py
```

Esto crea:
- 3 usuarios verificados (contraseña `Demo1234!`)
- 12 productos de muestra repartidos en las 5 categorías

### 5) Ejecutar la aplicación

```bash
python run.py
```

Abre tu navegador en 👉 **http://localhost:5000**

---

## 🔑 Credenciales de prueba

| Rol | Correo | Contraseña |
|---|---|---|
| **Administrador** | `admin@tecnoplace.com` | `Admin123!` |
| Usuario verificado | `maria@demo.com` | `Demo1234!` |
| Usuario verificado | `carlos@demo.com` | `Demo1234!` |
| Usuario verificado | `laura@demo.com` | `Demo1234!` |

> El admin se crea automáticamente al arrancar. Los usuarios demo se crean al ejecutar `seed.py`.

---

## 🧪 Flujo completo para probar

1. **Como administrador:** entra con `admin@tecnoplace.com` → Panel de administración.
2. **Como usuario nuevo:** crea una cuenta → sube documento + selfie → entra como admin y aprueba → vuelve como usuario y publica un producto.
3. **Catálogo:** explora, filtra por categoría/precio, abre el detalle.
4. **Compra simulada:** entra como otro usuario verificado y prueba el botón "Comprar".

---

## 📤 Subir a GitHub (paso a paso)

### Opción A — Desde la línea de comandos

#### 1) Crear el repositorio en GitHub
1. Entra a [github.com](https://github.com) → botón verde **"New"**.
2. Nombre: `tecnoplace` · Descripción libre.
3. Deja **"Public"** marcado.
4. **NO marques** las casillas de "Initialize with README", `.gitignore` ni licencia (ya están en este proyecto).
5. Click en **Create repository**.

#### 2) Inicializar Git en tu carpeta local

Desde la raíz del proyecto:

```bash
git init
git add .
git commit -m "Primer commit: TecnoPlace - Avance 2 Arquitectura de Software"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/tecnoplace.git
git push -u origin main
```

> Reemplaza `TU-USUARIO` por tu nombre de usuario en GitHub.

#### 3) Verificar
Refresca la página de tu repo en GitHub — deberías ver todos los archivos subidos.

---

### Opción B — Desde GitHub Desktop (más visual)

1. Descarga [GitHub Desktop](https://desktop.github.com/).
2. **File → Add Local Repository** → elige la carpeta `tecnoplace`.
3. Acepta crear un repo nuevo si te lo pide.
4. Escribe un commit message → **Commit to main**.
5. Click en **Publish repository** → asigna nombre `tecnoplace` → **Publish**.

---

### Opción C — Solo subir un archivo ZIP

Si solo quieres entregar el ZIP sin usar Git:

1. Comprime toda la carpeta `tecnoplace` (sin `venv/` ni `instance/`).
2. En GitHub: **Create new repository** → **uploading an existing file** → arrastra el ZIP descomprimido.

---

## ☁️ Despliegue en producción

### Opción 1 — Render.com (gratis, recomendado)

1. Sube el proyecto a GitHub (sección anterior).
2. Crea cuenta en [render.com](https://render.com).
3. **New +** → **Web Service** → conecta tu repo.
4. Configuración:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn run:app`
   - **Environment variable:** `SECRET_KEY` = una cadena aleatoria larga
5. Click **Create Web Service** → espera el despliegue.

### Opción 2 — PythonAnywhere

1. Crea cuenta en [pythonanywhere.com](https://pythonanywhere.com).
2. **Web → Add a new web app → Flask → Python 3.10**.
3. Sube el proyecto y configura el WSGI apuntando a `run.py` → `app`.

### Opción 3 — Servidor propio (Gunicorn + Nginx)

```bash
# En el servidor:
git clone https://github.com/TU-USUARIO/tecnoplace.git
cd tecnoplace
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="cadena-aleatoria-larga-en-produccion"
gunicorn --bind 0.0.0.0:8000 run:app
```

Configura Nginx como proxy inverso al puerto 8000 (ver diagrama de despliegue en el documento).

---

## 🛡️ Variables de entorno (producción)

| Variable | Por defecto | Descripción |
|---|---|---|
| `SECRET_KEY` | Valor dev inseguro | **Cambiar obligatoriamente en producción** |
| `DATABASE_URL` | SQLite local | URL de PostgreSQL si migras |

Ejemplo:
```bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
```

---

## 🐛 Solución de problemas

**Error: `ModuleNotFoundError: No module named 'flask'`**
→ Activa el entorno virtual: `source venv/bin/activate` (o `venv\Scripts\activate` en Windows).

**Error: `OperationalError: no such table`**
→ Borra `instance/tecnoplace.db` y vuelve a arrancar `python run.py` — recrea las tablas.

**No me deja publicar productos**
→ Debes verificar tu identidad primero. Entra como admin y aprueba tu solicitud.

**Las imágenes no se ven**
→ Verifica que existen las carpetas `app/static/uploads/` y `app/static/secure/`.

---

## 📚 Referencias

- Grinberg, M. (2018). *Flask Web Development* (2nd ed.). O'Reilly.
- Sommerville, I. (2021). *Ingeniería de software* (10ª ed.). Pearson.
- SQLite Consortium (2024). [SQLite Documentation](https://www.sqlite.org/docs.html).
- OMG (2017). [UML 2.5.1 Specification](https://www.omg.org/spec/UML/).

---

## 📄 Licencia

Proyecto académico — uso educativo · UNIMINUTO 2026.
