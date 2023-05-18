from flask import request, jsonify, session
from pymongo import MongoClient
from werkzeug.security import check_password_hash
from decorators import check_admin
from bson.objectid import ObjectId
class Login:

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['online_store']
        

    def login(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if not username or not password:
            return jsonify({'message': 'Username and password are required.'}), 400

        user = self.db.users.find_one({'username': username})
        if not user or not check_password_hash(user['password'], password):
            return jsonify({'message': 'Invalid username or password.'}), 401

        if user['is_active'] != True:  
            return jsonify({'message': 'Deactive user cannot login.'}), 401

        is_admin = False
        if user['role'] == 'admin':
            is_admin = True

        session['username'] = username  
        session['is_admin'] = is_admin

        return jsonify({'message': 'Login successful.', 'is_admin': is_admin, 'token': session.sid}), 200

    # Activate/Deactivate User
    @check_admin
    def activate_deactivate_user(self,user_id):
        
        if not check_admin:
            return jsonify({'message': 'Unauthorized.'}), 401
        
        user = self.db.users.find_one({'username': session['username']})
        if user['is_active'] != True:  
            return jsonify({'message': 'Deactive users cannot access this method..'}), 401    

        data = request.get_json()
        is_active = data['is_active']

        user = self.db.users.find_one_and_update(
            {'_id': ObjectId(user_id)},
            {'$set': {'is_active': is_active}},
            return_document=True
        )
        
        user2= self.db.users.find_one({'_id': ObjectId(user_id)})

        if not user:
            return jsonify({'message': 'User not found.'}), 404

        return jsonify({'message': 'User updated.', 'user': user2['username']}), 200