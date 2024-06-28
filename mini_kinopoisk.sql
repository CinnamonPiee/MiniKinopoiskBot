CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    email VARCHAR(60) NOT NULL UNIQUE,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    telegram_id BIGINT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT TIMEZONE('utc', now())
);

CREATE TABLE search_film (
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    janr VARCHAR(60) NOT NULL,
    year INTEGER NOT NULL,
    box_office FLOAT,
    country VARCHAR(60) NOT NULL,
    description TEXT,
    rating FLOAT NOT NULL
);

CREATE TABLE history_search (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    film_id INTEGER NOT NULL REFERENCES search_film(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT TIMEZONE('utc', now())
);
