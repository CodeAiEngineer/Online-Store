from flask import  request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from decorators import check_admin

class Categories:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['online_store']

    # def check_admin(self):
    #     def decorator(f):
    #         @wraps(f)
    #         def decorated_function(*args, **kwargs):
    #             user = self.db.users.find_one({'username': session['username']})
    #             if not user or not user['is_admin']:
    #                 abort(401)
    #             return f(*args, **kwargs)
    #         return decorated_function
    #     return decorator

    @check_admin
    def create_category(self):
        data = request.get_json()
        name = data['name']
        existing_category = self.db.categories.find_one({'name': name})
        if existing_category:
            return jsonify({'message': 'Category already exists.'}), 400
        new_category = {'name': name}
        self.db.categories.insert_one(new_category)
        return jsonify({'message': 'Category created successfully.'}), 201

    def get_all_categories(self):
        categories = []
        for category in self.db.categories.find():
            category['_id'] = str(category['_id'])
            categories.append(category)
        return jsonify({'categories': categories})

    def get_category_by_id(self, category_id):
        category = self.db.categories.find_one({'_id': ObjectId(category_id)})
        if not category:
            return jsonify({'message': 'Category not found.'}), 404
        category['_id'] = str(category['_id'])
        return jsonify(category)

    @check_admin
    def update_category(self, category_id):
        data = request.get_json()
        name = data['name']
        existing_category = self.db.categories.find_one({'name': name})
        if existing_category and existing_category['_id'] != ObjectId(category_id):
            return jsonify({'message': 'Category already exists.'}), 400
        updated_category = {'name': name}
        self.db.categories.update_one({'_id': ObjectId(category_id)}, {'$set': updated_category})
        return jsonify({'message': 'Category updated successfully.'})

    @check_admin
    def delete_category(self, category_id):
        result = self.db.categories.delete_one({'_id': ObjectId(category_id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Category deleted successfully.'})
        else:
            return jsonify({'message': 'Category not found.'}), 404


    
    
    def filter_products_by_category(self,category_id):
        category = self.db.categories.find_one({'_id': ObjectId(category_id)})
        if not category:
            return jsonify({'message': 'Invalid category ID.'}), 400

        products = self.db.products.find({'category_id': category['_id'], 'amount_in_stock': {'$gt': 0}})
        response = []
        for product in products:
            response.append({
                'id': str(product['_id']),
                'name': product['name'],
                'amount_in_stock': product['amount_in_stock'],
                'price': product['price'],
                'category': category['name']
            })

        return jsonify({'products': response}), 200