from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = '39de42602ffb6928b9e4414edfdb7961'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://leevi:@localhost:5432"
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute(text("SELECT id, name FROM genre"))
    genres = result.fetchall()
    return render_template("index.html", genres=genres)

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    #Tarkista onko jo olemassa tämän nimistä käyttäjää
    sql = text('SELECT id, password FROM users WHERE username=:username')
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        hash_value = generate_password_hash(password)
        sql = text('INSERT INTO users (username, password) VALUES (:username, :password)')
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        session["username"] = username
        return redirect("/")
    else:
        return render_template("invalid.html")
    

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        return render_template("form.html")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("form.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)


