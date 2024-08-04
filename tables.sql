CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT, 
    password TEXT
);

CREATE TABLE genre (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE book (
    id SERIAL PRIMARY KEY,
    name TEXT,
    genre_id INTEGER REFERENCES genre
);

CREATE TABLE review (
    id SERIAL PRIMARY KEY,
    content TEXT,
    grade INTEGER
    movie_id INTEGER
);
    