"""
Flask Application
=================

Configuración de Flask y definición de rutas HTTP.

Responsabilidades:
1. Crear la aplicación Flask
2. Configurar CORS (para que la app móvil pueda conectarse)
3. Definir las rutas HTTP (endpoints)
4. Conectar cada ruta con el método correspondiente del controller
"""

from flask import Flask, render_template, redirect
from flask_cors import CORS
from Infrastructure.Controllers.user_controller import UserController
from Infrastructure.Database.user_repository_impl import PostgreSQLUserRepository
from Infrastructure.Controllers.questionnaire_controller import QuestionnaireController
from Infrastructure.Database.questionnaire_repository_impl import PostgreSQLQuestionnaireRepository
from Infrastructure.Controllers.promotion_controller import PromotionController
from Infrastructure.Database.promotion_repository_impl import PostgreSQLPromotionRepository
from Infrastructure.Controllers.place_controller import PlaceController
from Infrastructure.Database.place_repository_impl import PostgreSQLPlaceRepository
from Infrastructure.Controllers.recommendation_controller import RecommendationController
from Infrastructure.auth.auth_middleware import token_required


def create_app():
    """
    Factory function que crea y configura la aplicación Flask

    Returns:
        Flask app configurada y lista para usar
    """

    # 1️⃣ CREAR LA APLICACIÓN FLASK
    import os

    # 1️⃣ CREAR LA APLICACIÓN FLASK
    # Obtener la ruta del archivo actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Ir dos niveles arriba para llegar a la raíz del proyecto
    # Infrastructure/Web/ -> Infrastructure/ -> proyecto_raiz/
    project_root = os.path.dirname(os.path.dirname(current_dir))

    # Ahora las carpetas están en presentation/
    templates_path = os.path.join(project_root, 'presentation', 'templates')
    static_path = os.path.join(project_root, 'presentation', 'static')

    app = Flask(
        __name__,
        template_folder=templates_path,
        static_folder=static_path
    )

    # 2️⃣ CONFIGURAR CORS
    # Permite que la app móvil (React Native) se pueda conectar a la API
    CORS(app)

    # 3️⃣ INYECCIÓN DE DEPENDENCIAS
    # Aquí es donde "armamos" toda la arquitectura

    # Crear el repositorio (capa de infraestructura)
    user_repository = PostgreSQLUserRepository()

    # Crear el controller y pasarle el repositorio
    user_controller = UserController(user_repository)

    questionnaire_repository = PostgreSQLQuestionnaireRepository()

    questionnaire_controller = QuestionnaireController(
        questionnaire_repository,
        user_repository  # Reutilizamos el user_repository
    )

    # Crear el repositorio de promociones
    promotion_repository = PostgreSQLPromotionRepository()

    # Crear el controller de promociones
    promotion_controller = PromotionController(
        promotion_repository,
        user_repository  # Reutilizamos el user_repository
    )

    # Crear el repositorio de lugares
    place_repository = PostgreSQLPlaceRepository()

    # Crear el controller de lugares
    place_controller = PlaceController(place_repository)

    # Crear el controller de recomendaciones
    recommendation_controller = RecommendationController(
        user_repository,      # Reutilizamos
        place_repository      # Reutilizamos
    )

    # 4️⃣ DEFINIR LAS RUTAS HTTP

    # ============================================
    # RUTAS DE PÁGINAS WEB (Frontend)
    # ============================================

    @app.route('/web')
    def web_home():
        """Página principal web"""
        return render_template('index.html')

    @app.route('/web/register')
    def web_register():
        """Página de registro"""
        return render_template('register.html')

    @app.route('/web/questionnaire')
    def web_questionnaire():
        """Página del cuestionario"""
        return render_template('questionnaire.html')

    @app.route('/web/recommendations')
    def web_recommendations():
        """Página de recomendaciones"""
        return render_template('recommendations.html')

    @app.route('/web/profile')
    def web_profile():
        """Página de perfil"""
        return render_template('profile.html')

    @app.route('/users/register', methods=['POST'])
    def register():
        """
        POST /users/register
        Registra un nuevo usuario
        """
        return user_controller.register()

    @app.route('/users/login', methods=['POST'])
    def login():
        """
        POST /users/login
        Autentica un usuario
        """
        return user_controller.login()
    
    @app.route('/users/me', methods=['GET'])
    @token_required
    def get_me(current_user):
        """GET /users/me - Verifica token y retorna usuario actual"""
        user_id = current_user.get('user_id') if isinstance(current_user, dict) else current_user.id
        return user_controller.get_user_by_id(user_id)

    @app.route('/users/<user_id>', methods=['GET'])
    def get_user(user_id):
        """
        GET /users/:id
        Obtiene un usuario por ID
        """
        return user_controller.get_user_by_id(user_id)

    
    @app.route('/users', methods=['GET'])
    @token_required
    def get_all_users(current_user):
        """
        GET /users
        Obtiene todos los usuarios (SOLO ADMIN)
        """
        return user_controller.get_all_users(current_user)

    @app.route('/users/<user_id>', methods=['PATCH'])
    @token_required
    def update_user(current_user, user_id):
        """
        PATCH /users/:id
        Actualiza un usuario
        """
        return user_controller.update_user(current_user, user_id)

    @app.route('/users/<user_id>', methods=['DELETE'])
    @token_required
    def delete_user(current_user, user_id):  # ← Orden importante: current_user primero
        """
        DELETE /users/:id
        REQUIERE TOKEN JWT
        """
        # Opcional: verificar que current_user.user_id == user_id
        # (solo puedes eliminar tu propia cuenta)
        return user_controller.delete_user(current_user, user_id)

    # ============================================
    # RUTAS DEL CUESTIONARIO
    # ============================================

    @app.route('/questionnaire/questions', methods=['GET'])
    def get_questions():
        """
        GET /questionnaire/questions
        Obtiene todas las preguntas del cuestionario
        """
        return questionnaire_controller.get_questions()

    @app.route('/questionnaire/submit', methods=['POST'])
    def submit_questionnaire():
        """
        POST /questionnaire/submit
        Envía respuestas y asigna categoría
        """
        return questionnaire_controller.submit_questionnaire()

    @app.route('/questionnaire/user/<user_id>', methods=['GET'])
    @token_required
    def get_user_answers(current_user, user_id):
        """
        GET /questionnaire/user/:user_id
        Obtiene las respuestas de un usuario
        """
        return questionnaire_controller.get_user_answers(current_user, user_id)

    # ← LAS RUTAS DE PROMOCIONES DEBEN ESTAR AQUÍ
    @app.route('/promotions/generate', methods=['POST'])
    @token_required
    def generate_promotion(current_user):
        """POST /promotions/generate (SOLO ADMIN)"""
        return promotion_controller.generate_promotion(current_user)

    @app.route('/promotions/validate/<code>', methods=['GET'])
    def validate_promotion(code):
        """GET /promotions/validate/:code"""
        return promotion_controller.validate_promotion(code)

    @app.route('/promotions/redeem', methods=['POST'])
    def redeem_promotion():
        """
        POST /promotions/redeem
        Redime un código promocional
        SIN autenticación JWT
        """
        return promotion_controller.redeem_promotion()

    @app.route('/promotions/user/<user_id>', methods=['GET'])
    def get_user_promotions(user_id):
        """
        GET /promotions/user/:user_id
        Obtiene las promociones del usuario
        """
        return promotion_controller.get_user_promotions(None, user_id)

    @app.route('/promotions/active', methods=['GET'])
    def get_active_promotions():
        """GET /promotions/active"""
        return promotion_controller.get_all_active()
    
    @app.route('/promotions/<promotion_id>', methods=['DELETE'])
    @token_required
    def delete_promotion(current_user, promotion_id):
        """DELETE /promotions/:id (SOLO ADMIN)"""
        return promotion_controller.delete_promotion(current_user, promotion_id)

    # ============================================
    # RUTAS DE LUGARES
    # ============================================

    @app.route('/places', methods=['POST'])
    @token_required
    def create_place(current_user):
        """
        POST /places
        Crea un nuevo lugar
        """
        return place_controller.create_place(current_user)

    @app.route('/places/<place_id>', methods=['GET'])
    def get_place(place_id):
        """
        GET /places/:id
        Obtiene un lugar por ID
        """
        return place_controller.get_place(place_id)

    @app.route('/places', methods=['GET'])
    def get_all_places():
        """
        GET /places
        Obtiene todos los lugares
        Query params: ?category_id=1 o ?type=restaurant o ?search=pizza
        """
        return place_controller.get_all_places()

    @app.route('/places/<place_id>', methods=['PATCH'])
    @token_required
    def update_place(current_user, place_id):
        """
        PATCH /places/:id
        Actualiza un lugar (SOLO ADMIN)
        """
        return place_controller.update_place(current_user, place_id)

    @app.route('/places/<place_id>', methods=['DELETE'])
    @token_required
    def delete_place(current_user, place_id):
        """
        DELETE /places/:id
        Elimina un lugar (SOLO ADMIN)
        """
        return place_controller.delete_place(current_user, place_id)

    @app.route('/recommendations/<user_id>', methods=['GET'])
    def get_recommendations(user_id):
        """
        GET /recommendations/:user_id
        Obtiene recomendaciones para un usuario
        """
        return recommendation_controller.get_recommendations(user_id)

    @app.route('/', methods=['GET'])
    def home():
        """
        GET /
        Redirige a la interfaz web
        """
        return redirect('/web')

    @app.route('/health', methods=['GET'])
    def health():
        """
        GET /health
        Health check - verifica que la API esté viva
        """
        return {'status': 'healthy'}, 200

    # 5️⃣ RETORNAR LA APP CONFIGURADA
    return app
