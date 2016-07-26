from system.core.model import Model
import re
from flask.ext.bcrypt import Bcrypt

bcrypt = Bcrypt()

class Registration(Model):
    def __init__(self):
        super(Registration, self).__init__()

    def register_user(self, user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        errors = []

        if not user['name']:
            errors.append('Name cannot be blank')
        if len(user['first_name']) < 2:
            errors.append("Name must be at least 2 characters long")
        if not user['first_name'].isalpha():
            errors.append("Name must only contain letters")
        if not user['email']:
            errors.append('Email cannot be blank')
        if not EMAIL_REGEX.match(user['email']):
            errors.append("Invalid Email Address!")
        if not user['password']:
            errors.append('Password cannot be blank')
        if len(user['password']) < 8:
            errors.append("Password must be at least 8 characters.")
        if user['password'] != user['confirm_pw']:
            errors.append("Password and confirmation do not match.")    
        if errors:
            return {"status": False, "errors": errors}
        else:
            password = user['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO users (name, email, password, created_at, updated_at) VALUES (:name, :email, :password, NOW(), NOW())"
            data = {
                'name': user['name'],
                'email': user['email'],
                'password': hashed_pw
            }
            self.db.query_db(query, data)
            return {"status": True}

    def login_validation(self, user):
        password = user['password']
        query = "SELECT * FROM users WHERE email = :temp_email"
        data = {'temp_email': user['email']}
        user = self.db.query_db(query, data)
        if not user:
            return False
        else:
            if self.bcrypt.check_password_hash(user[0]['password'], password):
                return user
        else:
            return False