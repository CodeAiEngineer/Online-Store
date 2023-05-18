from functools import wraps
from flask import session, abort
from pymongo import MongoClient

def check_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client = MongoClient('mongodb://localhost:27017')
        db = client['online_store']
        user = db.users.find_one({'username': session['username']})
        if not user or not user['is_admin']:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function
