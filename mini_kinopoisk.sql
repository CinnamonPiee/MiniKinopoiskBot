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
    year INT NOT NULL,
    box_office FLOAT,
    country VARCHAR NOT NULL,
    description TEXT,
    rating FLOAT NOT NULL
);

CREATE TABLE search_serial (
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    janr VARCHAR(60) NOT NULL,
    release_year VARCHAR(60) NOT NULL,
    series_length VARCHAR(10) NOT NULL,
    country VARCHAR NOT NULL,
    description TEXT,
    rating FLOAT NOT NULL
);

CREATE TABLE history_search_film (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    film_id INT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT TIMEZONE('utc', now()),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (film_id) REFERENCES search_film(id) ON DELETE CASCADE
);

CREATE TABLE history_search_serial (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    serial_id INT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT TIMEZONE('utc', now()),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (serial_id) REFERENCES search_serial(id) ON DELETE CASCADE
);

