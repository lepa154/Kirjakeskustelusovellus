from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

def get_list():
    result = db.session.execute(text('SELECT R.content, U.username, R.sent_at FROM reviews R, users U WHERE R.user_id=U.id ORDER BY R.id'))
    x = result.fetchall()
    return x

def register(username, password):
    sql = text('SELECT id, password FROM users WHERE username=:username')
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        hash_value = generate_password_hash(password)
        sql = text('INSERT INTO users (username, password) VALUES (:username, :password)')
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
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
        hash_value = user[1]
        if check_password_hash(hash_value, password):
            return True
        else:
            return False
        
def get_user_id():
    return session.get("user_id", 0)
        
def new_review(user_id, author, name, content, number):
    #tarkista, onko kirjaa kannassa
    result = db.session.execute(text('SELECT id, name FROM books WHERE name=:name'), {"name":name})
    book = result.fetchone()

    #lisää tietokantaan
    if not book:
        genre = "-"
        sql = 'INSERT INTO books (name, author, genre) VALUES (:name, :author, :genre) RETURNING id'
        result = db.session.execute(sql, {"name":name, "author":author, "genre":genre})
        book_id = result.fetchone()[0]

    else:
        book_id = book[0]

    sql = 'INSERT INTO reviews (content, grade, book_id, user_id, sent_at) VALUES (:content, :grade, :book_id, :user_id, :sent_at)'
    db.session.execute(sql, {"content":content, "grade":number, "book_id":book_id, "user_id":user_id, "sent_at":datetime.now()})
    db.session.commit()
    return True