import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'Turismed_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '1605'),
    'port': int(os.getenv('DB_PORT', 5432))
}

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '10012026jmdj')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 168

API_HOST = '0.0.0.0'
API_PORT = 5000
DEBUG_MODE = True

ADMIN_EMAILS = ['jorge.mora699@gmail.com']