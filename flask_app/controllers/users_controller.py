from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")


# Register/login routes


@app.route("/register/", methods = ["POST"])
def register():
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : request.form["password"],
        "pass_conf" : request.form["pass_conf"]
    }
    if not User.validate_register(data):
        return redirect("/")
    data["password"] = bcrypt.generate_password_hash(request.form['password'])
    user = User.create_user(data)
    session["user_id"] = user.id
    return redirect("/dashboard/")


@app.route("/login/", methods = ["POST"])
def login():
    data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
    }

    if not User.validate_login(data):
        return redirect("/")
    user = User.get_by_email(data)
    session["user_id"] = user.id
    return redirect("/dashboard/")


@app.route("/dashboard/")
def dashboard():
    data = {
        "user_id" : session["user_id"]
    }
    user = User.get_one_user(data)
    return render_template("dashboard.html", user = user)


@app.route("/logout/")
def logout():
    session.clear()
    return redirect("/")