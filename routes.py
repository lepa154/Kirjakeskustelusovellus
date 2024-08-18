from app import app, db
from flask import Flask, redirect, render_template, request, session
import visits



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
    
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #Tarkista onko jo olemassa tämän nimistä käyttäjää
        if visits.register(username, password):
            session["username"] = username
            return redirect("/")
        return render_template("register.html", error="Rekisteröinti epäonnistui")
    
    return render_template("register.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if visits.login(username, password):
            session["username"] = username
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
        if visits.new_review(user_id, author, name, content, number):
            return redirect("/")
    if request.method == "GET":
        return render_template("new.html")
    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")