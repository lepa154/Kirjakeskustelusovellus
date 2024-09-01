from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

def get_list():
    result = db.session.execute(text('SELECT R.id, R.content, U.username, R.sent_at, R.grade, B.name FROM reviews R JOIN users U ON R.user_id = U.id JOIN books B ON R.book_id = B.id ORDER BY R.id'))
    x = result.fetchall()
    return x

def register(username, password):
    sql = text('SELECT id, password FROM users WHERE username=:username')
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        hash_value = generate_password_hash(password)
        sql = text('INSERT INTO users (username, password) VALUES (:username, :password)')
        result = db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        user_id = db.session.execute(text('SELECT id FROM users WHERE username=:username'), {"username": username}).fetchone()[0]
        session["user_id"] = user_id
        
        return True
    else:
        return False

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        return False
    else:
        user_id = user[0]
        hash_value = user[1]
        if check_password_hash(hash_value, password):
            session["user_id"] = user_id
            return True
        else:
            return False
        
def get_user_id():
    return session.get("user_id")

def get_book_id(book_name):
    sql = 'SELECT id FROM books WHERE name=:name'
    result = db.session.execute(text(sql), {"name":book_name})
    return result.fetchone()[0]

def add_favourite_book(user_id, book_id):
    sql = 'SELECT * FROM favorites WHERE user_id=:user_id AND book_id=:book_id'
    result = db.session.execute(text(sql), {"user_id":user_id, "book_id":book_id})
    row = result.fetchone()
    if row is None:
        sql = 'INSERT INTO favorites (user_id, book_id, added_at) VALUES (:user_id, :book_id, :added_at)'
        result = db.session.execute(text(sql), {"user_id":user_id, "book_id":book_id, "added_at":datetime.now()})
        db.session.commit()
        return True
    return False
    #tarkista onko kirja jo suosikeissa

def get_favorites(user_id):
    sql = 'SELECT B.name, F.added_at FROM favorites F INNER JOIN books B ON F.book_id = B.id WHERE F.user_id = :user_id'
    result = db.session.execute(text(sql), {"user_id":user_id})
    return result.fetchall()

        
def new_review(user_id, author, name, content, number):
    #tarkista, onko kirjaa kannassa
    result = db.session.execute(text('SELECT id, name FROM books WHERE name=:name'), {"name":name})
    book = result.fetchone()

    #lisää tietokantaan
    if not book:
        genre = "-"
        sql = 'INSERT INTO books (name, author, genre) VALUES (:name, :author, :genre) RETURNING id'
        result = db.session.execute(text(sql), {"name":name, "author":author, "genre":genre})
        db.session.commit()
        book_id = result.fetchone()[0]

    else:
        book_id = book[0]

    sql = 'INSERT INTO reviews (content, grade, book_id, user_id, sent_at) VALUES (:content, :grade, :book_id, :user_id, :sent_at)'
    db.session.execute(text(sql), {"content":content, "grade":number, "book_id":book_id, "user_id":user_id, "sent_at":datetime.now()})
    db.session.commit()
    return True

def get_review(review_id):
    #hae arvostelu
    sql = 'SELECT R.id, R.content, U.username, R.sent_at, R.grade, B.name FROM reviews R JOIN users U ON R.user_id = U.id JOIN books B ON R.book_id = B.id WHERE R.id = :review_id'
    result = db.session.execute(text(sql), {"review_id": review_id})
    return result.fetchone()

def get_comments(review_id):
    sql = 'SELECT C.content, U.username, C.sent_at FROM comments C JOIN users U ON C.user_id = U.id WHERE C.review_id = :review_id ORDER BY C.sent_at'
    result = db.session.execute(text(sql), {"review_id": review_id})
    return result.fetchall()

def insert_comment(user_id, review_id, content):
    try:
        sql = 'INSERT INTO comments (content, user_id, review_id, sent_at) VALUES (:content, :user_id, :review_id, :sent_at)'
        result = db.session.execute(text(sql), {"content": content, "user_id": user_id, "review_id": review_id, "sent_at": datetime.now()})
        db.session.commit()
        return True
    except:
        return False
