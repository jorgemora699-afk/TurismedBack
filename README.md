# 📱 App Móvil - Lugares y Recomendaciones

Aplicación móvil para descubrir lugares según el perfil del usuario (restaurantes, bares, discotecas, cafés). Incluye cuestionario de preferencias, sistema de categorías y promociones.


## ⚙️ Backend (Flask + PostgreSQL)

### Requisitos previos

- Python 3.10+
- PostgreSQL 14+



### Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Crear la base de datos

```bash
# Conectarse a PostgreSQL
psql -U postgres

# Crear la base de datos
CREATE DATABASE nombre_de_tu_base_de_datos;
\q
```

### 6. Ejecutar el script SQL

```bash
psql -U postgres -d nombre_de_tu_base_de_datos -f database_setup.sql
```

Esto creará todas las tablas e insertará los datos iniciales (categorías, preguntas, lugares y promociones).


## 📦 Dependencias del backend

| Paquete | Versión | Uso |
|---|---|---|
| Flask | 3.1.0 | Framework web |
| Flask-CORS | 5.0.1 | Manejo de CORS |
| psycopg2-binary | 2.9.10 | Conexión a PostgreSQL |
| bcrypt | 4.3.0 | Hash de contraseñas |
| PyJWT | 2.10.1 | Autenticación con tokens JWT |
| python-dotenv | 1.0.1 | Variables de entorno |



## 🗃️ Estructura de la base de datos

| Tabla | Descripción |
|---|---|
| `users` | Usuarios registrados |
| `categories` | Categorías de perfil (Foodies, Fiesteros, etc.) |
| `questions` | Preguntas del cuestionario de preferencias |
| `question_options` | Opciones de respuesta por pregunta |
| `user_answers` | Respuestas del usuario al cuestionario |
| `places` | Lugares (restaurantes, bares, discotecas, cafés) |
| `promotions` | Códigos promocionales con descuento |
| `redemptions` | Registro de promociones usadas por usuario |
