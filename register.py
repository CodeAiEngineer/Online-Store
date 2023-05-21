from flask import request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

import re


class Register:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['online_store']
        

    def register(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        name = data.get('name')
        surname = data.get('surname')
        role = 'client'
        is_admin = False
        is_active = True

        if data.get('is_active') is not None:
            is_active = data['is_active']

        if not username or not password or not email or not name or not surname:
            return jsonify({'message': 'Username, password, email, name, and surname are required.'}), 400

        existing_user = self.db.users.find_one({'username': username})
        if existing_user:
            return jsonify({'message': 'Username already exists. Please enter a different username.'}), 400
        
        existing_email = self.db.users.find_one({'email': email})
        if existing_email:
            return jsonify({'message': 'Email already exists. Please enter a different email.'}), 400

        if len(password) < 8:
            return jsonify({'message': 'Password must be at least 8 characters long.'}), 400
        if len(username) < 4:
            return jsonify({'message': 'Username must be at least 4 characters long.'}), 400
        if not re.search(r'[A-Z]', password):
            return jsonify({'message': 'Password must contain at least one uppercase letter.'}), 400
        if not re.search(r'[a-z]', password):
            return jsonify({'message': 'Password must contain at least one lowercase letter.'}), 400
        if not re.search(r'[!@#$%^&*(),.?"+-:{}|<>]', password):
            return jsonify({'message': 'Password must contain at least one special character.'}), 400
        
        # Email format check
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not(re.fullmatch(regex, email)):
            return jsonify({'message': 'Invalid email format.'}), 400

        hashed_password = generate_password_hash(password)
        new_user = {
            'username': username,
            'password': hashed_password,
            'email': email,
            'name': name,
            'surname': surname,
            'role': role,
            'is_admin': is_admin,
            'is_active': is_active
        }
        self.db.users.insert_one(new_user)

        return jsonify({'message': 'Registration successful.'}), 201