CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT,
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    name TEXT,
    author TEXT,
    genre TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    content TEXT,
    grade INTEGER,
    book_id INTEGER REFERENCES books(id),
    user_id INTEGER REFERENCES users(id),
    sent_at TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users(id),
    review_id INTEGER REFERENCES reviews(id),
    sent_at TIMESTAMP
);
    
    
