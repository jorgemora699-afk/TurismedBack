# Turismed - Sistema de Recomendaciones

API REST construida con **Clean Architecture** para sistema de recomendaciones de lugares según preferencias de usuario.

## 🏗️ Arquitectura

Proyecto implementado siguiendo los principios de **Clean Architecture (Uncle Bob)**:
```
├── domain/              # Entidades y Casos de Uso (Lógica de Negocio)
├── application/         # Controllers y Repository Interfaces
├── infrastructure/      # Flask, PostgreSQL (Detalles técnicos)
├── presentation/        # Interfaz Web (HTML, CSS, JS)
└── config.py           # Configuración
```

## 🚀 Tecnologías

- **Backend:** Python 3.14, Flask
- **Base de datos:** PostgreSQL
- **Seguridad:** bcrypt
- **Frontend:** HTML, CSS, JavaScript

## 📋 Funcionalidades

### API de Usuarios
- ✅ Registro de usuarios
- ✅ Login con autenticación
- ✅ CRUD completo de usuarios

### API del Cuestionario
- ✅ 6 preguntas sobre preferencias
- ✅ Asignación automática de categoría
- ✅ Sistema de scoring por palabras clave

### Categorías
- Foodies
- Fiesteros
- Románticos
- Casuales
- Gourmet Nocturnos


### Usuarios
```
POST   /users/register           - Registrar usuario
POST   /users/login              - Login
GET    /users/:id                - Obtener usuario
PATCH  /users/:id                - Actualizar usuario
DELETE /users/:id                - Eliminar usuario
```

### Cuestionario
```
GET    /questionnaire/questions              - Obtener preguntas
POST   /questionnaire/submit                 - Enviar respuestas
GET    /questionnaire/user/:user_id          - Ver respuestas
```

### Interfaz Web
```
GET    /web                      - Login
GET    /web/register             - Registro
GET    /web/questionnaire        - Cuestionario
GET    /web/recommendations      - Recomendaciones
GET    /web/profile              - Perfil
```



## 📝 Próximas funcionalidades

- [ ] API de Lugares
- [ ] API de Recomendaciones
- [ ] API de Promociones
- [ ] Autenticación JWT
- [ ] App móvil con React Native

