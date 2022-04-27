from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    db = "recipies_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipies = []
        self.user_likes = []

    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data["first_name"]) < 2:
            flash("First Name must be at least 2 characters!")
            is_valid = False
        if len(data["last_name"]) < 2:
            flash("Last Name must be at least 2 characters!")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid Email")
            is_valid = False
        if User.get_by_email(data):
            flash("Email already in use! Please use a different email address!")
        if len(data["password"]) < 8:
            flash("Password must be at least 8 characters!")
            is_valid = False
        if data["password"] != data["pass_conf"]:
            flash("Passwords must match!")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        user_in_db = User.get_by_email(data)
        if not user_in_db:
            flash("Invalid Email/Password")
            is_valid = False
        elif not bcrypt.check_password_hash(user_in_db.password, data["password"]):
            flash("Invalid Email/Password")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_recipies(cls, data):
        query = "SELECT * FROM users L"
