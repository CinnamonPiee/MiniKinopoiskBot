CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    email VARCHAR(60) NOT NULL UNIQUE,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    telegram_id BIGINT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT TIMEZONE('utc', now())
);

CREATE TABLE IF NOT EXISTS search_film (
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    janr VARCHAR(60),
    year INTEGER,
    country VARCHAR(60),
    movie_length INTEGER,
    description TEXT,
    rating FLOAT,
    age_rating INTEGER,
    picture VARCHAR
);

CREATE TABLE IF NOT EXISTS search_serial (
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    janr VARCHAR(60),
    rating FLOAT,
    release_year VARCHAR(60),
    series_length VARCHAR(10),
    country VARCHAR(60),
    age_rating INTEGER,
    description TEXT,
    picture VARCHAR
);

CREATE TABLE IF NOT EXISTS history_search_film (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    film_id BIGINT NOT NULL REFERENCES search_film(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT TIMEZONE('utc', now())
);

CREATE TABLE IF NOT EXISTS history_search_serial (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    serial_id BIGINT NOT NULL REFERENCES search_serial(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT TIMEZONE('utc', now())
);
