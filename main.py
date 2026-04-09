"""
Main Entry Point
================

Punto de entrada principal de la aplicación.

Este archivo:
1. Crea la aplicación Flask
2. Ejecuta el servidor
"""

from Infrastructure.Web.flask_app import create_app
from config import API_HOST, API_PORT, DEBUG_MODE

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("Turimed - Clean Architecture")
    print("=" * 60)
    print(f"Server running on: http://{API_HOST}:{API_PORT}")
    print()
    print("Available endpoints:")
    print("   GET  /              - API info")
    print("   GET  /health        - Health check")
    print("   POST /users/register - Register new user")
    print("   POST /users/login   - Login user")
    print("   GET  /users/:id     - Get user by ID")
    print("   PATCH /users/:id    - Update user")
    print("   DELETE /users/:id   - Delete user")
    print("   GET  /questionnaire/questions      - Get questionnaire")
    print("   POST /questionnaire/submit         - Submit answers")
    print("   GET  /questionnaire/user/:user_id  - Get user answers")
    print("   POST /promotions/generate          - Generate promo code")
    print("   GET  /promotions/validate/:code    - Validate promo code")
    print("   POST /promotions/redeem            - Redeem promo code")
    print("   GET  /promotions/my-promotions     - Get user promos")
    print("   GET  /promotions/active            - Get active promos")
    print("   POST   /places              - Create place")
    print("   GET    /places/:id          - Get place by ID")
    print("   GET    /places              - Get all places")
    print("   PATCH  /places/:id          - Update place")
    print("   DELETE /places/:id          - Delete place")
    print("   GET  /recommendations/:user_id   - Get recommendations")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 60)

    # Ejecutar el servidor
    app.run(
        host=API_HOST,
        port=API_PORT,
        debug=DEBUG_MODE
    )
