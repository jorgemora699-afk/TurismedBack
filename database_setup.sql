-- ============================================================
--  SCRIPT DE CONFIGURACIÓN DE BASE DE DATOS
--  App Móvil - Lugares y Recomendaciones
-- ============================================================

-- Tabla de categorías
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    category_id INTEGER REFERENCES categories(id),
    has_completed_questionnaire BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(20) DEFAULT 'user',
    CONSTRAINT check_role CHECK (role IN ('user', 'admin'))
);

-- Tabla de preguntas
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    order_number INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de opciones por pregunta
CREATE TABLE question_options (
    id SERIAL PRIMARY KEY,
    question_id INT NOT NULL,
    option_text VARCHAR(100) NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Tabla de respuestas de usuarios
CREATE TABLE user_answers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES questions(id),
    answer_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de lugares
CREATE TABLE places (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    address TEXT,
    phone VARCHAR(20),
    category_id INTEGER REFERENCES categories(id),
    place_type VARCHAR(50),  -- restaurant, nightclub, cafe, bar
    price_range INTEGER CHECK (price_range BETWEEN 1 AND 3),  -- 1=$, 2=$$, 3=$$$
    rating DECIMAL(2, 1) CHECK (rating BETWEEN 0 AND 5),
    image_url TEXT,
    opening_hours TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de promociones
CREATE TABLE promotions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    discount_percentage INTEGER,
    discount_amount DECIMAL(10, 2),
    max_uses INTEGER DEFAULT 1,
    current_uses INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP,
    place_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de redenciones
CREATE TABLE redemptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    promotion_id INTEGER NOT NULL REFERENCES promotions(id) ON DELETE CASCADE,
    redeemed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, promotion_id)
);

-- ============================================================
--  DATOS INICIALES
-- ============================================================

-- Categorías
INSERT INTO categories (name, description) VALUES
('Foodies', 'Amantes de la buena comida y restaurantes con ambiente acogedor'),
('Fiesteros', 'Prefieren discotecas, música animada y ambiente nocturno'),
('Románticos', 'Buscan lugares íntimos, perfectos para parejas'),
('Casuales', 'Disfrutan de cualquier plan sin pretensiones'),
('Gourmet Nocturnos', 'Combinan buena gastronomía con vida nocturna');

-- Preguntas del cuestionario
INSERT INTO questions (question_text, order_number) VALUES
('¿Qué tipo de música prefieres?', 1),
('¿Qué ambiente prefieres?', 2),
('¿Qué tipo de comida prefieres?', 3),
('¿Cuándo prefieres salir?', 4),
('¿Con quién sueles salir?', 5),
('¿Cuál es tu presupuesto promedio?', 6);

-- Opciones del cuestionario
INSERT INTO question_options (question_id, option_text) VALUES
(1, 'Reggaetón'), (1, 'Salsa'), (1, 'Rock'), (1, 'Electrónica'),
(2, 'Tranquilo'), (2, 'Fiestero'), (2, 'Romántico'), (2, 'Familiar'),
(3, 'Comida rápida'), (3, 'Italiana'), (3, 'Mexicana'), (3, 'Asados'),
(4, 'Día'), (4, 'Noche'), (4, 'Fin de semana'), (4, 'Entre semana'),
(5, 'Solo'), (5, 'En pareja'), (5, 'Con amigos'), (5, 'En familia'),
(6, 'Bajo'), (6, 'Medio'), (6, 'Alto');

-- Lugares
INSERT INTO places (name, description, address, phone, category_id, place_type, price_range, rating) VALUES
-- Foodies (category_id = 1)
('La Trattoria Italiana', 'Auténtica cocina italiana con pasta fresca y pizzas artesanales', 'Calle 10 #5-25, El Poblado', '3001234567', 1, 'restaurant', 2, 4.5),
('Sushi Master', 'Restaurante japonés con sushi premium y ambiente minimalista', 'Carrera 43A #7-50', '3009876543', 1, 'restaurant', 3, 4.8),
('El Jardín Secreto', 'Restaurante con cocina de autor en medio de un jardín', 'Calle 8 #38-20', '3002345678', 1, 'restaurant', 3, 4.7),
-- Fiesteros (category_id = 2)
('Club Élite', 'Discoteca con DJ internacionales y pista de baile VIP', 'Calle 10 #40-35', '3003456789', 2, 'nightclub', 2, 4.3),
('La Rumba Bar', 'Bar con música en vivo y ambiente festivo', 'Carrera 70 #44-48', '3004567890', 2, 'bar', 1, 4.2),
('Tropicana Night', 'Discoteca de salsa y música tropical', 'Calle 33 #70-25', '3005678901', 2, 'nightclub', 2, 4.4),
-- Románticos (category_id = 3)
('Restaurante Vista Luna', 'Cena romántica con vista a la ciudad', 'Carrera 43A #1-50, piso 15', '3006789012', 3, 'restaurant', 3, 4.9),
('Café de las Letras', 'Café tranquilo perfecto para conversaciones íntimas', 'Calle 9 #43-10', '3007890123', 3, 'cafe', 2, 4.6),
('El Mirador Romántico', 'Restaurante con terraza y música suave', 'Calle 10A #34-11', '3008901234', 3, 'restaurant', 3, 4.7),
-- Casuales (category_id = 4)
('Burger House', 'Hamburguesas artesanales en ambiente relajado', 'Carrera 35 #8-60', '3009012345', 4, 'restaurant', 1, 4.1),
('Café Central', 'Café tradicional con buen wifi y ambiente de trabajo', 'Calle 49 #52-18', '3000123456', 4, 'cafe', 1, 4.0),
('Pizza Express', 'Pizzería casual con delivery rápido', 'Carrera 80 #30-45', '3001234560', 4, 'restaurant', 1, 4.2),
-- Gourmet Nocturnos (category_id = 5)
('Gourmet Night Club', 'Alta cocina con DJ y cócteles premium', 'Calle 10 #38-55', '3002345670', 5, 'nightclub', 3, 4.6),
('Steak & Beats', 'Restaurante de carnes premium con música electrónica', 'Carrera 43A #6-15', '3003456780', 5, 'restaurant', 3, 4.8),
('Lounge 360', 'Lounge bar con comida gourmet y vista panorámica', 'Calle 16 #28-51, piso 20', '3004567891', 5, 'bar', 3, 4.7);

-- Promociones de ejemplo
INSERT INTO promotions (code, description, discount_percentage, max_uses, expires_at) VALUES
('BIENVENIDA2024', 'Descuento de bienvenida', 20, 100, '2026-12-31 23:59:59'),
('VERANO50',       'Promoción de verano',    50,  50, '2026-08-31 23:59:59'),
('AMIGO15',        'Descuento por referido', 15, 200, '2026-12-31 23:59:59'),
('VIP100',         'Descuento VIP',         100,  10, '2026-12-31 23:59:59');
