from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = 'login_and_reg'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['update_at']

    @staticmethod
    def validate_user(users):
        is_valid = True
        if len(users['firstn']) < 2:
            flash('First name must be at least 3 characters.')
            is_valid = False
        if len(users['lastn']) < 2:
            flash('Last name must be at least 3 characters.')
            is_valid = False
        if not EMAIL_REGEX.match(users['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(users['passw']) < 1:
            flash('Password is required!')
            is_valid = False
        elif len(users['passw']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters!')
        if users['passw'] != users['confirm_passw']:
            is_valid = False
            flash('Passwords must match!')
        return is_valid

    @classmethod
    def create_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, 
        password, created_at, update_at)
        VALUES ( %(firstn)s, %(lastn)s, %(email)s, %(passw)s, NOW(), NOW());"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results


    @classmethod
    def get_user(cls, id):
        query = """SELECT * FROM users
                    WHERE id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, {'id': id})
        return cls(results[0])

    @classmethod
    def login_user(cls, data):
        query = """SELECT * FROM users
                    WHERE email = %(email)s"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])