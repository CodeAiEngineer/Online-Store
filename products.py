from flask import request, jsonify, session
from pymongo import MongoClient

from bson.objectid import ObjectId
from decorators import check_admin
from flask_session import Session
from flask import session
class Products:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['online_store']
        
    

    @check_admin
    def create_product(self):
        if not check_admin:
            return jsonify({'message': 'Unauthorized.'}), 401

        data = request.get_json()
        name = data['name']
        amount_in_stock = data['amount_in_stock']
        in_stock = True
        price = data['price']
        category_id = data['category_id']

        if not name or amount_in_stock is None or price is None or not category_id:
            return jsonify({'message': 'Invalid product data.'}), 400

        category = self.db.categories.find_one({'_id': ObjectId(category_id)})
        if not category:
            return jsonify({'message': 'Invalid category ID.'}), 400

        user = self.db.users.find_one({'username': session['username']})
        if not isinstance(user['_id'], ObjectId):
            user['_id'] = ObjectId(user['_id'])

        if user['is_active'] != True:  
            return jsonify({'message': 'Deactive users cannot access this method..'}), 401
        if amount_in_stock <= 0:
            return jsonify({'message': 'Count must be greater than zero.'}), 400
        # Check if the product already exists
        product = self.db.products.find_one({'name': name})
        if product:
            # If the product exists, update its amount in stock
            new_amount = product['amount_in_stock'] + amount_in_stock
            self.db.products.update_one({'_id': product['_id']}, {'$set': {'amount_in_stock': new_amount}})
        else:
            # If the product does not exist, create a new product
            product = {
                'name': name,
                'amount_in_stock': amount_in_stock,
                'in_stock': in_stock,
                'price': price,
                'category_id': category['_id']
            }
            result = self.db.products.insert_one(product)

        return jsonify({'message': 'Product created.', 'product_id': str(product['_id'])}), 201

 # Update Product

    @check_admin
    def update_product(self,product_id):
        if not check_admin:
            return jsonify({'message': 'Unauthorized.'}), 401

        data = request.get_json()
        name = data['name']
        amount_in_stock = data['amount_in_stock']
        price = data['price']
        category_id = data['category_id']

        if not name or amount_in_stock is None or price is None or not category_id:
            return jsonify({'message': 'Invalid product data.'}), 400

        category = self.db.categories.find_one({'_id': ObjectId(category_id)})
        if not category:
            return jsonify({'message': 'Invalid category ID.'}), 400
        
        user = self.db.users.find_one({'username': session['username']})
        if user['is_active'] != True:  
            return jsonify({'message': 'Deactive users cannot access this method..'}), 401
        if amount_in_stock <= 0:
            return jsonify({'message': 'Count must be greater than zero.'}), 400
        product = self.db.products.find_one_and_update(
            {'_id': ObjectId(product_id)},
            {'$set': {
                'name': name,
                'amount_in_stock': amount_in_stock,
                'price': price,
                'category_id': category['_id']
            }},
            return_document=True
        )

        if not product:
            return jsonify({'message': 'Product not found.'}), 404

        return jsonify({'message': 'Product updated.', 'product': name}), 200


    # Delete Product

    @check_admin
    def delete_product(self,product_id):
        if not check_admin:
            return jsonify({'message': 'Unauthorized.'}), 401

        result = self.db.products.delete_one({'_id': ObjectId(product_id)})

        if result.deleted_count == 0:
            return jsonify({'message': 'Product not found.'}), 404

        return jsonify({'message': 'Product deleted.'}), 200
    

    #Get products 
    

    def display_products(self):
        products = self.db.products.find({'$and': [{'amount_in_stock': {'$gt': 0}}, {'in_stock': True}, {'amount_in_stock': {'$ne': 0}}]})
        response = []
        for product in products:
            category = self.db.categories.find_one({'_id': product['category_id']})
            response.append({
                'id': str(product['_id']),
                'name': product['name'],
                # 'amount_in_stock': product['amount_in_stock'],
                'price': product['price'],
                'category': category['name']
            })

        return jsonify({'products': response}), 200
    
