from app import app, db
from flask import Flask, redirect, render_template, request, session, url_for, abort
import visits
import secrets



@app.route("/")
def index():
    username = session.get("username")
    if not username:
        return redirect("/login")
    
    list = visits.get_list()
    if not list:
        list = []
    count = len(list)
    return render_template("index.html", reviews=list, count=count)

@app.route("/get_reviews_by_book", methods=["POST"])
def book():
    book = request.form["input"]
    results = visits.get_list()
    new_list = []
    for i in results:
        if i[5] == book:
            new_list.append(i)
    count = len(new_list)
    return render_template("index.html", reviews=new_list, count=count)



    
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        errors = []

        if len(username) < 4 or len(username) > 15:
            errors.append("Käyttäjätunnuksen pitää olla 4-15 merkkiä")
        
        if len(password) < 8 or len(password) > 24:
            errors.append("Salasanan pitää olla 4-15 merkkiä")
        
        if password == username:
            errors.append("Käyttäjätunnus ja salasana eivät voi olla samat")

        result = visits.register(username, password)
        if not result:
            errors.append("Käyttäjätunnus on varattu")

        if errors:
            return render_template("register.html", errors=errors)
        
        session["username"] = username
        session["user_id"] = visits.get_user_id()
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    
    if request.method == "GET":
        return render_template("register.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if visits.login(username, password):
            session["username"] = username
            session["user_id"] = visits.get_user_id()
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return render_template("login.html", error="Kirjautuminen epäonnistui")
        
    return render_template("login.html")

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        author = request.form["author"]
        name = request.form["name"]
        content = request.form["content"]
        number = request.form["number"]
        user_id = visits.get_user_id()
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        errors = []

        if len(author) < 4 or len(author) > 30:
            errors.append("Tarkista kirjailijan nimi")
        if len(name) < 4 or len(name) > 30:
            errors.append("Tarkista kirjan nimi")
        if len(content) < 20 or len(content) > 200:
            errors.append("Arvostelun pituus pitää olla 20-200 merkkiä")

        if len(errors) > 0:
            return render_template("new.html", errors=errors)

        if visits.new_review(user_id, author, name, content, number):
            return redirect("/")
        
    if request.method == "GET":
        return render_template("new.html")
    
@app.route("/comment/<int:review_id>")
def comment(review_id):
    review = visits.get_review(review_id)
    comments = visits.get_comments(review_id)
    count = len(comments)
    return render_template("review.html", review=review, comments=comments, count=count)

@app.route("/new_comment/<int:review_id>", methods=["POST"])
def new_comment(review_id):
    user_id = visits.get_user_id()
    review_id = review_id
    content = request.form["content"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if len(content) < 20 or len(content) > 200:
        review = visits.get_review(review_id)
        comments = visits.get_comments(review_id)
        count = len(comments)
        return render_template("review.html", review=review, comments=comments, count=count, error="Kommentin pituus täytyy olla 20-200")
    if visits.insert_comment(user_id, review_id, content):
        return redirect(url_for('comment', review_id=review_id))
    
@app.route("/submit/<string:review_name>", methods=["POST"])
def add_favourite(review_name):
    book_id = visits.get_book_id(review_name)
    user_id = visits.get_user_id()
    if visits.add_favourite_book(user_id, book_id):
        return redirect("/")
    return redirect("/")

@app.route("/favorites")
def favorites():
    user_id = visits.get_user_id()
    result = visits.get_favorites(user_id)
    return render_template("favorites.html", books=result)



@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

