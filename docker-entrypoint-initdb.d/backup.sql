--
-- PostgreSQL database dump
--

\restrict 9C5cYdmT4cE6bM0C6qmMyYVuSQQECwYdBanQ1rw0JoA5BqqUjjLeOEfBbnvqJdI

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: places; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.places (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    description text,
    address text,
    phone character varying(20),
    category_id integer,
    place_type character varying(50),
    price_range integer,
    rating numeric(2,1),
    image_url text,
    opening_hours text,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT places_price_range_check CHECK (((price_range >= 1) AND (price_range <= 3))),
    CONSTRAINT places_rating_check CHECK (((rating >= (0)::numeric) AND (rating <= (5)::numeric)))
);


ALTER TABLE public.places OWNER TO postgres;

--
-- Name: places_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.places_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.places_id_seq OWNER TO postgres;

--
-- Name: places_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.places_id_seq OWNED BY public.places.id;


--
-- Name: promotions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.promotions (
    id integer NOT NULL,
    code character varying(20) NOT NULL,
    description text,
    discount_percentage integer,
    discount_amount numeric(10,2),
    max_uses integer DEFAULT 1,
    current_uses integer DEFAULT 0,
    is_active boolean DEFAULT true,
    expires_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    place_id integer
);


ALTER TABLE public.promotions OWNER TO postgres;

--
-- Name: promotions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.promotions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.promotions_id_seq OWNER TO postgres;

--
-- Name: promotions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.promotions_id_seq OWNED BY public.promotions.id;


--
-- Name: question_options; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.question_options (
    id integer NOT NULL,
    question_id integer NOT NULL,
    option_text character varying(100) NOT NULL
);


ALTER TABLE public.question_options OWNER TO postgres;

--
-- Name: question_options_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.question_options_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.question_options_id_seq OWNER TO postgres;

--
-- Name: question_options_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.question_options_id_seq OWNED BY public.question_options.id;


--
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questions (
    id integer NOT NULL,
    question_text text NOT NULL,
    order_number integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.questions OWNER TO postgres;

--
-- Name: questions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.questions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.questions_id_seq OWNER TO postgres;

--
-- Name: questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.questions_id_seq OWNED BY public.questions.id;


--
-- Name: redemptions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.redemptions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    promotion_id integer NOT NULL,
    redeemed_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.redemptions OWNER TO postgres;

--
-- Name: redemptions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.redemptions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.redemptions_id_seq OWNER TO postgres;

--
-- Name: redemptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.redemptions_id_seq OWNED BY public.redemptions.id;


--
-- Name: user_answers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_answers (
    id integer NOT NULL,
    user_id integer NOT NULL,
    question_id integer NOT NULL,
    answer_text text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.user_answers OWNER TO postgres;

--
-- Name: user_answers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_answers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_answers_id_seq OWNER TO postgres;

--
-- Name: user_answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_answers_id_seq OWNED BY public.user_answers.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    phone character varying(20),
    category_id integer,
    has_completed_questionnaire boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    role character varying(20) DEFAULT 'user'::character varying,
    CONSTRAINT check_role CHECK (((role)::text = ANY ((ARRAY['user'::character varying, 'admin'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: places id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.places ALTER COLUMN id SET DEFAULT nextval('public.places_id_seq'::regclass);


--
-- Name: promotions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotions ALTER COLUMN id SET DEFAULT nextval('public.promotions_id_seq'::regclass);


--
-- Name: question_options id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_options ALTER COLUMN id SET DEFAULT nextval('public.question_options_id_seq'::regclass);


--
-- Name: questions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions ALTER COLUMN id SET DEFAULT nextval('public.questions_id_seq'::regclass);


--
-- Name: redemptions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.redemptions ALTER COLUMN id SET DEFAULT nextval('public.redemptions_id_seq'::regclass);


--
-- Name: user_answers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_answers ALTER COLUMN id SET DEFAULT nextval('public.user_answers_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name, description, created_at) FROM stdin;
1	Foodies	Amantes de la buena comida y restaurantes con ambiente acogedor	2026-04-06 11:27:52.462145
2	Fiesteros	Prefieren discotecas, música animada y ambiente nocturno	2026-04-06 11:27:52.462145
3	Románticos	Buscan lugares íntimos, perfectos para parejas	2026-04-06 11:27:52.462145
4	Casuales	Disfrutan de cualquier plan sin pretensiones	2026-04-06 11:27:52.462145
5	Gourmet Nocturnos	Combinan buena gastronomía con vida nocturna	2026-04-06 11:27:52.462145
\.


--
-- Data for Name: places; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.places (id, name, description, address, phone, category_id, place_type, price_range, rating, image_url, opening_hours, is_active, created_at) FROM stdin;
1	La Trattoria Italiana	Auténtica cocina italiana con pasta fresca y pizzas artesanales	Calle 10 #5-25, El Poblado	3001234567	1	restaurant	2	4.5	\N	\N	t	2026-04-06 11:28:29.19012
2	Sushi Master	Restaurante japonés con sushi premium y ambiente minimalista	Carrera 43A #7-50	3009876543	1	restaurant	3	4.8	\N	\N	t	2026-04-06 11:28:29.19012
3	El Jardín Secreto	Restaurante con cocina de autor en medio de un jardín	Calle 8 #38-20	3002345678	1	restaurant	3	4.7	\N	\N	t	2026-04-06 11:28:29.19012
4	Club Élite	Discoteca con DJ internacionales y pista de baile VIP	Calle 10 #40-35	3003456789	2	nightclub	2	4.3	\N	\N	t	2026-04-06 11:28:29.19012
5	La Rumba Bar	Bar con música en vivo y ambiente festivo	Carrera 70 #44-48	3004567890	2	bar	1	4.2	\N	\N	t	2026-04-06 11:28:29.19012
6	Tropicana Night	Discoteca de salsa y música tropical	Calle 33 #70-25	3005678901	2	nightclub	2	4.4	\N	\N	t	2026-04-06 11:28:29.19012
7	Restaurante Vista Luna	Cena romántica con vista a la ciudad	Carrera 43A #1-50, piso 15	3006789012	3	restaurant	3	4.9	\N	\N	t	2026-04-06 11:28:29.19012
8	Café de las Letras	Café tranquilo perfecto para conversaciones íntimas	Calle 9 #43-10	3007890123	3	cafe	2	4.6	\N	\N	t	2026-04-06 11:28:29.19012
9	El Mirador Romántico	Restaurante con terraza y música suave	Calle 10A #34-11	3008901234	3	restaurant	3	4.7	\N	\N	t	2026-04-06 11:28:29.19012
10	Burger House	Hamburguesas artesanales en ambiente relajado	Carrera 35 #8-60	3009012345	4	restaurant	1	4.1	\N	\N	t	2026-04-06 11:28:29.19012
11	Café Central	Café tradicional con buen wifi y ambiente de trabajo	Calle 49 #52-18	3000123456	4	cafe	1	4.0	\N	\N	t	2026-04-06 11:28:29.19012
12	Pizza Express	Pizzería casual con delivery rápido	Carrera 80 #30-45	3001234560	4	restaurant	1	4.2	\N	\N	t	2026-04-06 11:28:29.19012
13	Gourmet Night Club	Alta cocina con DJ y cócteles premium	Calle 10 #38-55	3002345670	5	nightclub	3	4.6	\N	\N	t	2026-04-06 11:28:29.19012
14	Steak & Beats	Restaurante de carnes premium con música electrónica	Carrera 43A #6-15	3003456780	5	restaurant	3	4.8	\N	\N	t	2026-04-06 11:28:29.19012
15	Lounge 360	Lounge bar con comida gourmet y vista panorámica	Calle 16 #28-51, piso 20	3004567891	5	bar	3	4.7	\N	\N	t	2026-04-06 11:28:29.19012
18	TUTAINA 		Calle 10 #43E-72	3234748366	2	nightclub	3	\N	\N	Viernes- Domingo 9:00 PM - 4:00 AM 	t	2026-04-09 17:20:41.67087
19	Seremyc Esthetic 	Spa 	Carrera 73C #74-57	3004551666	4	cafe	2	\N	\N	Lunes - Sábado 9:00 AM - 6:00 PM 	t	2026-04-09 17:23:26.509138
20	Salvaje 		Carrera 52 #35-32	3128541321	2	nightclub	2	\N	\N	Jueves - Domingo 9:00 PM - 4:00 AM 	t	2026-04-09 18:40:07.746061
21	Arte frío 	Café bar 	Carrera 73C # 74-57	3002651328	3	cafe	2	\N	\N	Lunes - Domingo 2:00 PM - 11:00 PM 	t	2026-04-09 18:45:03.168037
\.


--
-- Data for Name: promotions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.promotions (id, code, description, discount_percentage, discount_amount, max_uses, current_uses, is_active, expires_at, created_at, place_id) FROM stdin;
1	BIENVENIDA2024	Descuento de bienvenida	20	\N	100	1	t	2026-12-31 23:59:59	2026-04-06 11:28:06.281391	4
2	VERANO50	Promoción de verano	50	\N	50	2	t	2026-08-31 23:59:59	2026-04-06 11:28:06.281391	3
5	NLIS6I1YP5	Descuento en masajes de relajación o limpieza facial	10	\N	10	0	t	2026-05-06 21:01:47.777379	2026-04-06 21:01:47.908	\N
3	AMIGO15	Descuento por referido	15	\N	200	2	t	2026-12-31 23:59:59	2026-04-06 11:28:06.281391	2
4	VIP100	Descuento VIP	100	\N	10	3	t	2026-12-31 23:59:59	2026-04-06 11:28:06.281391	1
8	MORA1605	Descuento de cumpleaños	15	\N	15	1	t	2026-05-08 20:45:35.947683	2026-04-08 20:45:36.031614	\N
\.


--
-- Data for Name: question_options; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.question_options (id, question_id, option_text) FROM stdin;
1	1	Reggaetón
2	1	Salsa
3	1	Rock
4	1	Electrónica
5	2	Tranquilo
6	2	Fiestero
7	2	Romántico
8	2	Familiar
9	3	Comida rápida
10	3	Italiana
11	3	Mexicana
12	3	Asados
13	4	Día
14	4	Noche
15	4	Fin de semana
16	4	Entre semana
17	5	Solo
18	5	En pareja
19	5	Con amigos
20	5	En familia
21	6	Bajo
22	6	Medio
23	6	Alto
\.


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.questions (id, question_text, order_number, created_at) FROM stdin;
1	¿Qué tipo de música prefieres?	1	2026-04-06 11:27:47.866244
2	¿Qué ambiente prefieres?	2	2026-04-06 11:27:47.866244
3	¿Qué tipo de comida prefieres?	3	2026-04-06 11:27:47.866244
4	¿Cuándo prefieres salir?	4	2026-04-06 11:27:47.866244
5	¿Con quién sueles salir?	5	2026-04-06 11:27:47.866244
6	¿Cuál es tu presupuesto promedio?	6	2026-04-06 11:27:47.866244
\.


--
-- Data for Name: redemptions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.redemptions (id, user_id, promotion_id, redeemed_at) FROM stdin;
1	1	4	2026-04-06 17:25:21.732502
2	1	2	2026-04-06 17:28:02.229176
3	1	3	2026-04-06 17:34:07.730047
4	1	1	2026-04-06 17:41:40.017236
5	3	4	2026-04-06 17:52:44.194151
6	4	2	2026-04-06 20:59:17.389934
9	7	8	2026-04-09 18:54:24.745827
\.


--
-- Data for Name: user_answers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_answers (id, user_id, question_id, answer_text, created_at) FROM stdin;
13	1	1	Salsa	2026-04-06 14:22:54.391095
14	1	2	Tranquilo	2026-04-06 14:22:54.391095
15	1	3	Comida rápida	2026-04-06 14:22:54.391095
16	1	4	Fin de semana	2026-04-06 14:22:54.391095
17	1	5	Con amigos	2026-04-06 14:22:54.391095
18	1	6	Medio	2026-04-06 14:22:54.391095
37	3	1	Salsa	2026-04-06 17:50:41.129925
38	3	2	Fiestero	2026-04-06 17:50:41.129925
39	3	3	Comida rápida	2026-04-06 17:50:41.129925
40	3	4	Fin de semana	2026-04-06 17:50:41.129925
41	3	5	Con amigos	2026-04-06 17:50:41.129925
42	3	6	Medio	2026-04-06 17:50:41.129925
43	4	1	Salsa	2026-04-06 20:58:34.328359
44	4	2	Familiar	2026-04-06 20:58:34.328359
45	4	3	Italiana	2026-04-06 20:58:34.328359
46	4	4	Día	2026-04-06 20:58:34.328359
47	4	5	En familia	2026-04-06 20:58:34.328359
48	4	6	Alto	2026-04-06 20:58:34.328359
61	7	1	Rock	2026-04-07 18:45:10.301995
62	7	2	Fiestero	2026-04-07 18:45:10.301995
63	7	3	Asados	2026-04-07 18:45:10.301995
64	7	4	Fin de semana	2026-04-07 18:45:10.301995
65	7	5	Con amigos	2026-04-07 18:45:10.301995
66	7	6	Alto	2026-04-07 18:45:10.301995
67	9	1	Salsa	2026-04-09 18:18:34.375128
68	9	2	Romántico	2026-04-09 18:18:34.375128
69	9	3	Mexicana	2026-04-09 18:18:34.375128
70	9	4	Noche	2026-04-09 18:18:34.375128
71	9	5	En pareja	2026-04-09 18:18:34.375128
72	9	6	Medio	2026-04-09 18:18:34.375128
73	10	1	Rock	2026-04-09 18:21:46.942253
74	10	2	Tranquilo	2026-04-09 18:21:46.942253
75	10	3	Asados	2026-04-09 18:21:46.942253
76	10	4	Fin de semana	2026-04-09 18:21:46.942253
77	10	5	En pareja	2026-04-09 18:21:46.942253
78	10	6	Alto	2026-04-09 18:21:46.942253
79	11	1	Salsa	2026-04-14 19:17:44.85612
80	11	2	Romántico	2026-04-14 19:17:44.85612
81	11	3	Comida rápida	2026-04-14 19:17:44.85612
82	11	4	Fin de semana	2026-04-14 19:17:44.85612
83	11	5	Con amigos	2026-04-14 19:17:44.85612
84	11	6	Medio	2026-04-14 19:17:44.85612
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password, phone, category_id, has_completed_questionnaire, created_at, role) FROM stdin;
1	Jorge Mora	jorge.mora699@gmail.com	$2b$12$xEf.Uj2ngn8jj1JztBQfk.ujzxQnQr6GAatL59IO4dZdiTvsMI7h2	3001234567	2	t	2026-04-06 11:51:54.9357	admin
4	Alba Carvajal	albanory123@gmail.com	$2b$12$mGy34JcIB9ermnJX8SZjxutStqUlL6J.z2rVU8uawFOrHueqKUWuO	3124657889	5	t	2026-04-06 20:57:51.540228	user
7	Julián Arango	arango773@hotmail.com	$2b$12$e3I4CYV6wRBeNk4h/vYIu.lKfhYAYFqbYhTwGiu9tPAI5LyBbLc/y	3012653213	5	t	2026-04-07 18:44:19.083248	user
3	Alejandro Carvajal	carvajal1102@gmail.com	$2b$12$qVDeX9MxXQ9LKEjj3O27FObd1s0eQLxKxFSekHp8x0kevUO6Q9IKy	3169235688	2	t	2026-04-06 13:37:57.317924	user
10	Jorge Andrés Grisales Herrera	jandress9791@gmail.com	$2b$12$INhh/PxWsA.g/ewuQrceou5t4pRu6jNYY3S18jThREKtrHv8acNUi	3106796643	3	t	2026-04-09 18:20:26.286414	user
9	Mateo Ruiz	mateo1@test.com	$2b$12$YJbpSG0pwV0YfLYZybhZyO6jbZlhSLsGVlmo5NIXNRPnAJOYqxgNu	\N	3	t	2026-04-09 18:17:45.106112	user
11	Daniela	danielag162020@outlook.com	$2b$12$c/KBkr3L5qJyHZqApBufz.zDUABvl1x2S4kS.lhx.mok9nkfHNAWO	3045738343	3	t	2026-04-14 19:16:35.70024	user
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 5, true);


--
-- Name: places_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.places_id_seq', 21, true);


--
-- Name: promotions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.promotions_id_seq', 8, true);


--
-- Name: question_options_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.question_options_id_seq', 23, true);


--
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.questions_id_seq', 6, true);


--
-- Name: redemptions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.redemptions_id_seq', 9, true);


--
-- Name: user_answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_answers_id_seq', 84, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 11, true);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: places places_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.places
    ADD CONSTRAINT places_pkey PRIMARY KEY (id);


--
-- Name: promotions promotions_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotions
    ADD CONSTRAINT promotions_code_key UNIQUE (code);


--
-- Name: promotions promotions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotions
    ADD CONSTRAINT promotions_pkey PRIMARY KEY (id);


--
-- Name: question_options question_options_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_options
    ADD CONSTRAINT question_options_pkey PRIMARY KEY (id);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- Name: redemptions redemptions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.redemptions
    ADD CONSTRAINT redemptions_pkey PRIMARY KEY (id);


--
-- Name: redemptions redemptions_user_id_promotion_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.redemptions
    ADD CONSTRAINT redemptions_user_id_promotion_id_key UNIQUE (user_id, promotion_id);


--
-- Name: user_answers user_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_answers
    ADD CONSTRAINT user_answers_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: promotions fk_promotions_place; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotions
    ADD CONSTRAINT fk_promotions_place FOREIGN KEY (place_id) REFERENCES public.places(id);


--
-- Name: places places_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.places
    ADD CONSTRAINT places_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: question_options question_options_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_options
    ADD CONSTRAINT question_options_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id);


--
-- Name: redemptions redemptions_promotion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.redemptions
    ADD CONSTRAINT redemptions_promotion_id_fkey FOREIGN KEY (promotion_id) REFERENCES public.promotions(id) ON DELETE CASCADE;


--
-- Name: redemptions redemptions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.redemptions
    ADD CONSTRAINT redemptions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_answers user_answers_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_answers
    ADD CONSTRAINT user_answers_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id);


--
-- Name: user_answers user_answers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_answers
    ADD CONSTRAINT user_answers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 9C5cYdmT4cE6bM0C6qmMyYVuSQQECwYdBanQ1rw0JoA5BqqUjjLeOEfBbnvqJdI

