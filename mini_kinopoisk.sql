CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    email VARCHAR(60) NOT NULL UNIQUE,
    phone_number VARCHAR(15) NOT NULL UNIQUE,
    telegram_id BIGINT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);

CREATE TABLE search_film (
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    janr VARCHAR(60) NOT NULL,
    year INTEGER NOT NULL,
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
    user_id BIGINT NOT NULL,
    film_id BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (film_id) REFERENCES search_film(id) ON DELETE CASCADE
);

CREATE TABLE history_search_serial (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    serial_id BIGINT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (serial_id) REFERENCES search_serial(id) ON DELETE CASCADE
);

